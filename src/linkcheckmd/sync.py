from __future__ import annotations
import requests
import re
import typing as T
from pathlib import Path
import warnings
import urllib3
import logging

from . import files

TIMEOUT = 10
RETRYCODES = (400, 404, 405, 503)
# multiple exceptions must be tuples, not lists in general

OKE = requests.exceptions.TooManyRedirects
# FIXME: until full browser like Arsenic implemented

EXC = (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError)

"""
synchronous routines
"""


def check_urls(
    path: Path,
    regex: str,
    ext: str = ".md",
    hdr: dict[str, str] | None = None,
    ssl_verify: bool = False,
    recurse: bool = False,
    exclude_domains: list[str] | None = None,
) -> list[tuple[Path, str, T.Any]]:

    bads: list[tuple[Path, str, T.Any]] = []

    glob = re.compile(regex)

    warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    with requests.Session() as sess:
        if hdr:
            sess.headers.update(hdr)
            sess.max_redirects = 5
        # %% loop
        for fn in files.get(path, ext, recurse):
            for bad in check_url(fn, glob, ext, sess, hdr, ssl_verify, exclude_domains):
                print("\n", bad[0], bad[1], bad[2])
                bads.append(bad)

    warnings.resetwarnings()

    return bads


def check_url(
    fn: Path,
    glob,
    ext: str,
    sess,
    hdr: dict[str, str] | None = None,
    ssl_verify: bool = False,
    exclude_domains: list[str] | None = None,
) -> T.Iterable[tuple[Path, str, T.Any]]:

    urls = glob.findall(fn.read_text(errors="ignore"))

    for url in urls:
        if ext == ".md":
            url = url[1:-1]
        
        # Skip URLs that contain excluded domains
        if exclude_domains:
            should_skip = False
            for domain in exclude_domains:
                if domain.lower() in url.lower():
                    should_skip = True
                    break
            if should_skip:
                continue
        try:
            R = sess.head(url, allow_redirects=True, timeout=TIMEOUT, verify=ssl_verify)
            if R.status_code in RETRYCODES:
                if retry(url, hdr, ssl_verify):
                    continue
                else:
                    yield fn, url, R.status_code
                    continue
        except OKE:
            continue
        except EXC as e:
            if retry(url, hdr, ssl_verify):
                continue
            yield fn, url, str(e)
            continue

        code = R.status_code
        if code != 200:
            yield fn, url, code
        else:
            logging.info(f"OK: {url:80s}")


def retry(url: str, hdr: dict[str, str] | None = None, ssl_verify: bool = False) -> bool:
    ok = False

    try:
        # anti-crawling behavior doesn't like .head() method--.get() is slower but avoids lots of false positives
        with requests.get(
            url,
            allow_redirects=True,
            timeout=TIMEOUT,
            verify=ssl_verify,
            headers=hdr,
            stream=True,
        ) as stream:
            Rb = next(stream.iter_lines(80), None)
            # if Rb is not None and 'html' in Rb.decode('utf8'):
            if Rb and len(Rb) > 10:
                ok = True
    except EXC:
        pass

    return ok
