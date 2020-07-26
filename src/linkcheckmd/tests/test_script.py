import subprocess
import pytest
import importlib.resources

import linkcheckmd as lc


def test_local():
    with importlib.resources.path("linkcheckmd.tests", "badlink.md") as file:
        urls = list(lc.check_local(file, ext=".md"))
    assert len(urls) == 2


@pytest.mark.parametrize("mode", ["sync", "coro"])
def test_mod(mode):

    if mode == "sync":
        pytest.importorskip("requests", reason="Synchronous requires requests")

    with importlib.resources.path("linkcheckmd.tests", "badlink.md") as file:
        urls = lc.check_remotes(file, domain="github.invalid", ext=".md", mode=mode)

    assert len(urls) == 2


@pytest.mark.parametrize("mode", ["sync", "coro"])
def test_script(mode):

    if mode == "sync":
        pytest.importorskip("requests", reason="Synchronous requires requests")

    with importlib.resources.path("linkcheckmd.tests", "badlink.md") as file:
        ret = subprocess.check_output(
            ["linkcheckMarkdown", str(file), "github.invalid", "--mode", mode], text=True
        )
    assert "github.invalid" in ret
