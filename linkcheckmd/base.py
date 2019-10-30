from pathlib import Path
from .runner import runner
import typing

from .coro import check_urls as coro_urls
from .sync import check_urls


def run_check(
    path: Path, domain: str, ext: str, mode: str, verbose: bool = False
) -> typing.List[typing.Tuple[str, str, typing.Any]]:
    if domain:
        pat = "https?://" + domain + r"[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]*"
    else:
        pat = r"https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[=a-zA-Z0-9\_\/\?\&\%\+\#\.\-]+"

    if ext == ".md":
        pat = r"\(" + pat + r"\)"

    if verbose:
        print(pat)

    path = Path(path).expanduser()

    if path.is_dir():
        flist = iter(path.glob("*" + ext))
    elif path.is_file():
        flist = iter([path])
    else:
        raise FileNotFoundError(path)
    # %% session
    """
    http://www.useragentstring.com
    """
    hdr = {"User-Agent": ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0")}

    if mode == "coro":
        urls = runner(coro_urls, flist, pat, ext, hdr, verbose)
    elif mode == "sync":
        urls = check_urls(flist, pat, ext, hdr, verbose=verbose)
    return urls
