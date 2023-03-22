from __future__ import annotations
import re
import typing as T
from pathlib import Path
import warnings
import asyncio
import itertools
import logging

import aiohttp

from . import files

# tuples, not lists

EXC = (
    aiohttp.client_exceptions.ClientConnectorError,
    aiohttp.client_exceptions.ServerDisconnectedError,
)
OKE = asyncio.TimeoutError
TIMEOUT = 10


async def check_urls(
    path: Path,
    regex: str,
    ext: str,
    hdr: dict[str, str] = None,
    method: str = "get",
    recurse: bool = False,
    ssl_verify: bool = True,
) -> list[tuple[str, str, T.Any]]:

    glob = re.compile(regex)

    tasks = [
        check_url(fn, glob, ext, hdr, method=method, ssl_verify=ssl_verify)
        for fn in files.get(path, ext, recurse)
    ]

    warnings.simplefilter("ignore")

    urls = await asyncio.gather(*tasks)

    warnings.resetwarnings()

    # this is per aiohttp manual, when using HTTPS SSL sites, just before closing
    # the event loop, do a 250ms sleep (not for each site)
    await asyncio.sleep(0.250)

    return list(itertools.chain(*urls))  # flatten list of lists


async def check_url(
    fn: Path,
    glob,
    ext: str,
    hdr: dict[str, str] = None,
    *,
    method: str = "get",
    ssl_verify: bool = True,
) -> list[tuple[str, str, T.Any]]:

    urls = glob.findall(fn.read_text(errors="ignore"))
    logging.debug(fn.name, " ".join(urls))
    bad: list[tuple[str, str, T.Any]] = []

    timeout = aiohttp.ClientTimeout(total=TIMEOUT)

    for url in urls:
        if ext == ".md":
            url = url[1:-1]
        try:
            # anti-crawling behavior doesn't like .head() method--.get() is slower but avoids lots of false positives
            async with aiohttp.ClientSession(
                headers=hdr, timeout=timeout, connector=aiohttp.TCPConnector(ssl=ssl_verify)
            ) as session:
                if method == "get":
                    async with session.get(url, allow_redirects=True) as response:
                        code = response.status
                elif method == "head":
                    async with session.head(url, allow_redirects=True) as response:
                        code = response.status
                else:
                    raise ValueError(f"Unknown retreive method {method}")
        except OKE:
            continue
        except EXC as e:
            bad.append((fn.name, url, e))  # e, not str(e)
            print("\n", bad[-1])
            continue

        if code != 200:
            bad.append((fn.name, url, code))
            print("\n", bad[-1])
        else:
            logging.info(f"OK: {url:80s}")

    return bad
