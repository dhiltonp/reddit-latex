#!/usr/bin/python3

import time
import sys

import praw
import pypandoc

time_units = [
    ("month", 60*60*24*30),
    ("week", 60*60*24*7),
    ("day", 60*60*24),
    ("hour", 60*60),
    ("minute", 60),
    (None, 999-time.time())]


class ThreadFormatter:
    indent_depth = .8
        
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
        else:
            header += " -- " + time.strftime("%b %d %Y", time.localtime(comment.created))

        header = pypandoc.convert(header, "tex", format="md").strip()
        header = '\n\\hrulefill\\linebreak\\textbf{'+header+'}\n\n'
        return header

    def format_comment(self, comment):
        if comment.body == "[deleted]":
            return pypandoc.convert("[deleted]", "tex", format="md")
        text = ""
        text += self.format_comment_header(comment)
        text += pypandoc.convert(comment.body, "tex", format="md")
        return text

    def format_thread(self, comments, depth=1):
        if len(comments) == 0:
            return ""
        indent = self.indent_depth*depth
        thread = ""
        for comment in comments:
            if type(comment) == "MoreComments":
                # more comments, but don't bother printing them
                #  (all interesting comments should have previously been ordered/loaded)
                continue
            thread += "\\begin{adjustwidth}{"+str(indent)+"em}{}\n"
            thread += self.format_comment(comment)
            thread += "\\end{adjustwidth}\n"
            discussion = self.format_thread(comment.replies, depth+1)
            thread += discussion
        #thread += "\\end{adjustwidth}\n"
        return thread

    def prioritize_comments(self, comments):
        pass

    def download_page(self, url):
        submission = self.r.submission(url=url)
        #submission.replace_more_comments(limit=None, threshold=0)
        question = submission.selftext
        print(question)
        print(self.format_thread(submission.comments))

    def print_header(self):
        print("""\\documentclass{article}
\\usepackage{hyperref,color}
\\usepackage{changepage}
\\usepackage[margin=1in]{geometry}
\\providecommand{\\tightlist}{%
  \\setlength{\\itemsep}{0pt}\\setlength{\\parskip}{0pt}}

\\begin{document}
""")

    def print_footer(self):
        print("""\\end{document}""")

if __name__ == "__main__":    
    if len(sys.argv[1:]) > 0:
        formatter = ThreadFormatter()
        formatter.print_header()
        for page in sys.argv[1:]:
            formatter.download_page(page)    
        formatter.print_footer()
    else:
        print("./reddit-latex.py [reddit_comment_urls]")

