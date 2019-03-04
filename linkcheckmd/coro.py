from aiohttp_requests import requests
import aiohttp
import re
from typing import Sequence, Dict, List, Tuple, Any
from pathlib import Path
import warnings
import asyncio
import urllib3
from . import TIMEOUT

EXC = (asyncio.TimeoutError, aiohttp.client_exceptions.ClientConnectorError)


def main(flist: Sequence[Path], pat: str, ext: str = '.md',
         hdr: Dict[str, str] = None, verbose: bool = False):

    glob = re.compile(pat)

    asyncio.run(arbiter(flist, glob, ext, hdr, verbose))


async def arbiter(flist, glob, ext: str,
                  hdr: Dict[str, str] = None, verbose: bool = False):

    tasks = [check_url(fn, glob, ext, hdr, verbose) for fn in flist]

    warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    asyncio.run(await asyncio.gather(*tasks))

    warnings.resetwarnings()


async def check_url(fn: Path, glob, ext: str,
                    hdr: Dict[str, str] = None,
                    verbose: bool = False) -> List[Tuple[str, str, Any]]:
    urls = glob.findall(fn.read_text())

    bad: List[Tuple[str, str, Any]] = []

    for url in urls:
        if ext == ".md":
            url = url[1:-1]
        try:
            R = await requests.get(url, allow_redirects=True, timeout=TIMEOUT, headers=hdr, verify_ssl=False)
        except EXC as e:
            bad += [(fn.name, url, e)]  # e, not str(e)
            print('\n', bad[-1])
            continue

        code = R.status
        if code != 200:
            bad += [(fn.name, url, code)]
            print('\n', bad[-1])
        else:
            if verbose:
                print(f'OK: {url:80s}', end='\r')

    return bad
