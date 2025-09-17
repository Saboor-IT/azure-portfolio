from pathlib import Path
import re

def fix_with_primary(text: str) -> tuple[str, int]:
    """
    Ensure a </summary> appears immediately after
    the Kali Linux Penetration Testing summary text.
    Returns the modified text and number of replacements.
    """
    pattern = re.compile(
        r'(<summary[^>]*>[^<]*Kali Linux Penetration Testing)(?!\s*</summary>)',
        re.IGNORECASE
    )
    new_text, count = pattern.subn(r'\1</summary>', text)
    return new_text, count

def fallback_insert(text: str) -> tuple[str, int]:
    """
    Fallback: if <summary> exists but no </summary> at all,
    insert one just before the first <ul> inside penTestingDropdown.
    """
    pattern = re.compile(
        r'(<details[^>]+id="penTestingDropdown"[^>]*>\s*<summary[^>]*>[^<]*Kali Linux Penetration Testing[^<]*)(?:(?!</summary>).)*?(<ul)',
        re.IGNORECASE | re.DOTALL
    )
    new_text, count = pattern.subn(r'\1</summary>\2', text)
    return new_text, count

def process_file(path: Path) -> None:
    original = path.read_text(encoding="utf-8")
    updated, changed = fix_with_primary(original)
    if not changed:
        updated, changed = fallback_insert(original)
    if changed:
        path.write_text(updated, encoding="utf-8")
        print(f"Fixed {path}")
    else:
        print(f"No changes needed: {path}")

if __name__ == "__main__":
    root = Path(".")  # current directory (adjust if needed)
    for html_file in root.rglob("*.html"):
        process_file(html_file)
