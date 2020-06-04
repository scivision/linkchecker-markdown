"""
for asyncio.open_connection(), we do NOT use ProactorEventLoop for Windows.
Hence the use of "use_run"
"""
import os
import sys
import asyncio


def runner(fun, *args):
    """
    Generic asyncio.run() equivalent for Python >= 3.5
    """
    use_run = (os.name == "nt" and (3, 8) > sys.version_info >= (3, 7)) or (
        os.name != "nt" and sys.version_info >= (3, 7)
    )

    if use_run:
        result = asyncio.run(fun(*args))
    else:  # 3.8, 3.6, 3.5
        loop = asyncio.SelectorEventLoop()
        result = loop.run_until_complete(fun(*args))
        loop.close()
    return result
