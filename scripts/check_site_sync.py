#!/usr/bin/env python3
"""Fail if the generated website (docs/) is out of sync with its source.

The website is built from source by scripts/build_site.py (METHODOLOGY.md, the
digest folders, and the site templates). It is easy to edit a source file and
forget to rebuild, leaving the published site stale — this has bitten the project
repeatedly. This check rebuilds the site and fails if docs/ would change in any
way OTHER than the wall-clock "Site built ..." footer stamp, which legitimately
differs on every build and must be ignored.

Used by .github/workflows/site-sync.yml (the PR gate) and runnable locally:
    python scripts/check_site_sync.py
"""

from __future__ import annotations

import subprocess
import sys

STAMP_MARKER = "footer-build"  # the wall-clock build stamp; differs every build


def main() -> int:
    build = subprocess.run(
        [sys.executable, "scripts/build_site.py"], capture_output=True, text=True)
    if build.returncode != 0:
        print("build_site.py failed:\n" + build.stdout + build.stderr)
        return 1

    diff = subprocess.run(
        ["git", "diff", "--", "docs/"], capture_output=True, text=True).stdout

    offending = [
        ln for ln in diff.splitlines()
        if ln[:1] in "+-"
        and not ln.startswith(("+++", "---"))
        and STAMP_MARKER not in ln
    ]
    if offending:
        print("ERROR: docs/ is out of sync with its source.")
        print("The website was not rebuilt after a source change. Fix with:")
        print("    python scripts/build_site.py   # then commit the docs/ changes")
        print("\nContent changes detected (excluding the build stamp):")
        print("\n".join(offending[:80]))
        return 1

    print("OK: docs/ is in sync with source (only the build stamp differs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
