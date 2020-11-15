"""
check links in Markdown files (as used for Static site generation)

linkcheckMarkdown ~/myHugosite/content/posts github.com

linkcheckMarkdown ~/myJekyllsite/_posts
"""

import argparse
import logging
import time

from . import check_remotes, check_local


def main():
    # http://www.useragentstring.com
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"

    p = argparse.ArgumentParser(description="check links in markdown sites")
    p.add_argument("path", help="path to Markdown files")
    p.add_argument(
        "domain",
        help="check only links to this domain (say github.com without https etc.)",
        nargs="?",
    )
    p.add_argument(
        "-a", "--useragent", help="user agent to use instead of default", default=user_agent
    )
    p.add_argument("-ext", help="file extension to scan", default=".md")
    p.add_argument(
        "-m",
        "--method",
        choices=["get", "head"],
        help="head is faster but gives false positives. Get is reliable but slower",
        default="get",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--mode", choices=["sync", "coro"], default="coro")
    p.add_argument("-local", help="only check local files", action="store_true")
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.INFO)

    hdr = {"User-Agent": P.useragent}

    for bad in check_local(P.path, ext=P.ext):
        print(bad)

    if not P.local:
        tic = time.monotonic()
        check_remotes(P.path, P.domain, ext=P.ext, mode=P.mode, hdr=hdr, method=P.method)
        print(time.monotonic() - tic, " seconds to check remote links in mode:", P.mode)


if __name__ == "__main__":
    main()
