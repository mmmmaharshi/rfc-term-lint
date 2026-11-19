# Hosted MCP distribution

Plug-and-play means zero new tools, so we ship the checker as a hosted server at a public URL instead of a local process or installable package. Draft privacy rules out sending text to a server, but the tool targets published papers only, and we accept running free-tier hosting with rate limits before keys.

## Considered Options

- `uvx` from PyPI: still a new tool to install, fails the bar.
- Per-OS binaries: zero tools but per-OS builds, signing warnings, manual updates.
- npm wrapper: same install burden in a different runtime.
