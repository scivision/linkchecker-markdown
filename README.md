# Linkchecker for Markdown-based static generated sites

![Actions Status](https://github.com/scivision/linkchecker-markdown/workflows/ci/badge.svg)
[![pypi versions](https://img.shields.io/pypi/pyversions/linkcheckmd.svg)](https://pypi.python.org/pypi/linkcheckmd)
[![PyPi Download stats](http://pepy.tech/badge/linkcheckmd)](http://pepy.tech/project/linkcheckmd)

Blazing-fast (10000 Markdown files per second) Python asyncio / [aiohttp](https://docs.aiohttp.org/)
based simple check of links in Markdown .md files only.
This tool is very helpful for large Markdown-based Jekyll and Hugo sites as
well as Markdown-based
[MkDocs](https://www.mkdocs.org/) documentation projects.
It is very fast and simple--it's what we use to check https://www.scivision.dev

## Install

for latest release:

```sh
python -m pip install linkcheckmd
```

or for latest development version.

```sh
git clone https://github.com/scivision/linkchecker-markdown

pip install -e linkchecker-markdown
```

## Usage

The static site generator does NOT have to be running for these tests.
This program looks at the Markdown .md files directly.

If any local or remote links are determined to be missing, the following happens:

* the file containing the bad link and the link is printed to "stdout"
* the program will exit with code 22 instead of 0 after all files are checked

The bad links are printed to stdout since the normal operation of this program is to check for errors.
Due to the fast, concurrent checking and numerous pages checked, there may be diagnostics printed to stderr.
That way library error messages can be kept separate from the missing page locations printed on stdout.


The examples assume webpage Markdown files have top-level directory ~/web.
*If using the linkchecker on an MkDocs documentation project, Markdown files
are typically found in a `~/docs` directory.*

### Python code

```python
import linkcheckmd as lc

lc.check_links("~/web")
```

### Command-line

This program may be invoked:

```sh
python -m linkcheckmd
```

* Jekyll

    ```sh
    python -m linkcheckmd ~/web/_posts
    ```

* Hugo

    ```sh
    python -m linkcheckmd ~/web/content
    ```

* MkDocs Documentation

    ```sh
    python -m linkcheckmd ~/docs
    ```

The `-v` `--verbose` options prints the URLs as they are checked.
Observe that URLs from different markdown files are interleaved, showing the asynchronous nature of this program.

### Benchmark

For benchmarking and reference, we include a synchronous Requests-based method.
For a website with 100+ pages, compare times of:

### Git precommit

See
[./examples/pre-commit](./examples/pre-commit)
script for a
[Git hook pre-commit](https://www.scivision.dev/git-markdown-pre-commit-linkcheck)
Python script.

### Tox and CI

This program can also be used as a check for bad links during continuous integration
testing or when using [`tox`](https://tox.readthedocs.io/).

## Alternatives

Strict anti-leeching methods can cause false positives with this and other link checking programs.

Alternative solutions include:

* asyncio-based web browser interface like Arsenic
* Go-based [htmltest](https://github.com/wjdp/htmltest).
* [GitHub Action](https://github.com/marketplace/actions/markdown-link-check) for checking links in Markdown files.
* Netlify link-check [plugin](https://github.com/munter/netlify-plugin-checklinks#readme)
* LinkChecker.py: too many false positives/negatives, very slow and only works with HTML.
