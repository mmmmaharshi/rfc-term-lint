"""Behavior tests for rfc-term-lint. Run: python test_server.py (stdlib only)."""

import server

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"ok - {name}")
    else:
        failed += 1
        print(f"FAIL - {name}")


def raises(fn, *args):
    try:
        fn(*args)
    except (ValueError, SystemExit):
        return True
    return False


# UPPERCASE keyword detected with its meaning
hits = server.evaluate("Server MUST retry.")["normative_hits"]
check("MUST flagged with meaning", any(h["term"] == "MUST" and h["note"] for h in hits))

# Lowercase is ambiguous; UPPERCASE never is
vague = server.evaluate("It should be fast and SHOULD scale.")["ambiguous_lowercase"]
words = [v["word"] for v in vague]
check("lowercase flagged, UPPERCASE not", "should" in words and "SHOULD" not in words)

# Longest match wins: one MUST NOT, not MUST plus NOT
hits = server.evaluate("Client MUST NOT cache.")["normative_hits"]
check("MUST NOT single hit", [h["term"] for h in hits] == ["MUST NOT"])

# Boilerplate detection
check("boilerplate found", server.evaluate("as in BCP 14 [RFC2119]")["has_boilerplate"])
check(
    "boilerplate missing", not server.evaluate("Server MUST retry.")["has_boilerplate"]
)

# Redundant phrasing and open-ended lists
fixes = server.suggest("It may optionally cache errors etc.")["fixes"]
check("may optionally -> MAY", any(f.get("to") == "MAY" for f in fixes))
check("etc. -> enumerate", any("enumerate" in f.get("to", "") for f in fixes))

# Boundary validation
check("None rejected", raises(server.evaluate, None))
check("non-string rejected", raises(server.suggest_fix, 123))
check("oversize rejected", raises(server.evaluate, "x" * (server.MAX_TEXT + 1)))

# Keyword set and meanings stay in sync
check("terms covered by meanings", set(server.TERMS) <= set(server.MEANINGS))

# Terminology parser handles sections and misses
import ingest_domain

sample = "3. Terminology\n\n   Content-Type:  media type of the body\n\n4. Next\n"
check(
    "terminology parsed",
    ingest_domain.parse_terminology(sample)
    == [("Content-Type", "media type of the body")],
)
check("missing section empty", ingest_domain.parse_terminology("no sections") == [])
fixes = server.suggest("you must not cache")["fixes"]
check(
    "must not single fix",
    [f["to"] for f in fixes] == ["MUST NOT"],
)
r = server.lookup_term("content-type")
check("domain term resolves", r.get("source", "").startswith("RFC"))
check(
    "unknown term minimal", server.lookup_term("FOO") == {"term": "FOO", "found": False}
)

# Transport selection
check("stdio default", server.transport_config({}) == ("stdio", {}))
check(
    "http custom",
    server.transport_config(
        {"TRANSPORT": "streamable-http", "HOST": "127.0.0.1", "PORT": "9000"}
    )
    == ("streamable-http", {"host": "127.0.0.1", "port": 9000}),
)
check("bad transport rejected", raises(server.transport_config, {"TRANSPORT": "tcp"}))
check(
    "bad port rejected",
    raises(server.transport_config, {"TRANSPORT": "streamable-http", "PORT": "x"}),
)
t = "Server MUST retry, see RFC 2119."
check(
    "boilerplate rule agrees",
    server.evaluate(t)["has_boilerplate"]
    and not server.suggest(t)["needs_boilerplate"],
)

print(f"{passed} passed, {failed} failed")
raise SystemExit(1 if failed else 0)
