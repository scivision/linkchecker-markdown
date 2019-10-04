import requests
import re
import typing
from pathlib import Path
import warnings
import urllib3

TIMEOUT = 10
RETRYCODES = (400, 404, 405, 503)
# multiple exceptions must be tuples, not lists in general
OKE = requests.exceptions.TooManyRedirects  # FIXME: until full browswer like Arsenic implemented
EXC = (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError)

"""
synchronous routines
"""


def check_urls(
    flist: typing.Iterable[Path],
    pat: str,
    ext: str = ".md",
    hdr: typing.Dict[str, str] = None,
    verifycert: bool = False,
    verbose: bool = False,
) -> typing.List[typing.Tuple[str, str, typing.Any]]:

    glob = re.compile(pat)

    warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    with requests.Session() as sess:
        if hdr:
            sess.headers.update(hdr)
            sess.max_redirects = 5
        # %% loop
        bad: typing.List[typing.Tuple[str, str, typing.Any]] = []

        for fn in flist:
            bad.extend(check_url(fn, glob, ext, sess, hdr, verifycert, verbose))

    warnings.resetwarnings()
    return bad


def check_url(
    fn: Path, glob, ext: str, sess, hdr: typing.Dict[str, str] = None, verifycert: bool = False, verbose: bool = False
) -> typing.List[typing.Tuple[str, str, typing.Any]]:

    urls = glob.findall(fn.read_text(errors="ignore"))

    bad: typing.List[typing.Tuple[str, str, typing.Any]] = []

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
                    print("\n", bad[-1])
                    continue
        except OKE:
            continue
        except EXC as e:
            if retry(url, hdr, verifycert):
                continue
            bad += [(fn.name, url, str(e))]
            print("\n", bad[-1])
            continue

        code = R.status_code
        if code != 200:
            bad += [(fn.name, url, code)]
            print("\n", bad[-1])
        else:
            if verbose:
                print(f"OK: {url:80s}", end="\r")

    return bad


def retry(url: str, hdr: typing.Dict[str, str] = None, verifycert: bool = False) -> bool:
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
