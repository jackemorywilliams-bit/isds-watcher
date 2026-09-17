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

Two properties of the relay that a request must be designed around. Both were learned
the expensive way, on 2026-09-17, when two of ten rows could not have answered the
question they were written for and seven more came back uninterpretable.

- **A `find` sees only VISIBLE PROSE.** `excerpt_of` removes `<script>` and `<style>`
  element bodies and then every remaining tag *before* the search runs
  (`scripts/fetch_relay.py:78-79, 126-131`). Markup, attributes, script contents,
  endpoints and query parameters are unreachable to any `find`, so a null on a term
  like `facet` or `json` says nothing about whether such machinery exists on the page.
- **EVERY URL EXPECTED TO PRODUCE A NULL NEEDS A COMPANION CONTROL ROW ON THE SAME URL
  IN THE SAME RUN.** When a `find` misses, `excerpt_of` returns the empty string rather
  than a head excerpt (`:132-133`), so a null row hands back no window at all and cannot
  show that the tag-strip yielded any prose from that document. Without a control row
  that hits, a null is uninterpretable: it cannot be told apart from an instrument
  failure. Rows sharing a URL with different `find` values are separate fetches and cost
  one slot each — a negative belongs to the byte-stream it was obtained on, and the
  control is what establishes that stream answered.

<!-- graph:auto start -->
Map: [[Evidence Ledger]]
<!-- graph:auto end -->
