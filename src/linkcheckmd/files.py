from pathlib import Path
import typing as T


def get(path: Path, ext: str, recurse: bool = False) -> T.Iterable[Path]:
    """
    yield files in path with suffix ext. Optionally, recurse directories.
    """

    path = Path(path).expanduser().resolve()

    if path.is_dir():
        for p in path.iterdir():
            if p.is_file() and p.suffix == ext:
                yield p
            elif p.is_dir():
                if recurse:
                    yield from get(p, ext, recurse)
                else:
                    # Hugo PageResource
                    for n in ("index.md", "_index.md"):
                        if (p / n).is_file():
                            yield p / n
                            break
    elif path.is_file():
        yield path
    else:
        raise FileNotFoundError(path)
