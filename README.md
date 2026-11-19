# rfc-term-lint MCP

Lints research-paper wording against BCP 14 (RFC 2119 + RFC 8174) keywords.

## Use the hosted server

No install. Point your MCP client at the public URL (streamable HTTP):

```json
{ "mcpServers": { "rfc-term-lint": { "url": "https://<host>/mcp" } } }
```

## Self-host with Docker

```sh
docker build -t rfc-term-lint .
docker run -p 8000:8000 rfc-term-lint
```

`TRANSPORT=stdio` (default) keeps local stdio mode; `streamable-http` serves
`POST /mcp` on `HOST`/`PORT` (defaults `0.0.0.0`/`8000`).

## Local dev

`uv sync && uv run server.py` (stdio). Roadmap: per-IP rate limits before any
API keys (see `docs/adr/0001-hosted-mcp-distribution.md`).

## Tools

- `search_rfc_term` — meaning of a MUST/SHOULD/MAY keyword
- `evaluate_text` — flags normative hits + ambiguous lowercase usage
- `suggest_fix` — rewrite suggestions for one paragraph

## Data

- `python build_terms.py` regenerates `rfc_terms.json` from rfc-editor.org
- `python ingest_domain.py 9110` extracts Terminology sections to `domain_terms.json`
- `python test_server.py` runs the 11 behavior checks
