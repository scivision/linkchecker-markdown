from aiohttp_requests import requests
import aiohttp
import re
from typing import Sequence, Dict, List, Tuple, Any
from pathlib import Path
import warnings
import asyncio
import urllib3
from . import TIMEOUT

# multiple exceptions must be tuples, not lists in general
OKE = (asyncio.TimeoutError,)  # FIXME: until full browswer like Arsenic implemented
EXC = (aiohttp.client_exceptions.ClientConnectorError, aiohttp.client_exceptions.ServerDisconnectedError)


def main(flist: Sequence[Path], pat: str, ext: str = '.md',
         hdr: Dict[str, str] = None, verbose: bool = False):

    glob = re.compile(pat)

    if hasattr(asyncio, 'run'):  # python >= 3.7
        asyncio.run(arbiter(flist, glob, ext, hdr, verbose))
    else:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(arbiter(flist, glob, ext, hdr, verbose))
        loop.close()


async def arbiter(flist, glob, ext: str,
                  hdr: Dict[str, str] = None, verbose: bool = False):

    tasks = [check_url(fn, glob, ext, hdr, verbose) for fn in flist]

    warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

    await asyncio.gather(*tasks)

    warnings.resetwarnings()


async def check_url(fn: Path, glob, ext: str,
                    hdr: Dict[str, str] = None,
                    verbose: bool = False) -> List[Tuple[str, str, Any]]:
    urls = glob.findall(fn.read_text())

    bad = []  # type: List[Tuple[str, str, Any]]

    for url in urls:
        if ext == ".md":
            url = url[1:-1]
        try:
            R = await requests.get(url, allow_redirects=True, timeout=TIMEOUT, headers=hdr, verify_ssl=False)
        except OKE:
            continue
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
                print('OK: {:80s}'.format(url), end='\r')

    return bad
