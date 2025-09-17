#!/usr/bin/env python3
"""
fix_summary.py
Find <summary ...>Kali Linux Penetration Testing ... (missing </summary>)
and insert </summary> before the following <ul> for all .html files under ROOT.
Creates a backup file <filename>.bak for each modified file.
"""

import re
import shutil
from pathlib import Path

# <-- set this to your folder containing the HTML files
ROOT = Path(r"C:\Users\Saboor\Documents\azure-portfolio\docs")

# Pattern used by the primary replacer:
# - find an opening <summary ...> that contains "Kali Linux Penetration Testing"
# - match up to (but not including) the next <ul tag (lookahead)
PRIMARY_RE = re.compile(
    r'(<summary[^>]*>)([\s\S]*?Kali\s+Linux\s+Penetration\s+Testing[\s\S]*?)(?=<\s*ul\b)',
    flags=re.IGNORECASE
)

# helper to detect any closing summary inside a string
CLOSE_RE = re.compile(r'</\s*summary\s*>', flags=re.IGNORECASE)


def fix_with_primary(text: str) -> tuple[str, int]:
    """Use the primary regex with a callable replacement to avoid duplication."""
    edits = 0

    def repl(m):
        nonlocal edits
        opening = m.group(1)
        inner = m.group(2)
        if CLOSE_RE.search(inner):
            return m.group(0)
        edits += 1
        return f"{opening}{inner.rstrip()}</summary>\n"

    new_text = PRIMARY_RE.sub(repl, text)
    return new_text, edits


def fallback_insert(text: str) -> tuple[str, int]:
    """
    Fallback approach:
    - find each occurrence of the phrase
    - find the nearest earlier <summary and the next <ul
    - if there's no </summary> between phrase and <ul, insert </summary> before <ul
    """
    lowered = text.lower()
    phrase = 'kali linux penetration testing'
    start = 0
    edits = 0

    while True:
        idx = lowered.find(phrase, start)
        if idx == -1:
            break
        # find last '<summary' before idx
        open_pos = text.rfind('<summary', 0, idx)
        if open_pos == -1:
            start = idx + len(phrase)
            continue
        # find next '<ul' after idx
        ul_pos = text.find('<ul', idx)
        if ul_pos == -1:
            start = idx + len(phrase)
            continue
        # check if </summary> exists between idx and ul_pos
        if CLOSE_RE.search(text[idx:ul_pos]):
            start = idx + len(phrase)
            continue
        # insert closing tag right before the <ul
        text = text[:ul_pos] + '</summary>\n' + text[ul_pos:]
        lowered = text.lower()  # refresh lowered copy since we modified text
        edits += 1
        start = ul_pos + len('</summary>\n') + len('<ul')

    return text, edits


def main():
    if not ROOT.exists():
        print(f"ERROR: root path does not exist: {ROOT}")
        return

    total_changed = 0
    for f in sorted(ROOT.rglob("*.html")):
        original = f.read_text(encoding="utf-8")
        text = original

        # try primary method
        text, n1 = fix_with_primary(text)

        # fallback to catch edge cases not matched by primary
        text, n2 = fallback_insert(text)

        if (n1 + n2) > 0 and text != original:
            bak = f.with_name(f.name + '.bak')
            shutil.copy2(f, bak)
            f.write_text(text, encoding="utf-8")
            print(f"Modified {f} — primary={n1} fallback={n2} (backup: {bak.name})")
            total_changed += (n1 + n2)
        else:
            print(f"No change: {f}")

    print(f"Done. Total changes made: {total_changed}")


if __name__ == "__main__":
    main()
