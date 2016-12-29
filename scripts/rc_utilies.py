import codecs
import re
import pywikibot
from pywikibot import config2 as config


def split_line(counter):
    if counter % 100:
        return ''
    else:
        pywikibot.output("%s lines" % counter)
        return (u'<!-- ***** %dth title is above this line. ***** -->\n'
                % counter)


def text_file_page_gen(filename, site):
    f = codecs.open(filename, 'r', config.textfile_encoding)

    r = re.compile(ur'\[\[(.+?)(?:\]\]|\|)')
    page_title = None
    for page_title in r.findall(f.read()):
        yield pywikibot.Page(site, page_title)
    if page_title is None:
        f.seek(0)
        for title in f:
            title = title.strip()
            if '|' in title:
                title = title[:title.index('|')]
            if title:
                yield title
    f.close()