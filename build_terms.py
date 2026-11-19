import re, json, urllib.request


def get(url):
    return (
        urllib.request.urlopen(url, timeout=30).read().decode("utf-8", errors="ignore")
    )


# 1. Normative keywords: auto-extract from BCP14 boilerplate (RFC2119 + RFC8174)
t2119 = get("https://www.rfc-editor.org/rfc/rfc2119.txt")
t8174 = get("https://www.rfc-editor.org/rfc/rfc8174.txt")
# Boilerplate lists keywords in quotes - parse both, union
quoted = set(re.findall(r'"([A-Z]+(?: [A-Z]+)?)"', t2119 + t8174))
# Keep only real BCP14 keywords (filter noise like OLD/NEW/END)
allow = {
    "MUST",
    "MUST NOT",
    "REQUIRED",
    "SHALL",
    "SHALL NOT",
    "SHOULD",
    "SHOULD NOT",
    "RECOMMENDED",
    "NOT RECOMMENDED",
    "MAY",
    "OPTIONAL",
}
terms = sorted(quoted & allow)
out = {
    "source": ["rfc2119.txt", "rfc8174.txt"],
    "generated_by": "build_terms.py (no hand-craft)",
    "keywords": terms,
}
print(json.dumps(out, indent=2))
with open("rfc_terms.json", "w") as f:
    json.dump(out, f, indent=2)
