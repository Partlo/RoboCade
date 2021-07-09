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


expansions = {
    "rothc": "Rise of the Hutt Cartel",
    "starfighter": "Galactic Starfighter",
    "strongholds": "Galactic Strongholds",
    "shadow": "Shadow of Revan",
    "kotfe": "Knights of the Fallen Empire",
    "kotet": "Knights of the Eternal Throne",
    "onslaught": "Onslaught"
}


def main(*args):
    gen_factory = pagegenerators.GeneratorFactory()
    exp = ""
    for arg in pywikibot.handle_args(*args):
        if arg.lower() == "base":
            exp = "Star Wars: The Old Republic"
        elif arg.lower() in ["cartel", "market", "cartel market"]:
            exp = "Cartel Market"
        elif arg.lower() in expansions:
            exp = f"Star Wars: The Old Republic: {expansions[arg.lower()]}"

    gen_factory.handle_arg("-ns:0")
    if exp:
        gen_factory.handle_arg(f"-ref:{exp}")
    else:
        assert False

    gener = None
    gener = gen_factory.getCombinedGenerator(gener)
    gen = pagegenerators.PreloadingGenerator(gener, pageNumber=50)
    counter = 0
    append = False
    filename = 'tor.txt'
    articles = codecs.open(filename, encoding='utf-8',
                           mode=(lambda x: x and 'a' or 'w')(append))
    if exp == "Cartel Market":
        pattern = r'\*[ \']?\[\[Cartel Market'
    else:
        pattern = re.compile('\*[ ]?\'+[ ]?\[\[' + exp + '\]\][ ]?\'+')
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
            if "{{Top|real}}" in text:
                articles.write(u'\t%s\n' % (page.title()))
            elif re.search(pattern, text):
                articles.write(u'%s\n' % (page.title()))
            else:
                articles.write(u'\t%s\n' % (page.title()))
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
