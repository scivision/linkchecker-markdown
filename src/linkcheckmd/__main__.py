"""
check links in Markdown files (as used for Static site generation)

linkcheckMarkdown ~/myHugosite/content/posts github.com

linkcheckMarkdown ~/myJekyllsite/_posts
"""

import argparse
import logging
import time

from .base import check_links


def main():
    p = argparse.ArgumentParser(description="check links in markdown sites")
    p.add_argument("path", help="path(s) to Markdown files", nargs="*")
    p.add_argument(
        "-d",
        "--domain",
        help="check only links to this domain (say github.com without https etc.)",
        default=None,
    )
    p.add_argument("-e", "--ext", help="file extension to scan", default=".md")
    p.add_argument(
        "-m",
        "--method",
        choices=["get", "head"],
        help="head is faster but gives false positives. Get is reliable but slower",
        default="get",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--sync", help="don't use asyncio", action="store_true")
    p.add_argument("-local", help="only check local files", action="store_true")
    p.add_argument("-r", "--recurse", help="recurse directories under path", action="store_true")
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.INFO)

    tic = time.monotonic()
    bad = check_links(
        P.path,
        ext=P.ext,
        domain=P.domain,
        method=P.method,
        use_async=not P.sync,
        local=P.local,
        recurse=P.recurse,
    )

    print(f"{time.monotonic() - tic:0.3} seconds to check links")

    if bad:
        # using 22 following cURL
        # https://everything.curl.dev/usingcurl/returns
        raise SystemExit(22)


if __name__ == "__main__":
    main()
