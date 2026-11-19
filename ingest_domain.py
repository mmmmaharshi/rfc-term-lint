"""Fetch Terminology sections for given RFC numbers. Usage: python ingest_domain.py 9000 9110 9114"""

import re, json, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).parent


def get(n):
    return (
        urllib.request.urlopen(f"https://www.rfc-editor.org/rfc/rfc{n}.txt", timeout=30)
        .read()
        .decode("utf-8", errors="ignore")
    )


def parse_terminology(text):
    m = re.search(
        r"(?im)^\d+\.?\s+terminology\b(.*?)(?=^\d+\.?\s+[A-Z]|\Z)", text, re.S
    )
    if not m:
        return []
    return re.findall(
        r"(?m)^\s*(?:o\s+)?([A-Z][A-Za-z0-9 /-]{2,40})\s*:\s*(.+)", m.group(1)
    )


def main(ns):
    out = {}
    for n in ns:
        if not re.fullmatch(r"\d+", n):
            print(f"skip {n!r}: not an RFC number")
            continue
        try:
            terms = parse_terminology(get(n))
        except Exception as e:
            print(f"rfc{n}: fetch failed: {e}")
            continue
        if not terms:
            print(f"rfc{n}: no Terminology section")
            continue
        out[n] = [{"term": k.strip(), "def": v.strip()} for k, v in terms]
        print(f"rfc{n}: {len(out[n])} terms")
    if not out:
        raise SystemExit("no terms found; domain_terms.json left untouched")
    (HERE / "domain_terms.json").write_text(json.dumps(out, indent=2))
    print(f"wrote domain_terms.json ({sum(map(len, out.values()))} terms)")


if __name__ == "__main__":
    main(sys.argv[1:] or ["9110"])
