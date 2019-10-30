#!/usr/bin/env python
"""
check links in Markdown files (as used for Static site generation)
I noted linkchecker program doesn't catch GitHub 404 for example.

python linkcheck.py ~/myHugosite/content/posts github.com

python linkcheck.py ~/myJekyllsite/_posts
"""
import argparse
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
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--mode", help="sync or coro", default="coro")
    P = p.parse_args()

    hdr = {"User-Agent": P.useragent}

    run_check(P.path, P.domain, ext=P.ext, mode=P.mode, hdr=hdr, verbose=P.verbose)


if __name__ == "__main__":
    main()
