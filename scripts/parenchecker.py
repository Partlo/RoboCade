import wikipedia as pywikibot
import pagegenerators
import codecs


class ParenChecker:
    def __init__(self, articles=None):
        self.counter = 0
        self.articles = articles
        self.site = pywikibot.getSite()
        firstPageTitle = pywikibot.input(
            u'At which page do you want to start?')
        namespace = pywikibot.Page(self.site, firstPageTitle).namespace()
        firstPageTitle = pywikibot.Page(self.site, firstPageTitle).title(withNamespace=False)
        self.gen = pagegenerators.AllpagesPageGenerator(firstPageTitle,
                                                        namespace,
                                                        includeredirects='only')
    def run(self):
        try:
            for page in self.gen:
                if page.title().find("(") != -1:
                    self.counter += 1
                    self.articles.write(u'#%s\n%s' % (page.title(), self.splitLine()))
                    self.articles.flush()
        except KeyboardInterrupt:
            quit()

    def splitLine(self):
        if self.counter % 100:
            return ''
        else:
            pywikibot.output("%s lines" % self.counter)
            return (u'<!-- ***** %dth title is above this line. ***** -->\n'
                    % self.counter)

def main(*args):
    append = False
    filename = "paren.txt"
    try:
        titlefile = codecs.open(filename, encoding='utf-8',
                                mode=(lambda x: x and 'a' or 'w')(append))
    except IOError:
        pywikibot.output("%s cannot be opened for writing." %
                         filename)
        return
    checker = ParenChecker(titlefile)

    try:
        checker.run()
    finally:
        if titlefile:
            titlefile.close()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()