# rfc-term-lint MCP

Lints research-paper wording against BCP 14 (RFC 2119 + RFC 8174) keywords.

## Run

`uv sync && uv run server.py` (stdio). Or `pip install mcp` + any Python ≥3.10.

## Tools

- `search_rfc_term` — meaning of a MUST/SHOULD/MAY keyword
- `evaluate_text` — flags normative hits + ambiguous lowercase usage
- `suggest_fix` — rewrite suggestions for one paragraph

## Data

- `python build_terms.py` regenerates `rfc_terms.json` from rfc-editor.org
- `python ingest_domain.py 9110` extracts Terminology sections to `domain_terms.json`
- `python test_server.py` runs the 11 behavior checks
