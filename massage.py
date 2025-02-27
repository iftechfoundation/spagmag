import sys
import os, os.path
import re
import ftfy

def scrape_file(bdat, filename):
    dat = guess_encoding(bdat)
    if filename in ('spag43.html', 'SPAG43'):
        dat = ftfy.fix_text(dat, unescape_html=False, uncurl_quotes=False, fix_line_breaks=True)
        dat = dat.replace('Ranma ˝', 'Ranma ½')
        dat = dat.replace('Muńz', 'Muñiz')
        dat = dat.replace('Muñz', 'Muñiz')
    else:
        dat = dat.replace('\r\n', '\n')
    return dat

def guess_encoding(bdat):
    try:
        dat = bdat.decode('utf-8')
        #print('...utf-8')
        return dat
    except:
        pass
    try:
        dat = bdat.decode('windows-1252')
        #print('...windows-1252')
        return dat
    except:
        pass
    raise Exception('decoding failed')

pat_ftpgmdhead = re.compile('ftp[:]?/+ftp.gmd.de[:]?/')
pat_ftpprefix = re.compile('ftp.(gmd.de|ifarchive.org)[:]?[/]+')
pat_ftpifhead = re.compile('ftp[:]?/+[a-z.]*ifarchive[.]org[:]?/')
pat_altif = re.compile('/(mirror|www).ifarchive.org/')
pat_ifdbhead = re.compile('http[s]?://ifdb.tads.org/')
pat_sparkylink = re.compile('href="http://[a-z.]*sparkynet.com/spag/')

footer = '''
<div id="oldfooter">
  <p>SPAG is maintained as a historical archive by the
  <a href="https://iftechfoundation.org/">Interactive Fiction Technology Foundation</a>.
  Pages are no longer updated and links may no longer work.
  All articles and reviews are copyright by their original authors.
  </p>
</div>
'''

def massage_text(dat):
    dat = pat_ftpgmdhead.sub('https://ifarchive.org/', dat)
    dat = pat_ftpifhead.sub('https://ifarchive.org/', dat)
    dat = pat_ftpprefix.sub('https://ifarchive.org/', dat)
    dat = pat_altif.sub('/ifarchive.org/', dat)
    dat = dat.replace('http://ifarchive.org/', 'https://ifarchive.org/')
    dat = pat_ifdbhead.sub('https://ifdb.org/', dat)
    return dat

def massage_html(dat):
    dat = dat.replace('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">', '<!DOCTYPE html>')
    dat = dat.replace('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">', '<!DOCTYPE html>')
    dat = dat.replace('<script src="http://www.google-analytics.com/ga.js" type="text/javascript"></script>', '')
    dat = dat.replace('<script type="text/javascript">var pageTracker=_gat._getTracker("UA-34585834-1");pageTracker._initData();pageTracker._trackPageview();</script>', '')
    dat = pat_ftpgmdhead.sub('https://ifarchive.org/', dat)
    dat = pat_ftpifhead.sub('https://ifarchive.org/', dat)
    dat = pat_ftpprefix.sub('https://ifarchive.org/', dat)
    dat = pat_altif.sub('/ifarchive.org/', dat)
    dat = dat.replace('http://ifarchive.org/', 'https://ifarchive.org/')
    dat = pat_ifdbhead.sub('https://ifdb.org/', dat)
    dat = pat_sparkylink.sub('href="/archives/', dat)
    dat = dat.replace('</body>', footer+'\n\n</body>')
    return dat

pat_textfile = re.compile('^SPAG[0-9]+$')

for (dirpath, dirnames, filenames) in os.walk('htdocs/archives-orig'):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        outpath = os.path.join(dirpath.replace('archives-orig', 'archives'), filename)
        if filename.endswith('.html'):
            print('html:', path)
            with open(path, 'rb') as infl:
                bdat = infl.read()
                dat = scrape_file(bdat, filename)
            dat = massage_html(dat)
            with open(outpath, 'wb') as outfl:
                bdat = dat.encode(encoding='ascii', errors='xmlcharrefreplace')
                outfl.write(bdat)
        elif filename.endswith('.txt') or pat_textfile.match(filename):
            print('text:', path)
            with open(path, 'rb') as infl:
                bdat = infl.read()
                dat = scrape_file(bdat, filename)
            dat = massage_text(dat)
            with open(outpath, 'wb') as outfl:
                bdat = dat.encode(encoding='utf-8')
                outfl.write(bdat)
            
        
    
