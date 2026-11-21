#!/usr/bin/env python3
"""Pre-move checker for a JetBrains project folder.

Run BEFORE moving a PyCharm / GoLand project root to a new location:

    python check_project_move.py /path/to/project [/new/location]

It is read-only: it never moves, edits, or deletes anything. It checks
exactly the things that can break a move, and prints a short verdict:

  * absolute references to the old location inside the project
    (scripts, configs, .env, .idea run configurations, ...)
  * an in-project .venv (its internals hold absolute paths: recreate it)
  * git worktrees / submodules / a .git file pointing elsewhere
  * absolute symlinks (relative ones travel fine if their target moves too)
  * Go `replace` directives in go.mod pointing at absolute paths
  * whether .git and .idea are present at all (both must move with the root)

Exit code 0 = nothing found that would break the move (notes may still
apply). Exit code 1 = at least one blocking item was found.
Exit code 2 = usage error (missing / unreadable project folder).

Standard library only. Output paths are beside the script's working
directory only in the sense that this script writes nothing at all.
"""

import os
import re
import sys

# Folders never worth scanning for text matches: version-control data,
# caches, and virtualenvs (the .venv gets its own dedicated check below).
SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".idea",
    "node_modules", ".mypy_cache", ".pytest_cache", ".tox",
}
# File extensions treated as text. Anything else is skipped unless it is
# a known config name (handled below). Binary files are never read.
TEXT_EXTS = {
    ".py", ".go", ".js", ".ts", ".json", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".env", ".txt", ".md", ".xml", ".html", ".css",
    ".sh", ".bat", ".dockerfile", ".properties", ".gradle",
}
TEXT_NAMES = {
    ".env", "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "go.mod", "go.sum", "Makefile", "requirements.txt",
}
MAX_FILE_BYTES = 2_000_000  # skip unexpectedly huge files


def is_text_file(path, name):
    if name in TEXT_NAMES:
        return True
    _, ext = os.path.splitext(name)
    return ext.lower() in TEXT_EXTS


def scan_for_old_path(root, old_path):
    """Return [(rel_path, line_no, line)] for text files mentioning old_path."""
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if name == "go.mod":
                # Covered by the dedicated replace-directive check below.
                continue
            if not is_text_file(path, name):
                continue
            try:
                if os.path.getsize(path) > MAX_FILE_BYTES:
                    continue
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    for lineno, line in enumerate(fh, 1):
                        if old_path in line:
                            hits.append(
                                (os.path.relpath(path, root), lineno, line.rstrip())
                            )
            except OSError:
                continue
    return hits


def scan_idea_configs(root, old_path):
    """Run/debug configs live in .idea/*.xml; report absolute-path hits there."""
    idea = os.path.join(root, ".idea")
    hits = []
    if not os.path.isdir(idea):
        return hits
    for name in sorted(os.listdir(idea)):
        if not name.endswith(".xml"):
            continue
        path = os.path.join(idea, name)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                for lineno, line in enumerate(fh, 1):
                    if old_path in line and "$PROJECT_DIR$" not in line:
                        hits.append((os.path.join(".idea", name), lineno, line.rstrip()))
        except OSError:
            continue
    return hits


