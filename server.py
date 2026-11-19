"""rfc-term-lint MCP server - minimal. Run: python server.py (stdio)"""

import json, re
from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("rfc-term-lint")
TERMS = json.loads(Path(__file__).with_name("rfc_terms.json").read_text())["keywords"]
# shortcut: meanings condensed from RFC2119 S1-5, upgrade when extractor parses sections
MEANINGS = {
    "MUST": "absolute requirement",
    "MUST NOT": "absolute prohibition",
    "REQUIRED": "absolute requirement",
    "SHALL": "absolute requirement",
    "SHALL NOT": "absolute prohibition",
    "SHOULD": "recommendation, weigh before ignoring",
    "SHOULD NOT": "recommendation against",
    "RECOMMENDED": "recommendation",
    "NOT RECOMMENDED": "recommendation against",
    "MAY": "truly optional",
    "OPTIONAL": "truly optional",
}
KW = sorted(TERMS, key=len, reverse=True)
KW_RE = re.compile(r"\b(" + "|".join(map(re.escape, KW)) + r")\b")
LOWER_RE = re.compile(
    r"(?<![A-Z])\b(must|should|may|shall|required|recommended|optional)\b(?![A-Z])"
)


@mcp.tool()
def search_rfc_term(term: str) -> dict:
    """Look up a BCP14 keyword. term: e.g. MUST, SHOULD, MAY"""
    t = term.strip().upper()
    if t in MEANINGS:
        return {"term": t, "meaning": MEANINGS[t], "source": "BCP14 (RFC2119+RFC8174)"}
    return {"term": t, "found": False, "keywords": TERMS}


@mcp.tool()
def evaluate_text(text: str) -> dict:
    """Flag normative keywords + ambiguous lowercase usage."""
    flags = [
        {"term": m.group(0), "pos": m.start(), "note": MEANINGS.get(m.group(0), "")}
        for m in KW_RE.finditer(text)
    ]
    vague = [
        {
            "word": m.group(0),
            "pos": m.start(),
            "suggest": "uppercase per BCP14 if normative, else reword (e.g. 'is expected to')",
        }
        for m in LOWER_RE.finditer(text)
    ]
    return {
        "normative_hits": flags,
        "ambiguous_lowercase": vague,
        "has_boilerplate": "RFC 2119" in text or "BCP 14" in text,
    }


@mcp.tool()
def suggest_fix(paragraph: str) -> dict:
    """Suggest BCP14-precise rewrite for one paragraph."""
    fixes = []
    for m in LOWER_RE.finditer(paragraph):
        fixes.append(
            {
                "at": m.start(),
                "from": m.group(0),
                "to": m.group(0).upper(),
                "why": "normative intent -> UPPERCASE per BCP14, else reword to 'is expected to'",
            }
        )
    if re.search(r"(?i)\bmay\s+optionally\b", paragraph):
        fixes.append(
            {
                "from": "may optionally",
                "to": "MAY",
                "why": "'optionally' is redundant with MAY",
            }
        )
    if re.search(r"(?i)\betc\.?\b", paragraph):
        fixes.append(
            {
                "from": "etc.",
                "to": "enumerate explicitly",
                "why": "RFC style forbids open-ended lists in normative text",
            }
        )
    return {
        "fixes": fixes,
        "needs_boilerplate": "BCP 14" not in paragraph
        and bool(KW_RE.search(paragraph)),
    }


if __name__ == "__main__":
    mcp.run()
