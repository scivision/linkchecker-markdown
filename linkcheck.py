#!/usr/bin/env python
"""
check links in Markdown files (as used for Static site generation)
I noted linkchecker program doesn't catch GitHub 404 for example.

python linkcheck.py ~/myHugosite/content/posts github.com

python linkcheck.py ~/myJekyllsite/_posts
"""
import argparse
import logging

from linkcheckmd import run_check

"""
http://www.useragentstring.com
"""
UA = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to Markdown files")
    p.add_argument("domain", help="check only links to this domain (say github.com without https etc.)", nargs="?")
    p.add_argument("-a", "--useragent", help="user agent to use instead of default", default=UA)
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
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.INFO)

    hdr = {"User-Agent": P.useragent}

    run_check(P.path, P.domain, ext=P.ext, mode=P.mode, hdr=hdr, method=P.method)


if __name__ == "__main__":
    main()
