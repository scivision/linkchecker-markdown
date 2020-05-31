# Linkchecker for Markdown-based static generated sites

![Actions Status](https://github.com/scivision/linkchecker-markdown/workflows/ci/badge.svg)
[![pypi versions](https://img.shields.io/pypi/pyversions/linkcheckmd.svg)](https://pypi.python.org/pypi/linkcheckmd)
[![PyPi Download stats](http://pepy.tech/badge/linkcheckmd)](http://pepy.tech/project/linkcheckmd)

Python Requests based simple check of links in Markdown .md files only.
I got frustrated with all the false positives and moreso the false negatives from LinkChecker.py, which is also very slow and only works with HTML.
This tool is very helpful for large Markdown-based Jekyll and Hugo sites.
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

The static site generator does NOT have to be running for these tests--it looks at the .md files directly.
Assuming your webpage Markdown files have top-level directory ~/web:

* Jekyll

    ```sh
    linkcheckMarkdown ~/web/_posts
    ```

* Hugo

    ```sh
    linkcheckMarkdown ~/web/content
    ```

The `-v` `--verbose` options prints the URLs as they are checked.
Observe that URLs from different markdown files are interleaved, showing the asynchronous nature of this program.

## Alternatives

Strict anti-leeching methods cause false positives with this and other link checking programs.

Alternative solutions include:

* use an asyncio-based web browser interface like Arsenic
* use Go-based [htmltest](https://github.com/wjdp/htmltest).
* [GitHub Action](https://github.com/marketplace/actions/markdown-link-check) for checking links in Markdown files.
* Netlify link-check [plugin](https://github.com/munter/netlify-plugin-checklinks#readme)
