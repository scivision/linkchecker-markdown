import os
import asyncio

from .base import check_links, check_local, check_remotes

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore
# type ignore needed for non-windows mypy