def check_git(root):
    """Return (notes, problems) about the .git layout."""
    notes, problems = [], []
    git = os.path.join(root, ".git")
    if not os.path.exists(git):
        problems.append("No .git here — this folder is not a git checkout "
                        "(or .git was lost in an earlier copy).")
        return notes, problems
    if os.path.isfile(git):
        # A .git *file* means a worktree or a submodule: it points elsewhere.
        try:
            with open(git, "r", encoding="utf-8", errors="ignore") as fh:
                target = fh.read().strip()
            problems.append(".git is a file, not a folder (%s) — this is a "
                            "linked worktree or submodule; move it only with "
                            "its gitdir." % target)
        except OSError:
            problems.append(".git is a file and could not be read.")
        return notes, problems
    notes.append(".git folder present.")
    # Worktrees and submodules registered inside .git/config.
    config = os.path.join(git, "config")
    try:
        with open(config, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        if "worktree" in text.lower():
            notes.append(".git/config mentions worktrees — check `git worktree list`.")
        for m in re.finditer(r"url\s*=\s*(/\S+)", text):
            problems.append("Submodule / remote URL is an absolute local path: %s"
                            % m.group(1))
    except OSError:
        pass
    return notes, problems


def check_venv(root):
    venv = os.path.join(root, ".venv")
    if os.path.isdir(venv):
        return ["In-project .venv found — do NOT move it as-is; its internals "
                "hold absolute paths. Recreate it at the new location instead."]
    return []


def check_symlinks(root):
    """Absolute symlinks break (or point back) after a move."""
    problems, notes = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(dirnames + filenames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                target = os.readlink(path)
                rel = os.path.relpath(path, root)
                if os.path.isabs(target):
                    if target.startswith(root + os.sep) or target == root:
                        problems.append("Absolute symlink inside the project: "
                                        "%s -> %s (will point at the OLD "
                                        "location after the move)" % (rel, target))
                    else:
                        notes.append("Absolute symlink to outside the project: "
                                     "%s -> %s (still valid after the move)"
                                     % (rel, target))
    return notes, problems


def check_go_mod(root):
    problems = []
    gomod = os.path.join(root, "go.mod")
    if not os.path.isfile(gomod):
        return problems
    try:
        with open(gomod, "r", encoding="utf-8", errors="ignore") as fh:
            for lineno, line in enumerate(fh, 1):
                m = re.search(r"replace\s+\S+\s+=>\s+(/\S+)", line)
                if m:
                    problems.append("go.mod line %d: replace directive points "
                                    "at an absolute path: %s"
                                    % (lineno, m.group(1)))
    except OSError:
        pass
    return problems


def main(argv):
    if len(argv) < 2 or len(argv) > 3:
        print("Usage: python check_project_move.py /path/to/project "
              "[/new/location]", file=sys.stderr)
        return 2
    root = os.path.abspath(argv[1])
    if not os.path.isdir(root):
        print("Not a folder: %s" % root, file=sys.stderr)
        return 2
    new_loc = os.path.abspath(argv[2]) if len(argv) == 3 else None

    print("Checking: %s" % root)
    if new_loc:
        print("Planned move to: %s" % new_loc)

    problems, notes = [], []

    # .idea presence — it holds run configs and interpreter settings.
    if os.path.isdir(os.path.join(root, ".idea")):
        notes.append(".idea folder present (will move with the root).")
    else:
        notes.append("No .idea folder — PyCharm/GoLand will create fresh "
                     "project settings at the new location.")

    git_notes, git_problems = check_git(root)
    notes.extend(git_notes)
    problems.extend(git_problems)

    problems.extend(check_venv(root))

    sl_notes, sl_problems = check_symlinks(root)
    notes.extend(sl_notes)
    problems.extend(sl_problems)

    problems.extend(check_go_mod(root))

    # The main sweep: the old absolute path, anywhere in text files.
    hits = scan_for_old_path(root, root)
    idea_hits = scan_idea_configs(root, root)
    # .idea was skipped in the main sweep, so add its hits separately.
    hits.extend(idea_hits)
    for rel, lineno, line in hits:
        problems.append("%s:%d: still references the old location: %s"
                        % (rel, lineno, line.strip()[:160]))

    print()
    for note in notes:
        print("  note: %s" % note)
    if problems:
        print()
        print("Found %d item(s) to fix before moving:" % len(problems))
        for problem in problems:
            print("  !! %s" % problem)
        print()
        print("Fix the items above, re-run this check, and only then move "
              "the folder (IDE closed, whole root including hidden files).")
        return 1

    print()
    print("OK — nothing found that would break the move.")
    print("Still do the move with the IDE closed, move the whole root "
          "(including hidden .git and .idea), then open the new location "
          "and check git status, the interpreter / Go SDK, and one run.")
    if new_loc:
        print("Note: a named conda env lives outside the project, so moving "
              "the folder does not move or break it — at most re-select the "
              "same interpreter in PyCharm.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
