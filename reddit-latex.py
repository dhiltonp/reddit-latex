#!/usr/local/bin/python3

import praw
import time
import pylatex
import pypandoc
from time import sleep

time_units = [
    ("month", 60*60*24*30),
    ("week", 60*60*24*7),
    ("day", 60*60*24),
    ("hour", 60*60),
    ("minute", 60),
    (None, 999-time.time())]


class ThreadFormatter:
    def __init__(self):
        self.r = praw.Reddit(user_agent="reddit-latex:v.1")

    def format_comment_header(self, comment):
        header = ""
        header += "%d points /u/%s" % (comment.score, comment.author)
        if comment.author_flair_text:
            header += " ("+comment.author_flair_text+")"
        if comment.edited:
            header += " -- " + time.strftime("%b %d %Y", time.localtime(comment.created))
            diff = comment.edited - comment.created
            for name, seconds in time_units:
                if name == None:
                    # catchall
                    header += " (edited)"
                    break
                if diff > 2*seconds:
                    header += " (edited %d %ss after posting)" % (diff//seconds, name)
                    break
                elif diff > seconds:
                    header += " (edited %d %s after posting)" % (diff//seconds, name)
                    break
            #header += " ("+time.ctime(comment.edited)+")"
        else:
            header += " -- " + time.strftime("%b %d %Y", time.localtime(comment.created))

        #header += "\n\n"
        header = pypandoc.convert(header, "tex", format="md")
        header = "\\mdfsubtitle{"+header+"}\n\n"
        return header

    def format_comment(self, comment):
        if comment.body == "[deleted]":
            return pypandoc.convert("[deleted]", "tex", format="md")
        text = ""
        text += self.format_comment_header(comment)
        text += comment.body
        return pypandoc.convert(text, "tex", format="md")

    def format_thread(self, comments):
        if len(comments) == 0:
            return ""
        thread = "\\begin{mdframed}\n"
        for i in range(len(comments)):
            thread += self.format_comment(comments[i])
            discussion = self.format_thread(comments[i].replies)
            thread += discussion
        thread += "\\end{mdframed}\n"
        return thread

    def prioritize_comments(self, comments):
        pass

    def download_page(self, url):
        submission = self.r.get_submission(url=url)
        question = submission.selftext
        print(question)
        print(self.format_thread(submission.comments))

    def print_header(self):
        print("""\\documentclass{article}
\\usepackage{hyperref,color}
\\usepackage[framemethod=tikz]{mdframed}
\\usepackage[margin=0.5in]{geometry}
\\providecommand{\\tightlist}{%
  \\setlength{\\itemsep}{0pt}\\setlength{\\parskip}{0pt}}

\\begin{document}
""")

    def print_footer(self):
        print("""\\end{document}""")

formatter = ThreadFormatter()
formatter.print_header()
formatter.download_page("https://www.reddit.com/r/LaTeX/comments/3umdyg/latex_formatting_of_reddit_posts/")
formatter.download_page("https://www.reddit.com/r/AskHistorians/comments/1zmi5t/is_there_any_evidence_that_moors_reached_the/")
formatter.print_footer()
