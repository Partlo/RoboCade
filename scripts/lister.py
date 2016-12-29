import wikipedia as pywikibot
import pagegenerators
import codecs
import catlib
import re


def splitLine(counter, title):
    if 0 == (counter % 500):
        try:
            pywikibot.output("%s	%s", (counter, title))
        except TypeError:
            pywikibot.output(str(title))


def main(*args):
    genFactory = pagegenerators.GeneratorFactory()
    for arg in pywikibot.handleArgs(*args):
        print arg
        genFactory.handleArg(arg)

    gener = None
    gener = genFactory.getCombinedGenerator(gener)
    gen = pagegenerators.PreloadingGenerator(gener, pageNumber=60)
    counter = 0
    append = False
    filename = 'articles.txt'
    articles = codecs.open(filename, encoding='utf-8',
                           mode=(lambda x: x and 'a' or 'w')(append))
    try:
        for page in gen:
            counter += 1
            splitLine(counter, page.title())
            # articles.write(u'[[%s]]\n' % (page.title()))
            # articles.write(u'[[%s/Legends]]\n' % (page.title()))
            # articles.write(u'[[%s/Canon]]\n' % (page.title()))
            # articles.write(u'[[%s]]\n' % (page.title()))
            articles.write(u'[[%s]]\n' % (page.title()))
            # articles.write(u'[[%s]]\n' % (page.title()[:-6]))
            articles.flush()
    except KeyboardInterrupt:
        quit()
    if articles:
        articles.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
