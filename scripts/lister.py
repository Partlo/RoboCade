import pywikibot
from pywikibot import pagegenerators
import codecs
import re


def split_line(counter, title):
    if 0 == (counter % 500):
        try:
            pywikibot.output("%s	%s", (counter, title))
        except TypeError:
            pywikibot.output(str(title))


def main(*args):
    gen_factory = pagegenerators.GeneratorFactory()
    for arg in pywikibot.handle_args(*args):
        print(arg)
        gen_factory.handle_arg(arg)

    gener = None
    gener = gen_factory.getCombinedGenerator(gener)
    gen = pagegenerators.PreloadingGenerator(gener, pageNumber=50)
    counter = 0
    append = False
    filename = 'names.txt'
    articles = codecs.open(filename, encoding='utf-8',
                           mode=(lambda x: x and 'a' or 'w')(append))
    try:
        for page in gen:
            if counter % 100 == 0:
                print(counter)

            counter += 1
            # split_line(counter, page.title())
            # # articles.write(u'[[%s]]\n' % (page.title()))
            # # articles.write(u'[[%s/Legends]]\n' % (page.title()))
            # # articles.write(u'[[%s/Canon]]\n' % (page.title()))
            # # articles.write(u'[[%s]]\n' % (page.title()))
            # articles.write(u'[[%s]]\n' % (page.title()))
            # # articles.write(u'[[%s]]\n' % (page.title()[:-6]))
            # articles.flush()
            # if "Darth" in page.title():
            text = page.get()

            # if "hermaphrodite" in text or "Hermaphrodite" in text:
            # # if "{{Top|real}}" not in text and re.search(r'\*[ ]?\'+[ ]?\[\[Star Wars: The Old Republic\]\][ ]?\'+', text):
            # # if "{{Top|real}}" not in text and re.search(r'\*[ ]?\'+[ ]?\[\[Star Wars: The Old Republic: Knights of the Eternal Throne\]\][ ]?\'+', text):
            # # if "{{Top|real}}" not in text and re.search(r'\*[ ]?\'+[ ]?\[\[Star Wars: The Old Republic: Knights of the Fallen Empire\]\][ ]?\'+', text):
            # # if "{{Top|real}}" not in text and re.search(r'\*[ ]?\'+[ ]?\[\[Star Wars: The Old Republic: Shadow of Revan\]\][ ]?\'+', text):
            # # if "{{Top|real}}" not in text and re.search(r'\*[ ]?\'+[ ]?\[\[Star Wars: The Old Republic: Rise of the Hutt Cartel\]\][ ]?\'+', text):
            x = re.search("\|source=''\[\[(.*?)\]\]''\n", text)
            if x:
                articles.write(u'%s\t%s\n' % (x.groups(1), page.title()))
                # articles.write(u'#[[%s]]\n' % (page.title()))
                articles.flush()
    except KeyboardInterrupt:
        quit()
    if articles:
        articles.close()


def determine_title_format(*, page):
    text = page.get()
    page_title = page.title()

    pagename = re.match("{{[Tt]op\|[^\n]+\|title=''{{PAGENAME}}''", text)
    if pagename:
        return f"''[[{page_title}]]''"

    title1 = None
    title_match = re.match("{{[Tt]op\|[^\n]+\|title=(?P<title>.*?)[|}]", text)
    if title_match:
        title1 = title_match.groupdict()['title']
        if title1 == f"''{page_title}''":
            return f"''[[{page_title}]]''"

    match = re.match("^(?P<title>.+?) \((?P<paren>.*?)\)$", page_title)
    if match:
        title2 = None
        title2_match = re.match("{{[Tt]op\|[^\n]+\|title2=(?P<title>.*?)[|}]", text)
        if title2_match:
            title2 = title2_match.groupdict()['title']

        if title1 or title2:
            title1 = title1 or match.groupdict()['title']
            title2 = title2 or match.groupdict()['paren']
            return f"[[{page_title}|{title1} ({title2})]]"
        else:
            return f"[[{page_title}]]"
    elif title1 and title1 != page_title:
        return f"[[{page_title}|{title1}]]"
    else:
        return f"[[{page_title}]]"


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
