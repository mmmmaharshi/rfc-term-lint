"""Fetch Terminology sections for given RFC numbers. Usage: python ingest_domain.py 9000 9110 9114"""

import re, json, sys, urllib.request


def get(n):
    return (
        urllib.request.urlopen(f"https://www.rfc-editor.org/rfc/rfc{n}.txt", timeout=30)
        .read()
        .decode("utf-8", errors="ignore")
    )


out = {}
for n in sys.argv[1:] or ["9000"]:
    try:
        t = get(n)
    except Exception as e:
        print(f"rfc{n}: fetch failed: {e}")
        continue
    m = re.search(r"(?im)^\d+\.?\s+terminology\b(.*?)(?=^\d+\.?\s+[A-Z]|\Z)", t, re.S)
    if not m:
        print(f"rfc{n}: no Terminology section")
        continue
    sec = m.group(1)
    terms = re.findall(r"(?m)^\s*(?:o\s+)?([A-Z][A-Za-z0-9 /-]{2,40})\s*:\s*(.+)", sec)
    out[n] = [{"term": k.strip(), "def": v.strip()[:200]} for k, v in terms[:50]]
    print(f"rfc{n}: {len(out[n])} terms")
json.dump(out, open("domain_terms.json", "w"), indent=2)
print(f"wrote domain_terms.json ({sum(map(len, out.values()))} terms)")
