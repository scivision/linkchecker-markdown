from __future__ import annotations
from pathlib import Path
import typing as T
import logging
import re
import asyncio

from .coro import check_urls
from . import files

# http://www.useragentstring.com
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"


def check_links(
    path: Path,
    domain: str = None,
    *,
    ext: str,
    hdr: dict[str, str] = None,
    method: str = "get",
    use_async: bool = True,
    local: bool = False,
    recurse: bool = False,
    ssl_verify: bool = True,
) -> T.Iterable[tuple]:

    if local and recurse:
        logging.error("'recurse' currently works only for remote links.")

    for missing_file in check_local(path, ext=ext):
        # to get an iterable/list of these, call check_local directly from your program
        print(missing_file)

    bad = None
    if not local:
        bad = check_remotes(
            path,
            domain,
            ext=ext,
            hdr=hdr,
            method=method,
            use_async=use_async,
            recurse=recurse,
            ssl_verify=ssl_verify,
        )

    return bad


def check_local(path: Path, ext: str) -> T.Iterable[tuple[str, str]]:
    """check internal links of Markdown files
    this is a simple static analysis; only plain filename references are handled.
    """

    regex = r"\]\(([=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+)\)"
    glob = re.compile(regex)

    path = Path(path).resolve().expanduser()  # must have .resolve()

    for fn in files.get(path, ext):
        # print(fn)
        urls = glob.findall(fn.read_text(errors="ignore"))

        for url in urls:
            if url[0] == "#":
                continue

            stem = url.strip("/")

            if not url[0] == "/":
                if {"/", "."}.intersection(stem):
                    continue
                yield fn.name, url
                continue

            if {"/", "."}.intersection(stem):
                continue

            if not (
                (path / (stem + ext)).is_file()
                or (path.parent / (stem + ext)).is_file()
                or (path / stem).is_dir()
            ):
                yield fn.name, url


def check_remotes(
    path: Path,
    domain: str,
    *,
    ext: str,
    hdr: dict[str, str] = None,
    method: str = "get",
    use_async: bool = True,
    recurse: bool = False,
    ssl_verify: bool = True,
) -> list[tuple[str, str, T.Any]]:
    if domain:
        pat = "https?://" + domain + r"[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]*"
    else:
        pat = r"https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"

    if ext == ".md":
        pat = r"\(" + pat + r"\)"

    logging.debug(f"regex {pat}")

    if not hdr:
        hdr = {"User-Agent": USER_AGENT}

    # %% session
    if use_async:
        urls = asyncio.run(
            check_urls(
                path,
                regex=pat,
                ext=ext,
                hdr=hdr,
                method=method,
                recurse=recurse,
                ssl_verify=ssl_verify,
            )
        )
    else:
        from .sync import check_urls as sync_urls

        urls = sync_urls(path, regex=pat, ext=ext, hdr=hdr, recurse=recurse, ssl_verify=ssl_verify)

    return urls
