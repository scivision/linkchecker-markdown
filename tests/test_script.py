#!/usr/bin/env python
import subprocess
import sys
import pytest
from pathlib import Path
import linkcheckmd as lc

R = Path(__file__).parent


@pytest.mark.parametrize("mode,path", [("sync", R), ("sync", R / "badlink.md"), ("coro", R), ("coro", R / "badlink.md")])
def test_mod(mode, path):
    urls = lc.run_check(path, "github.invalid", ".md", mode)
    assert len(urls) == 2


@pytest.mark.parametrize("mode", ["sync", "coro"])
def test_script(mode):
    ret = subprocess.check_output(
        [sys.executable, "linkcheck.py", str(R), "github.invalid", "--mode", mode], cwd=R.parent, universal_newlines=True
    )
    assert "github.invalid" in ret


if __name__ == "__main__":
    pytest.main([__file__])
