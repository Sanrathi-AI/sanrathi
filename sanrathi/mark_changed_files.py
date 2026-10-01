"""Apache License 2.0, section 4(b): a work we distribute in modified form
must carry "prominent notices stating that [we] changed the files". This adds
a one-line "Modified by Sanrathi, 2026" comment to the top of every text file
changed since the Presenton fork point, in the right comment syntax for its
type, and skips files that already have the marker. Binary files (images,
icons) can't carry a comment, so they are only listed in SANRATHI_CHANGES.md.

Run from the repo root, after other edits are committed:
    python sanrathi/mark_changed_files.py <fork-point-commit>
"""
import subprocess
import sys
from pathlib import Path

MARKER = "Modified by Sanrathi, 2026"

COMMENT_STYLE = {
    ".tsx": "//", ".ts": "//", ".js": "//", ".cjs": "//", ".mjs": "//",
    ".py": "#",
    ".css": ("/*", "*/"),
    ".svg": ("<!--", "-->"),
}


def comment_line(suffix: str) -> str | None:
    style = COMMENT_STYLE.get(suffix)
    if style is None:
        return None
    if isinstance(style, tuple):
        start, end = style
        return f"{start} {MARKER} {end}\n"
    return f"{style} {MARKER}\n"


def mark(path: Path) -> bool:
    line = comment_line(path.suffix)
    if line is None:
        return False
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False

    lines = text.splitlines(keepends=True)
    insert_at = 0
    # Keep a leading "use client"/"use server" directive first (Next.js
    # requires it to be the first statement in the file).
    if lines and lines[0].strip().strip(";") in ('"use client"', "'use client'",
                                                   '"use server"', "'use server'"):
        insert_at = 1
    lines.insert(insert_at, line)
    path.write_text("".join(lines), encoding="utf-8")
    return True


def main() -> None:
    fork_point = sys.argv[1] if len(sys.argv) > 1 else "2dcbde77"
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{fork_point}..HEAD", "--",
         "servers", "templates", "start.js", "docker-compose.yml"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()

    marked, skipped_binary, already = [], [], []
    for rel in out:
        if rel.startswith("templates/sanrathi-"):
            continue  # new template folders, not modifications of an existing file
        path = Path(rel)
        if not path.exists():
            continue
        if path.suffix not in COMMENT_STYLE:
            skipped_binary.append(rel)
            continue
        if mark(path):
            marked.append(rel)
        else:
            already.append(rel)

    print(f"Marked {len(marked)} files, {len(already)} already marked, "
          f"{len(skipped_binary)} binary files left unmarked (list them by hand):")
    for rel in skipped_binary:
        print(f"  binary: {rel}")


if __name__ == "__main__":
    main()
