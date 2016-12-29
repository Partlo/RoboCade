import pywikibot
import codecs
from rc_utilies import text_file_page_gen, split_line


class TORchecker:
    def __init__(self, exp=None, articles=None):
        self.counter = 0
        self.articles = articles
        self.site = pywikibot.getSite()
        self.list = []
        self.appearances = []

        for page in text_file_page_gen('swtor.txt', self.site):
            self.list.append(page)

        app_source = 'Star Wars: The Old Republic'
        if exp == 'rothc':
            app_source += ': Rise of the Hutt Cartel'
        if exp == 'strongholds':
            app_source += ': Galactic Strongholds'
        if exp == 'starfighter':
            app_source += ': Galactic Starfighter'
        if exp == 'shadow':
            app_source += ': Shadow of Revan'
        if exp == 'kotfe':
            app_source += ': Knights of the Fallen Empire'
        for page in list(pywikibot.Page(self.site, app_source).getReferences()):
            self.appearances.append(page.title())

    def run(self):
        not_linked = []
        not_listed = []
        try:
            for page in self.appearances:
                if page not in self.list:
                    not_listed.append(page)
            for page in self.list:
                if page not in self.appearances:
                    not_linked.append(page)

            self.articles.write(u'Not linked:\n')
            for p in not_linked:
                self.articles.write(u'%s\n' % p)
                self.articles.flush()
            self.articles.write(u'\nNot listed:\n')
            for p in not_listed:
                self.articles.write(u'%s\n' % p)
                self.articles.flush()
        except KeyboardInterrupt:
            quit()


def main(*args):
    append = False
    filename = "tor.txt"
    try:
        title_file = codecs.open(filename, encoding='utf-8',
                                mode=(lambda x: x and 'a' or 'w')(append))
    except IOError:
        pywikibot.output("%s cannot be opened for writing." %
                         filename)
        return
    checker = TORchecker(args[0], title_file)

    try:
        checker.run()
    finally:
        if title_file:
            title_file.close()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
