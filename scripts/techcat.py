import pywikibot
from pywikibot import pagegenerators
import codecs
import re
from scripts.rc_utilities import split_line


def main(*args):
    gen_factory = pagegenerators.GeneratorFactory()
    for arg in pywikibot.handleArgs(*args):
        print(arg)
        gen_factory.handleArg(arg)
        gener = None
        gener = gen_factory.getCombinedGenerator(gener)
        gen = pagegenerators.PreloadingGenerator(gener, pageNumber=60)
        counter = 0
        append = False
        filename = 'params.txt'
        articles = codecs.open(filename, encoding='utf-8',
                               mode=(lambda x: x and 'a' or 'w')(append))
        params = ['imageBG', 'image', 'name', 'homeworld', 'birth', 'death', 'species', 'gender', 'height', 'mass',
                  'hair', 'eyes', 'skin', 'cyber', 'era', 'affiliation', 'masters', 'apprentices']
        try:
            for page in gen:
                text = page.get()
                line = ''
                if text != re.sub(r"\{\{[Ll]ocation(\||\r\n)", r"",
                                  text):  # and text != re.sub(r"\|builder=", r"", text):
                    counter += 1
                    articles.write(u'#%s	%s\n%s' % (page.title(), line, split_line(counter)))
                    articles.flush()
                # for param in params:
                # if text == re.sub(r"\|%s=" % param, r"", text)
                # line = line + '	' + param
                # if len(line) > 0:
                # counter += 1
                # articles.write(u'#%s	%s\n%s' % (page.title(), line, splitLine(counter)))
                # articles.flush()
        except KeyboardInterrupt:
            quit()
        if articles:
            articles.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
