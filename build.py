#!/usr/bin/env python3

import sys
import re
import os, os.path

from jinja2 import Environment, FileSystemLoader, select_autoescape

destdir = 'htdocs'

class Issue:
    def __init__(self, index, date, articles):
        self.index = index
        self.uri = 'issue-%s' % (index,)
        self.date = date
        self.articles = articles

class Article:
    def __init__(self, title, uri, author=None, quoted=None):
        self.title = title
        self.uri = uri
        self.author = author
        self.quoted = quoted
        if quoted is None:
            self.quoted = (author is not None)

        showtitle = title.replace('&', '&amp;')
        showtitle = title.replace('>', '&gt;')
        showtitle = title.replace('<', '&lt;')
        while '_' in showtitle:
            showtitle = showtitle.replace('_', '<i>', 1)
            showtitle = showtitle.replace('_', '</i>', 1)
        self.showtitle = showtitle
            
issues = [
    Issue('64', 'August ###, 2016', [
        Article('Letter from the Editor and Call for Submissions',
                'issue-64-letter-from-the-editor-and-call-for-submissions'),
        Article('Top Threes: Brendan Patrick Hennessy _(Birdland)_',
                'top-threes-brendan-patrick-hennessy-birdland'),
        Article('>SOLVE ZORK: Teaching an AI to Play Parser IF',
                'solve-zork-teaching-an-ai-to-play-parser-if',
                'Hugo Labrande'),
        Article('I’m Your Forgotten Past: The Dubious History of Interactive Film',
                'im-your-forgotten-past-the-dubious-history-of-interactive-film',
                'Katherine Morayati'),
        Article('Evolving Storytelling in Hidden-Object Picture Games',
                'evolving-storytelling-in-hidden-object-games',
                'Lisa Brunette'),
        Article('SPAG Specifics: Caelyn Sandel’s _Bloom_',
                'spag-specifics-caelyn-sandels-bloom',
                'Cat Manning')
    ]),
]

## comments:
## 64-solvezork.html (2)
## 64-film.html (1)
## 64-hidden (17)
## 64-bloom (3)

jenv = Environment(
    loader = FileSystemLoader('templates'),
    extensions = [
    ],
    autoescape = select_autoescape(),
    keep_trailing_newline = True,
)

template = jenv.get_template('front.html')
fl = open(os.path.join(destdir, 'index.html'), 'w')
fl.write(template.render())
fl.close()

template = jenv.get_template('about.html')
fl = open(os.path.join(destdir, 'about/index.html'), 'w')
fl.write(template.render())
fl.close()

for issue in issues:
    template = jenv.get_template('issue.html')
    dir = os.path.join(destdir, issue.uri)
    os.makedirs(dir, exist_ok=True)
    fl = open(os.path.join(dir, 'index.html'), 'w')
    fl.write(template.render(uri=issue.uri, issue=issue))
    fl.close()
    
    for art in issue.articles:
        path = os.path.join('articles', issue.uri, art.uri)
        fl = open(path)
        content = fl.read()
        fl.close()
        
        template = jenv.get_template('article.html')
        dir = os.path.join(destdir, issue.uri, art.uri)
        os.makedirs(dir, exist_ok=True)
        fl = open(os.path.join(dir, 'index.html'), 'w')
        fl.write(template.render(issue=issue, art=art, content=content))
        fl.close()
