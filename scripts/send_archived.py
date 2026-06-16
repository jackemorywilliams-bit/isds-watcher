"""Re-send one archived digest exactly as it was finalized.

Reads digests/<FOLDER>/index.html (the finalized email body) and meta.json (the
reconciled counts), then emails it verbatim to config.RECIPIENTS. Useful for
delivering a specific run's digest to the inbox without re-running the pipeline.

Usage:
    python scripts/send_archived.py [FOLDER]
FOLDER defaults to $DIGEST_FOLDER, else the most recent archived run.
"""
import datetime
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config  # noqa: E402
from src.email_send import send_digest  # noqa: E402


def _resolve_folder() -> str:
    arg = sys.argv[1] if len(sys.argv) > 1 else os.getenv("DIGEST_FOLDER", "")
    if arg:
        return arg if os.path.isdir(arg) else os.path.join("digests", arg)
    folders = sorted(glob.glob("digests/*_ISDS-Thematic-Watch"))
    if not folders:
        sys.exit("no archived digests found")
    return folders[-1]


def main() -> int:
    folder = _resolve_folder()
    index_html = os.path.join(folder, "index.html")
    if not os.path.exists(index_html):
        sys.exit(f"{index_html} not found")
    html = open(index_html, encoding="utf-8").read()

    meta = {}
    meta_path = os.path.join(folder, "meta.json")
    if os.path.exists(meta_path):
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except (ValueError, OSError):
            meta = {}

    date_str = meta.get("date") or os.path.basename(folder).split("_")[0]
    matches = int(meta.get("matches", 0) or 0)
    leads = int(meta.get("watch_list_leads", 0) or 0)
    screened = int(meta.get("screened", 0) or 0)
    subject = (
        f"ISDS Thematic Watch — {date_str} "
        f"({matches} match{'' if matches == 1 else 'es'} · "
        f"{leads} watch-list lead{'' if leads == 1 else 's'}, "
        f"{screened} screened)"
    )

    cfg = config.load_config()
    ok = send_digest(html, subject, cfg)
    print(f"folder:    {folder}")
    print(f"subject:   {subject}")
    print(f"recipients:{config.RECIPIENTS}")
    print(f"sent:      {ok}  ({datetime.datetime.now(datetime.timezone.utc).isoformat()})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
