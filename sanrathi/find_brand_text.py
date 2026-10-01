"""List every place the word 'Presenton' is VISIBLE to users in the UI, so you
can change it to 'Sanrathi' by hand. It skips code identifiers, imports, API
paths, cookie names and env var names - those must NOT be renamed.
Run from the repo root:  python sanrathi/find_brand_text.py
"""
import re
from pathlib import Path

VISIBLE = re.compile(
    r""">[^<{]*Presenton[^<{]*<"""          # JSX text:  >Welcome to Presenton<
    r"""|(?:alt|title|placeholder|aria-label|label|description)=["'][^"']*Presenton"""
    r"""|["'`][^"'`]*\bPresenton\b[^"'`]*\s[^"'`]*["'`]"""  # sentences in strings
)
SKIP = re.compile(r"import |from ['\"]|presenton_session|PRESENTON_|/api/|@presenton")
for folder in ("servers/nextjs/app", "servers/nextjs/components"):
    for f in sorted(p for p in Path(folder).rglob("*") if p.suffix in {".tsx", ".ts"}):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if VISIBLE.search(line) and not SKIP.search(line):
                print(f"{f}:{i}: {line.strip()[:110]}")
