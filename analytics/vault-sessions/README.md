# Vault sessions

The Obsidian archivist's session records. Every scheduled archivist session writes
one file here, `<YYYY-MM-DD>.md`, and `.github/workflows/vault-log.yml` emails any
record that has no marker in `.sent/`.

What a record should contain, so the email is worth opening:

- **What was audited** this session, and against which commit.
- **Drift found and fixed**, each line citing a commit hash or file path.
- **Escalations** — lines beginning `NEEDS YOU`, `ACTION`, `FOR EMORY`, `TO VERIFY`
  or `AWAITING EMORY` render as marked callouts in the email and are counted in the
  subject line, so Emory can tell from his inbox whether a session needs him.
- **Could not verify** — stated plainly rather than omitted.

The cadence lives with the archivist routine, not with the emailer. The emailer
runs daily and asks only "is anything unsent?", so a session that slips a day is
still delivered, and a session that never ran sends nothing rather than a false
all-clear.

<!-- graph:auto start -->
Map: [[Evidence Ledger]]
<!-- graph:auto end -->
