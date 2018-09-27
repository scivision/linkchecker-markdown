#!/usr/bin/env python
"""
check links in Markdown files (as used for Static site generation)
I noted linkchecker program doesn't catch GitHub 404 for example.
"""
import requests
import re
from pathlib import Path
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('path', help='path to Markdown files')
    p.add_argument('domain', help='check only links to this domain', nargs='?')
    p.add_argument('-ext', help='file extension to scan', default='.md')
    p.add_argument('-v', '--verbose', action='store_true')
    p = p.parse_args()

    if p.domain:
        pat = f"https?:\/\/{p.domain}[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"
    else:
        pat = "https?:\/\/[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"

    if p.ext == ".md":
        pat = f"\({pat}\)"

    glob = re.compile(pat)

    path = Path(p.path).expanduser()

    if path.is_dir():
        flist = path.glob(f"*{p.ext}")
    elif path.is_file():
        flist = [path]
    else:
        raise FileNotFoundError(path)

    bad = []
    for fn in flist:
        urls = glob.findall(fn.read_text())
        for url in urls:
            if p.ext == ".md":
                url = url[1:-1]

            try:
                R = requests.head(url, allow_redirects=True, timeout=10)
            except Exception as e:
                bad += [(fn.name, url, str(e))]
                print('\n', bad[-1])
                continue

            code = R.status_code
            if code != 200:
                bad += [(fn.name, url, code)]
                print('\n', bad[-1])
            else:
                if p.verbose:
                    print(f'OK: {url:80s}', end='\r')

    return bad


if __name__ == '__main__':
    main()
