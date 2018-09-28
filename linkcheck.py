#!/usr/bin/env python
"""
check links in Markdown files (as used for Static site generation)
I noted linkchecker program doesn't catch GitHub 404 for example.
"""
import requests
import re
from pathlib import Path
from argparse import ArgumentParser
from typing import Dict, List, Tuple, Sequence, Any
import warnings
import urllib3

EXC = (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError)
OKE = requests.exceptions.TooManyRedirects
RETRYCODES = (400, 404, 405, 503)
TIMEOUT = 10


def main():
    p = ArgumentParser()
    p.add_argument('path', help='path to Markdown files')
    p.add_argument('domain', help='check only links to this domain', nargs='?')
    p.add_argument('-ext', help='file extension to scan', default='.md')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('--verify', help='verify certificates', action='store_true')
    p.add_argument('--debug', action='store_true')
    p = p.parse_args()

    if p.domain:
        pat = f"https?://{p.domain}[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"
    else:
        pat = "https?://[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"

    if p.ext == ".md":
        pat = f"\({pat}\)"

    path = Path(p.path).expanduser()

    if path.is_dir():
        flist = path.glob(f"*{p.ext}")
    elif path.is_file():
        flist = [path]
    else:
        raise FileNotFoundError(path)
# %% session
    """
    http://www.useragentstring.com
    this defeats many anti-scrapers
    This program isn't scraping, it just reads the headers,
    but many sites give 4xx errors for an honest user-agent like python-requests/2.19.1

    Also using a Session is more efficent when you revisit the same site.
    """
    hdr = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                       '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')}

    check_urls(flist, pat, p.ext, hdr, p.verify, p.verbose)


def check_urls(flist: Sequence[Path], pat: str, ext: str = '.md',
               hdr: Dict[str, str] = None,
               verifycert: bool = False, verbose: bool = False) -> List[Tuple[str, str, Any]]:

    glob = re.compile(pat)

    warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    with requests.Session() as sess:
        if hdr:
            sess.headers.update(hdr)
            sess.max_redirects = 5
# %% loop
        bad: List[Tuple[str, str, Any]] = []

        for fn in flist:
            bad.extend(check_url(fn, glob, ext, sess, hdr, verifycert, verbose))

    warnings.resetwarnings()
    return bad


def check_url(fn: Path, glob, ext: str, sess, hdr: Dict[str, str] = None,
              verifycert: bool = False, verbose: bool = False) -> List[Tuple[str, str, Any]]:
    urls = glob.findall(fn.read_text())

    bad: List[Tuple[str, str, Any]] = []

    for url in urls:
        if ext == ".md":
            url = url[1:-1]
        try:
            R = sess.head(url, allow_redirects=True, timeout=TIMEOUT, verify=verifycert)
            if R.status_code in RETRYCODES:
                if retry(url, hdr, verifycert):
                    continue
                else:
                    bad += [(fn.name, url, R.status_code)]
                    print('\n', bad[-1])
                    continue
        except OKE:
            continue
        except EXC as e:
            if retry(url, hdr, verifycert):
                continue
            bad += [(fn.name, url, str(e))]
            print('\n', bad[-1])
            continue

        code = R.status_code
        if code != 200:
            bad += [(fn.name, url, code)]
            print('\n', bad[-1])
        else:
            if verbose:
                print(f'OK: {url:80s}', end='\r')

    return bad


def retry(url: str, hdr: Dict[str, str] = None, verifycert: bool = False) -> bool:
    ok = False

    try:
        with requests.get(url, allow_redirects=True, timeout=TIMEOUT, verify=verifycert, headers=hdr, stream=True) as stream:
            Rb = next(stream.iter_lines(80), None)
            # if Rb is not None and 'html' in Rb.decode('utf8'):
            if Rb and len(Rb) > 10:
                ok = True
    except EXC:
        pass

    return ok


if __name__ == '__main__':
    main()
