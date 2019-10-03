[![Actions Status](https://github.com/scivision/linkchecker-markdown/workflows/ci/badge.svg)](https://github.com/scivision/linkchecker-markdown/actions)

# Linkchecker for Markdown-based static generated sites

We suggest considering Go-based [htmltest](https://github.com/wjdp/htmltest) for many more features and performance.

Python Requests-based simple check of links in Markdown .md files only.
I got frustrated with all the false positives and moreso the false negatives from LinkChecker.py, which is also very slow and only works with HTML.
This tool is very helpful for large Markdown-based Jekyll and Hugo sites.
It is very fast and simple.

HOWEVER: we have found that as time goes on, more and more servers have strict anti-leeching methods that break this program too.
The solution may be to use an asyncio-based web browser interface like Arsenic in this program, or simply use Go-based htmltest.

## Install

```sh
git clone https://github.com/scivision/linkchecker-markdown

pip install -e linkchecker-markdown
```

## Examples

The static site generator does NOT have to be running for these tests--it looks at the .md files directly.
Assuming your webpage Markdown files have top-level directory ~/web:

* Jekyll

    ```sh
    python linkcheck.py ~/web/_posts
    ```
* Hugo

    ```sh
    python linkcheck.py ~/web/content
    ```
