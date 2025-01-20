#!/usr/bin/env python3

import sys
import re
import os, os.path

from jinja2 import Environment, FileSystemLoader, select_autoescape

destdir = 'htdocs'

class Issue:
    def __init__(self, index, date, articles):
        self.index = index
        self.showindex = index.replace('-', '.')
        self.uri = 'issue-%s' % (index,)
        self.date = date
        self.articles = articles

class Article:
    def __init__(self, title, uri, author=None, alttitle=None, quoted=None):
        self.title = title
        self.alttitle = escape_html_string(alttitle)
        self.uri = uri
        self.author = author
        self.quoted = quoted
        if quoted is None:
            self.quoted = (author is not None)

        showtitle = escape_html_string(title, escapetags=True)
        while '_' in showtitle:
            showtitle = showtitle.replace('_', '<i>', 1)
            showtitle = showtitle.replace('_', '</i>', 1)
        self.showtitle = showtitle

        self.content = None
        self.comments = []
        
    def load(self, issue):
        path = os.path.join('articles', issue.uri, self.uri)
        fl = open(path)
        dat = fl.read()
        fl.close()

        ls = []
        comdict = None
        for ln in dat.split('\n'):
            ln = ln.rstrip()
            if ln == '----':
                if comdict is not None and comdict:
                    self.comments.append(Comment(comdict))
                comdict = {}
                continue
            if comdict is not None:
                if not ln:
                    continue
                key, _, val = ln.partition(':')
                key = key.strip()
                val = val.strip()
                comdict[key] = val
            else:
                ls.append(ln)

        if comdict is not None and comdict:
            self.comments.append(Comment(comdict))
            
        ls.append('')
        self.content = escape_html_string('\n'.join(ls), escapetags=False)

class Comment:
    def __init__(self, map):
        self.timestamp = map['timestamp']
        self.timestr = map['timestr']
        self.author = map['author']
        self.authorurl = map.get('authorurl')
        self.body = escape_html_string(map['body'], escapetags=False)

htmlable_pattern = re.compile("[ -%'-;=?-~]+")
htmlable_withtags_pattern = re.compile("[ -~]+")

html_entities = {
    # Newlines and tabs are not encoded.
    '\n': '\n', '\t': '\t',
    # The classic three HTML characters that must be escaped.
    '&': '&amp;', '<': '&lt;', '>': '&gt;',
}

def escape_html_string(val, escapetags=True):
    """Apply &#x...; escapes for Unicode characters.
    If escapetags is true, also apply the basic HTML/XML &-escapes.
    """
    if val is None:
        return None
    if escapetags:
        pat = htmlable_pattern
    else:
        pat = htmlable_withtags_pattern
    res = []
    pos = 0
    while pos < len(val):
        match = pat.match(val, pos=pos)
        if match:
            res.append(match.group())
            pos = match.end()
        else:
            ch = val[pos]
            ent = html_entities.get(ch)
            if ent:
                res.append(ent)
            else:
                res.append('&#x%X;' % (ord(ch),))
            pos += 1
    return ''.join(res)

issues = [
    
    Issue('64', 'August 9, 2016', [
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
    
    Issue('63', 'April 11, 2016', [
        Article('Letter from the Editor and Call for Submissions',
                'issue-63-letter-from-the-editor'),
        Article('SPAG Specifics: Paulo Chikiamco’s _Slammed!_',
                'spag-specifics-paolo-chikiamcos-slammed',
                'Hugo Labrande'),
        Article('You Are an Online Clickbait Satirist. Can You Hack It in the IF World?',
                'you-are-an-online-clickbait-satirist-can-you-hack-it-in-the-if-world',
                'Katherine Morayati'),
        Article('Safeguarding your IF Awards from Animal Attack',
                'safeguarding-your-if-voting-from-animal-attack',
                'Ted Casaubon'),
    ]),
    
    Issue('62', 'May 4, 2015', [
        Article('Letter From the Editor and Call for Submissions!',
                'letter-from-the-editor-and-call-for-submissions'),
        Article('>JUSTIFY, HEIGHTEN, SAY YES: Interactive Fiction as Improv',
                'justify-heighten-say-yes-interactive-fiction-as-improv',
                'Hugo Labrande'),
        Article('Poetry Is What Gets Lost in Translation: Notes on translating _PataNoir_ and _Sunday Morning_',
                'poetry-is-what-gets-lost-in-translation-notes-on-translating-patanoir-and-sunday-morning',
                'Marius Müller'),
        Article('Choose Your Own Path: Taking CYOA IRL with the Active Fiction Project',
                'active-fiction-project-vancouver',
                'Rowan Lipkovits'),
        Article('Capsule reviews of the games in ParserComp and Spring Thing’s main garden',
                'parsercomp-spring-thing-2015-reviews',
                alttitle='SPAG Verdicts: ParserComp, Spring Thing'),
        Article('“Macdougal and Me at the Spring Thing Fair”: a longer-form, fictionalized overview of Spring Thing',
                'macdougal-and-me-at-the-spring-thing-fair',
                'Christopher Huang',
                alttitle='Macdougal and Me at the Spring Thing Fair',
                quoted=False),
        Article('SPAG Specifics: Matthew S. Burns’ _The Writer Will Do Something_',
                'the-writer-will-do-something-matthew-burns-review',
                'Katherine Morayati'),
    ]),
    
    Issue('61-5', 'February 2, 2015', [
        Article('Letter from the Editor and Call for Submissions',
                'issue-61-5-letter-from-the-editor-masthead-and-call-for-submissions'),
        Article('2014: The Year That Was',
                'the-year-that-was',
                'Katherine Morayati'),
        Article('SPAG Specifics: Puzzles in _The Hours_',
                'spag-specifics-the-hours',
                'Victor Gijsbers'),
        Article('SPAG Valentines!',
                'spag-valentines'),
    ]),
    
    Issue('61', 'January 2, 2013', [
        Article('Editorial: Welcome back!',
                'editorial'),
        Article('The Modem Squeals of a Guilded Youth — Rowan Lipkovits talks to Jim Munroe',
                'modem-squeals-of-a-guilded-youth-jim-munroe'),
        Article('Depicting Grief — An interview with the author of Eurydice',
                'depicting-grief-eurydice-interview',
                'Sam Kabo Ashwell'),
        Article('Andromeda Apocalypse — Backstage with Marco Innocenti',
                'andromeda-apocalypse-marco-innocenti',
                'Felix Pleșoianu'),
        Article('Shared Worlds — Collaboration in interactive fiction',
                'shared-worlds-collaboration-in-interactive-fiction',
                'Joey Jones'),
        Article('SPAG Specifics: Creating, inverting and making good the detective genre',
                'creating-inverting-making-good-the-detective-genre',
                'Mark Ricard'),
    ]),
    
]

for issue in issues:
    for art in issue.articles:
        art.load(issue)

jenv = Environment(
    loader = FileSystemLoader('templates'),
    extensions = [
    ],
    autoescape = select_autoescape(),
    keep_trailing_newline = True,
)

template = jenv.get_template('front.html')
fl = open(os.path.join(destdir, 'index.html'), 'w')
fl.write(template.render(issues=issues))
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
        template = jenv.get_template('article.html')
        dir = os.path.join(destdir, issue.uri, art.uri)
        os.makedirs(dir, exist_ok=True)
        fl = open(os.path.join(dir, 'index.html'), 'w')
        fl.write(template.render(issue=issue, art=art, content=art.content))
        fl.close()
