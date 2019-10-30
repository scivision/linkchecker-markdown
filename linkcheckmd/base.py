from pathlib import Path
from .runner import runner
import typing

from .coro import check_urls as coro_urls
from .sync import check_urls


def run_check(
    path: Path, domain: str, *, ext: str, mode: str, hdr: typing.Dict[str, str] = None, verbose: bool = False
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
    if mode == "coro":
        urls = runner(coro_urls, flist, pat, ext, hdr, verbose)
    elif mode == "sync":
        urls = check_urls(flist, pat, ext, hdr, verbose=verbose)
    return urls
