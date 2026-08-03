# Fetch requests

A research session with no network of its own drops a JSON file here and pushes it.
The push fires `.github/workflows/fetch-relay.yml`, which fetches each URL from a
GitHub runner through the project's own `polite_get` and writes the answer to
`analytics/fetch-results/<same-name>.json`.

```json
{ "note": "why this batch exists", "urls": ["https://…", "https://…"] }
```

Rules the relay enforces, so a session cannot bypass them by accident:

- **https only**, and only hosts on the allowlist in `scripts/fetch_relay.py`.
  It retrieves what the sources or the record already identified — it is not a
  discovery channel (METHODOLOGY Part VIII).
- **The reduction travels, never the document.** Results carry url, final url,
  status, content-type, byte length, sha256, timestamp, user-agent and one
  excerpt capped at 400 characters. No third-party body is written anywhere.
- **Every batch carries a control** (`https://example.com/`). If the control
  fails, the batch is VOID and no row may be read as information about its
  resource — the runner was the problem, not the site.
- **Every requested URL gets a row**, including failures. A URL is never
  silently absent, and `no_contact` (we never reached the origin) is never
  recorded as an origin answer.
- Do not put `[skip ci]` in the request commit message — it suppresses the run.
