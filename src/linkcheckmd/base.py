from pathlib import Path
import typing as T
import logging

from .runner import runner
from .coro import check_urls as coro_urls
from .sync import check_urls


def check_remotes(
    path: Path,
    domain: str,
    *,
    ext: str,
    mode: str,
    hdr: T.Dict[str, str] = None,
    method: str = "get",
) -> T.List[T.Tuple[str, str, T.Any]]:
    if domain:
        pat = "https?://" + domain + r"[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]*"
    else:
        pat = r"https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"

    if ext == ".md":
        pat = r"\(" + pat + r"\)"

    logging.debug(f"regex {pat}")

    path = Path(path).expanduser()

    if path.is_dir():
        flist = iter(path.glob("*" + ext))
    elif path.is_file():
        flist = iter([path])
    else:
        raise FileNotFoundError(path)
    # %% session
    if mode == "coro":
        urls = runner(coro_urls, flist, pat, ext, hdr, method)
    elif mode == "sync":
        urls = check_urls(flist, pat, ext, hdr)
    return urls
