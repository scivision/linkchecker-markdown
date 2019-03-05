
[![Build Status](https://travis-ci.com/scivision/linkchecker-markdown.svg?branch=master)](https://travis-ci.com/scivision/linkchecker-markdown)

# Linkchecker for Markdown-based static generated sites

Python Requests-based simple check of links in Markdown .md files only.
I got frustrated with all the false positives and moreso the false negatives from LinkChecker.py, which is also very slow and only works with HTML.
This tool is very helpful for large Markdown-based Jekyll and Hugo sites.
It is very fast and simple.

HOWEVER: we have found that as time goes on, more and more servers have strict anti-leeching methods that break this program too.
The solution may be to use an asyncio-based web browser interface like Arsenic in this program.
We hope to do so as time/interest permit.

Alternatives exist for Go and JavaScript.

## install
```sh
pip install -e .
```

## Examples

* Jekyll
  ```sh
  python linkcheck.py ~/web/_posts
  ```
* Hugo
  ```sh
  python linkcheckpy ~/web/content
  ```
