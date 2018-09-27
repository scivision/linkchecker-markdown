# linkchecker-markdown
Python Requests-based simple check of links in Markdown .md files only.
I got frustrated with all the false positives and moreso the false negatives from LinkChecker.py, which is also very slow and only works with HTML.
I have large Markdown-based Jekyll sites, and I wanted something that would run very fast, be simple, and reliable.

Alternatives exist for Go and JavaScript.

## install
```sh
pip install -e .
```

## Usage
Assuming the Markdown files for your website are in `~/web/_posts`:
```sh
python linkcheck.py ~/web/_posts
```
