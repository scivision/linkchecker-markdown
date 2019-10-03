#!/usr/bin/env python
"""
check links in Markdown files (as used for Static site generation)
I noted linkchecker program doesn't catch GitHub 404 for example.

python linkcheck.py ~/myHugosite/content/posts github.com

python linkcheck.py ~/myJekyllsite/_posts
"""
from pathlib import Path
from argparse import ArgumentParser
from linkcheckmd.runner import runner
from linkcheckmd.coro import check_pages


def main():
    p = ArgumentParser()
    p.add_argument("path", help="path to Markdown files")
    p.add_argument("domain", help="check only links to this domain (juse say github.com without https etc.)", nargs="?")
    p.add_argument("-ext", help="file extension to scan", default=".md")
    p.add_argument("-v", "--verbose", action="store_true")
    p = p.parse_args()

    if p.domain:
        pat = "https?://" + p.domain + r"[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"
    else:
        pat = r"https?://[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"

    if p.ext == ".md":
        pat = r"\(" + pat + r"\)"

    path = Path(p.path).expanduser()

    if path.is_dir():
        flist = path.glob("*" + p.ext)
    elif path.is_file():
        flist = [path]
    else:
        raise FileNotFoundError(path)
    # %% session
    """
    http://www.useragentstring.com
    """
    hdr = {"User-Agent": ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0")}

    runner(check_pages, flist, pat, p.ext, hdr, p.verbose)


if __name__ == "__main__":
    main()
