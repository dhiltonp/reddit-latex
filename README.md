# reddit-latex
Converts a Reddit thread into LaTeX

Depends on praw and pypandoc.

```
./reddit-latex.py https://www.reddit.com/r/LaTeX/comments/3umdyg/latex_formatting_of_reddit_posts > latex_formatting.tex
pdflatex latex_formatting.tex
```

Sample output: http://filebin.net/c9x2mvhfbv/test2.pdf


# requirements

 - latex
 - `pip3 install praw pypandoc`
 - praw.ini file

```
[DEFAULT]
client_id=$SOME_VALUE
client_secret=$SOME_VALUE
```

Generate an id and secret from https://www.reddit.com/prefs/apps


# todo

- fix nested frames crossing over to multiple pages
- fix URLs for printing
- clean up pdflatex errors


