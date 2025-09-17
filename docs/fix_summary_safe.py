#!/usr/bin/env python3
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\Saboor\Documents\azure-portfolio")

# regex to find <summary ...>Kali Linux Penetration Testing
SUMMARY_RE = re.compile(r'(<summary[^>]*>.*?Kali Linux Penetration Testing)', re.IGNORECASE)
CLOSE_RE = re.compile(r'</summary>', re.IGNORECASE)

for html_file in ROOT.rglob("*.html"):
    text = html_file.read_text(encoding="utf-8")
    new_text = text
    changed = False

    for match in SUMMARY_RE.finditer(text):
        start_idx = match.end()
        # find the next <ul> after the match
        ul_idx = text.find('<ul', start_idx)
        if ul_idx == -1:
            continue
        # check if </summary> exists between match and <ul>
        if CLOSE_RE.search(text[start_idx:ul_idx]):
            continue
        # insert </summary> before <ul>
        new_text = new_text[:ul_idx] + '</summary>\n' + new_text[ul_idx:]
        changed = True

    if changed:
        bak_file = html_file.with_suffix('.bak')
        shutil.copy2(html_file, bak_file)
        html_file.write_text(new_text, encoding="utf-8")
        print(f"Updated {html_file.name} (backup: {bak_file.name})")
