#!/usr/bin/env python3
"""
lmstudio-lt-bridge: speak LanguageTool HTTP API on the front, LM Studio on the back.

The Obsidian "LanguageTool Integration" plugin supports a "Custom URL" endpoint.
It sends POST requests to <base>/v2/check with form-encoded `text` and `language`
fields and expects a LanguageTool-shaped JSON response (matches with offsets,
replacements and messages).

LM Studio, however, speaks the OpenAI chat-completions API. This bridge sits
between the two: it accepts the plugin's /v2/check requests, asks your LM Studio
model to proofread, and translates the model's findings back into the
LanguageTool format the plugin understands.

Stdlib only -- no pip dependencies.

Configuration via environment variables:
    LT_BRIDGE_HOST    bind address (default 127.0.0.1)
    LT_BRIDGE_PORT    listen port (default 8081)
    LMSTUDIO_URL      LM Studio base URL, e.g. http://192.168.1.20:1234/v1
                      (default http://localhost:1234/v1)
    LMSTUDIO_MODEL    model id to use; default = first model reported by /v1/models
    LMSTUDIO_API_KEY  LM Studio ignores this, but some setups want *something*
                      (default "lm-studio")
    MAX_CHARS         max characters per LLM request; longer notes are split
                      into paragraph chunks (default 6000)
    REQUEST_TIMEOUT   seconds to wait for the model per chunk (default 180)

Usage:
    LMSTUDIO_URL=http://192.168.1.20:1234/v1 python3 lt_bridge.py

Then in Obsidian: Settings -> LanguageTool Integration -> Endpoint -> Custom URL
-> http://localhost:8081
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("LT_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.environ.get("LT_BRIDGE_PORT", "8081"))
LM_URL = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1").rstrip("/")
LM_MODEL = os.environ.get("LMSTUDIO_MODEL", "")
LM_KEY = os.environ.get("LMSTUDIO_API_KEY", "lm-studio")
MAX_CHARS = int(os.environ.get("MAX_CHARS", "6000"))
TIMEOUT = float(os.environ.get("REQUEST_TIMEOUT", "180"))

SYSTEM_PROMPT = (
    "You are a meticulous proofreading engine. Analyze the user's text for "
    "grammar, spelling, and punctuation errors.\n"
    "Ignore Markdown formatting syntax (headings, bold/italic markers, list "
    "dashes, [[wiki links]], URLs) -- only flag errors in the prose itself.\n"
    "Respond with ONLY a JSON array, no markdown fences, no commentary. "
    "Each element must have exactly these keys:\n"
    '  "quote": the exact offending substring, copied VERBATIM from the input '
    "(as short as possible while covering the error),\n"
    '  "message": a short explanation of the error,\n'
    '  "replacements": a JSON array of 1-3 corrected versions of the quote,\n'
    '  "category": one of "Spelling", "Grammar", "Punctuation", "Style".\n'
    "Rules: quotes must appear verbatim in the input text. Do not invent "
    "errors. If the text has no errors, return []. "
    "Report at most 40 issues, most important first."
)

LANG_NAMES = {
    "en": "English", "en-US": "English (US)", "en-GB": "English (UK)",
    "en-AU": "English (Australia)", "en-CA": "English (Canada)",
    "de": "German", "de-DE": "German (Germany)", "de-AT": "German (Austria)",
    "de-CH": "German (Switzerland)", "fr": "French", "es": "Spanish",
    "it": "Italian", "pt": "Portuguese", "pt-BR": "Portuguese (Brazil)",
    "nl": "Dutch", "pl": "Polish", "ru": "Russian", "uk": "Ukrainian",
    "ja": "Japanese", "zh": "Chinese", "auto": "auto-detected",
}

ISSUE_TYPES = {
    "Spelling": "misspelling",
    "Grammar": "grammar",
    "Punctuation": "typographical",
    "Style": "style",
}


def log(*args):
    print(f"[{time.strftime('%H:%M:%S')}]", *args, file=sys.stderr, flush=True)


def lm_request(path, payload=None, timeout=TIMEOUT):
    """Minimal OpenAI-compatible client (GET when payload is None)."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        LM_URL + path,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LM_KEY}",
        },
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


