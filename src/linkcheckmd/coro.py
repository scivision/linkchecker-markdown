import re
import typing as T
from pathlib import Path
import warnings
import asyncio
import itertools
import logging

import requests
import aiohttp

# tuples, not lists

EXC = (
    aiohttp.client_exceptions.ClientConnectorError,
    aiohttp.client_exceptions.ServerDisconnectedError,
    requests.exceptions.ConnectionError,
    requests.exceptions.ReadTimeout,
)
OKE = asyncio.TimeoutError
TIMEOUT = 10


async def check_urls(
    flist: T.Iterable[Path],
    regex: str,
    ext: str,
    hdr: T.Dict[str, str] = None,
    method: str = "get",
) -> T.List[T.Tuple[str, str, T.Any]]:

    glob = re.compile(regex)

    tasks = [check_url(fn, glob, ext, hdr, method=method) for fn in flist]

    warnings.simplefilter("ignore")

    urls = await asyncio.gather(*tasks)

    warnings.resetwarnings()

    return list(itertools.chain(*urls))  # flatten list of lists


async def check_url(
    fn: Path, glob, ext: str, hdr: T.Dict[str, str] = None, *, method: str = "get"
) -> T.List[T.Tuple[str, str, T.Any]]:

    urls = glob.findall(fn.read_text(errors="ignore"))
    logging.debug(fn.name, " ".join(urls))
    bad = []  # type: T.List[T.Tuple[str, str, T.Any]]

    for url in urls:
        if ext == ".md":
            url = url[1:-1]
        try:
            if method == "get":
                # anti-crawling behavior doesn't like .head() method--.get() is slower but avoids lots of false positives
                R = requests.get(
                    url, allow_redirects=True, timeout=TIMEOUT, headers=hdr, verify=False
                )
            elif method == "head":
                R = requests.head(
                    url, allow_redirects=True, timeout=TIMEOUT, headers=hdr, verify=False
                )
            else:
                raise ValueError(f"unknown method {method}")
        except OKE:
            continue
        except EXC as e:
            bad.append((fn.name, url, e))  # e, not str(e)
            print("\n", bad[-1])
            continue

        code = R.status_code
        if code != 200:
            bad.append((fn.name, url, code))
            print("\n", bad[-1])
        else:
            logging.info(f"OK: {url:80s}")

    return bad
