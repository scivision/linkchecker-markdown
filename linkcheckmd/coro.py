from aiohttp_requests import requests
import aiohttp
import re
import typing
from pathlib import Path
import warnings
import asyncio
import urllib3
from . import TIMEOUT

# multiple exceptions must be tuples, not lists in general
OKE = (asyncio.TimeoutError,)  # FIXME: until full browswer like Arsenic implemented
EXC = (aiohttp.client_exceptions.ClientConnectorError, aiohttp.client_exceptions.ServerDisconnectedError)


async def check_pages(flist: typing.Iterator[Path], pat: str, ext: str, hdr: typing.Dict[str, str] = None, verbose: bool = False):

    glob = re.compile(pat)

    tasks = [check_url(fn, glob, ext, hdr, verbose) for fn in flist]

    warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    await asyncio.gather(*tasks)

    warnings.resetwarnings()


async def check_url(
    fn: Path, glob, ext: str, hdr: typing.Dict[str, str] = None, verbose: bool = False
) -> typing.List[typing.Tuple[str, str, typing.Any]]:

    urls = glob.findall(fn.read_text(errors="ignore"))

    bad = []  # type: typing.List[typing.Tuple[str, str, typing.Any]]

    for url in urls:
        if ext == ".md":
            url = url[1:-1]
        try:
            R = await requests.get(url, allow_redirects=True, timeout=TIMEOUT, headers=hdr, verify_ssl=False)
        except OKE:
            continue
        except EXC as e:
            bad += [(fn.name, url, e)]  # e, not str(e)
            print("\n", bad[-1])
            continue

        code = R.status
        if code != 200:
            bad += [(fn.name, url, code)]
            print("\n", bad[-1])
        else:
            if verbose:
                print("OK: {:80s}".format(url), end="\r")

    return bad
