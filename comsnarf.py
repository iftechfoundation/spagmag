import sys
import re

from html_sanitizer import Sanitizer

pat_headstart = re.compile('<header class="comment-meta comment-author vcard">')
pat_head = re.compile('<cite>(.*)</cite>.*<time datetime="([^"]*)">([^<]*)</time>')
pat_btag = re.compile('<b[^>]*>(.*)</b[^>]*>')
pat_linktag = re.compile('<a[ ]+href="([^"]*)"[^>]*>(.*)</a[^>]*>')
pat_comstart = re.compile('<section class="comment-content comment">')
pat_comend = re.compile('<!-- .comment-content -->')

sanitizer = Sanitizer({ 'add_nofollow': True })

fl = open(sys.argv[1])

comments = []

dat = None
body = None

for ln in fl.readlines():
    ln = ln.strip()
    if pat_headstart.match(ln):
        dat = {}
        body = None
        continue
    match = pat_head.search(ln)
    if match:
        dat['timestamp'] = match.group(2)
        dat['timestr'] = match.group(3)
        val = match.group(1).strip()
        match = pat_btag.match(val)
        if match:
            val = match.group(1)
        match = pat_linktag.match(val)
        if match:
            val = match.group(2)
            dat['authorurl'] = match.group(1)
        dat['author'] = val
        continue
    match = pat_comstart.match(ln)
    if match:
        body = []
        continue
    match = pat_comend.search(ln)
    if match:
        body = '\n'.join(body)
        body = sanitizer.sanitize(body)
        dat['body'] = body
        comments.append(dat)
        dat = None
        body = None
        continue
    if body is not None:
        body.append(ln)

if comments:
    print('\n----')
for dat in comments:
    for key, val in dat.items():
        print('%s: %s' % (key, val,))
    print('\n----')

    