_model_cache = None


def get_model():
    global _model_cache
    if LM_MODEL:
        return LM_MODEL
    if _model_cache:
        return _model_cache
    data = lm_request("/models", timeout=15)
    models = data.get("data", [])
    if not models:
        raise RuntimeError("LM Studio reports no loaded models at " + LM_URL)
    _model_cache = models[0]["id"]
    log("auto-selected model:", _model_cache)
    return _model_cache


def extract_json_array(s):
    """Pull a JSON array out of possibly-chatty model output."""
    s = s.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```$", "", s)
    try:
        v = json.loads(s)
        if isinstance(v, list):
            return v
        if isinstance(v, dict):
            for key in ("issues", "errors", "matches", "results"):
                if isinstance(v.get(key), list):
                    return v[key]
        return []
    except Exception:
        pass
    m = re.search(r"\[.*\]", s, re.S)
    if m:
        try:
            v = json.loads(m.group(0))
            if isinstance(v, list):
                return v
        except Exception:
            pass
    return []


def check_chunk(text, language):
    """Ask the model to proofread one chunk; return raw issue dicts."""
    lang_name = LANG_NAMES.get(language, language or "auto-detected")
    user_content = (
        f"Proofread the following {lang_name} text and return the JSON array "
        f"of issues:\n\n{text}"
    )
    payload = {
        "model": get_model(),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0,
        "max_tokens": 3000,
        "stream": False,
    }
    data = lm_request("/chat/completions", payload)
    content = data["choices"][0]["message"]["content"]
    return extract_json_array(content)


def chunk_text(text):
    """Split long notes into paragraph-aligned chunks, keeping offsets."""
    if len(text) <= MAX_CHARS:
        return [(0, text)]
    parts = re.split(r"(\n\s*\n+)", text)
    chunks, buf, buf_start, pos = [], "", None, 0
    for part in parts:
        if buf_start is None:
            buf_start = pos
        if len(buf) + len(part) > MAX_CHARS and buf.strip():
            chunks.append((buf_start, buf))
            buf, buf_start = "", None
            if not part.strip():  # separator belongs to the gap, not a chunk
                pos += len(part)
                continue
            buf_start = pos
        buf += part
        pos += len(part)
    if buf.strip():
        chunks.append((buf_start, buf))
    return chunks or [(0, text[:MAX_CHARS])]


def to_matches(text, issues):
    """Convert model issues into LanguageTool match objects.

    The model reports the exact offending *quote*; we locate it in the text
    ourselves, because LLMs cannot be trusted to count character offsets.
    """
    matches = []
    seen = set()
    cursor = 0
    for item in issues:
        if not isinstance(item, dict):
            continue
        quote = str(item.get("quote", "") or "")
        if not quote:
            continue
        pos = text.find(quote, cursor)
        if pos == -1:
            pos = text.find(quote)  # retry from the start before giving up
        if pos == -1:
            log("  could not locate quote, skipping:", quote[:60])
            continue
        key = (pos, len(quote))
        if key in seen:
            continue
        seen.add(key)
        cursor = pos + 1

        reps = item.get("replacements") or []
        if isinstance(reps, str):
            reps = [reps]
        replacements = [{"value": str(r)} for r in reps[:3]]

        category = str(item.get("category", "Grammar") or "Grammar").capitalize()
        if category not in ISSUE_TYPES:
            category = "Grammar"
        message = str(item.get("message", "Possible issue.") or "Possible issue.")

        ctx_start = max(0, pos - 40)
        ctx_end = min(len(text), pos + len(quote) + 40)
        matches.append({
            "message": message,
            "shortMessage": "",
            "replacements": replacements,
            "offset": pos,
            "length": len(quote),
            "context": {
                "text": text[ctx_start:ctx_end],
                "offset": pos - ctx_start,
                "length": len(quote),
            },
            "sentence": "",
            "type": {"typeName": "Other"},
            "rule": {
                "id": f"LMSTUDIO_{category.upper()}",
                "description": message,
                "issueType": ISSUE_TYPES[category],
                "category": {"id": category.upper(), "name": category},
            },
            "ignoreForIncompleteSentence": False,
            "contextForSureMatch": 0,
        })
    return matches


class Handler(BaseHTTPRequestHandler):
    server_version = "LTLMStudioBridge/1.0"

    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        log(f"{self.client_address[0]} {args[0] % args[1:]}")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        if path == "/":
            self._send(200, {
                "status": "ok",
                "service": "lmstudio-languagetool-bridge",
                "lmstudio": LM_URL,
            })
        elif path == "/v2/languages":
            self._send(200, [
                {"name": name, "code": code, "longCode": code}
                for code, name in sorted(LANG_NAMES.items())
                if code != "auto"
            ])
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        if path != "/v2/check":
            self._send(404, {"error": f"unknown endpoint {path!r}; expected POST /v2/check"})
            return
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8", "replace")
        ctype = self.headers.get("Content-Type", "")

        fields = {}
        if "application/json" in ctype:
            try:
                fields = json.loads(raw) if raw.strip() else {}
            except Exception:
                fields = {}
        else:  # the Obsidian plugin posts application/x-www-form-urlencoded
            fields = {k: v[0] for k, v in
                      urllib.parse.parse_qs(raw, keep_blank_values=True).items()}

        text = str(fields.get("text", "") or "")
        if not text and fields.get("data"):
            # LanguageTool also allows a JSON `data` array of {text, ...}
            try:
                data = json.loads(fields["data"])
                text = "\n".join(str(d.get("text", "")) for d in data
                                 if isinstance(d, dict))
            except Exception:
                text = ""
        language = str(fields.get("language", "auto") or "auto")
        log(f"check: {len(text)} chars, language={language}")

        if not text.strip():
            self._send(200, empty_response(language))
            return

        try:
            all_matches = []
            for base, chunk in chunk_text(text):
                issues = check_chunk(chunk, language)
                log(f"  chunk @ {base}: {len(issues)} raw issues")
                for m in to_matches(chunk, issues):
                    m["offset"] += base  # context text stays chunk-local
                    all_matches.append(m)
        except Exception as exc:  # noqa: BLE001 -- report backend failure cleanly
            log("LM Studio request failed:", exc)
            self._send(502, {"error": f"LM Studio request failed: {exc}"})
            return

        lang_code = language if language != "auto" else "en-US"
        lang_name = LANG_NAMES.get(lang_code, lang_code)
        self._send(200, {
            "software": {
                "name": "lmstudio-languagetool-bridge",
                "version": "1.0.0",
                "buildDate": "",
                "apiVersion": 1,
                "premium": False,
                "premiumHint": "",
                "status": "",
            },
            "warnings": {"incompleteResults": False},
            "language": {
                "name": lang_name,
                "code": lang_code,
                "detectedLanguage": {
                    "name": lang_name, "code": lang_code, "confidence": 1.0,
                    "source": "languagetool",
                },
            },
            "matches": sorted(all_matches, key=lambda m: m["offset"]),
        })


def empty_response(language):
    lang_code = language if language != "auto" else "en-US"
    return {
        "software": {"name": "lmstudio-languagetool-bridge", "version": "1.0.0",
                     "apiVersion": 1, "premium": False, "status": ""},
        "warnings": {"incompleteResults": False},
        "language": {"name": LANG_NAMES.get(lang_code, lang_code),
                     "code": lang_code},
        "matches": [],
    }


def main():
    try:
        lm_request("/models", timeout=10)
        log("LM Studio reachable at", LM_URL)
    except Exception as exc:  # noqa: BLE001
        log("WARNING: cannot reach LM Studio at", LM_URL, "--", exc)
        log("The bridge will still start, but checks will fail until it is up.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    log(f"listening on http://{HOST}:{PORT}  ->  LM Studio at {LM_URL}")
    log("In Obsidian: Settings -> LanguageTool Integration -> Endpoint -> "
        "Custom URL -> http://%s:%d" % (HOST, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("shutting down")


if __name__ == "__main__":
    main()
