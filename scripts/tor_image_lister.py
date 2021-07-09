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

    gen_factory.handle_arg("-catr:Images_from_Star_Wars:_The_Old_Republic")

    gener = None
    gener = gen_factory.getCombinedGenerator(gener)
    gen = pagegenerators.PreloadingGenerator(gener, pageNumber=50)
    counter = 0
    append = False
    filename = 'tor-images.txt'
    articles = codecs.open(filename, encoding='utf-8',
                           mode=(lambda x: x and 'a' or 'w')(append))

    try:
        for page in gen:
            if counter % 100 == 0:
                print(counter)

            counter += 1
            text = page.get()
            matches = re.findall(r'\[\[Category:Images[_ ]from[_ ]Star[_ ]Wars:[_ ]The[_ ]Old[_ ]Republic[: ]*?(.*?)\]\]', text)
            cat = []
            for c in matches:
                if c:
                    cat.append((c[2:] if c.startswith(": ") else c).strip())
            if cat:
                articles.write(u'%s\t%s\n' % (page.title(), ','.join(cat)))
            elif "Images from the Star Wars: The Old Republic Codex" in text:
                articles.write(u'%s\tCodex\n' % (page.title()))
            elif "Images of mounts from Star Wars: The Old Republic" in text:
                articles.write(u'%s\tMounts\n' % (page.title()))
            elif "Images of weapons from Star Wars: The Old Republic" in text:
                articles.write(u'%s\tWeapons\n' % (page.title()))
            elif "Images of pets from Star Wars: The Old Republic" in text:
                articles.write(u'%s\tPets\n' % (page.title()))
            else:
                articles.write(u'%s\tUnknown\n' % (page.title()))
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
