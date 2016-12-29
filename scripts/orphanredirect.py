import wikipedia as pywikibot
import pagegenerators
import codecs


class OrphanChecker:
    def __init__(self, articles=None, *args):
        self.counter = 0
        self.articles = articles
        self.done = codecs.open('done.txt', encoding='utf-8',
                                mode=(lambda x: x and 'a' or 'w')(False))
        self.site = pywikibot.getSite()
        self.parenthetical = False
        self.maxRefLinks = None
        firstPage = None
        allpages = False
        textfilename = None

        for arg in pywikibot.handleArgs(*args):
            if arg.startswith('-start'):
                if len(arg) == 6:
                    firstPage = pywikibot.input(
                        u'At which page do you want to start?')
                else:
                    firstPageTitle = arg[6:]
            elif arg == '-paren':
                self.parenthetical = True
            elif arg == '-all':
                allpages = True
            elif arg.startswith('-filename'):
                textfilename = arg[10:]
                if not textfilename:
                    textfilename = pywikibot.input(
                        u'Please enter the local file name:')
            elif arg.startswith('-max'):
                if len(arg) == 4:
                    self.maxRefLinks = int(pywikibot.input(
                        u'What is the maximum number of references?'))
                else:
                    self.maxRefLinks = int(arg[5:])

        if self.maxRefLinks is None:
            self.maxRefLinks = int(pywikibot.input(
                u'What is the maximum number of references?'))

        if allpages:
            if firstPage is None:
                firstPage = pywikibot.input(
                    u'At which page do you want to start?')
            namespace = pywikibot.Page(self.site, firstPage).namespace()
            firstPageTitle = pywikibot.Page(self.site, firstPage).title(withNamespace=False)
            self.gen = pagegenerators.AllpagesPageGenerator(firstPageTitle,
                                                            namespace,
                                                            includeredirects='only')
        elif textfilename:
            self.gen = pagegenerators.TextfilePageGenerator(textfilename)

    def run(self):
        nopage = []
        notredirects = []
        try:
            for page in self.gen:
                try:
                    # if self.parenthetical:
                    #     if page.title().find("(") == -1:
                    #         continue
                    # else:
                    # if page.isRedirectPage():
                    pages = list(page.getReferences(internal=True))
                    numRefs = len(pages)
                    pywikibot.output("%s has %s pages linking to it" % (page.title(), numRefs))
                    self.counter += 1
                    if numRefs <= int(self.maxRefLinks):
                        self.done.write(u'%s	%s\n%s'
                                        % (page.title(asLink=True),
                                           numRefs,
                                           self.splitLine()))
                    else:
                        self.articles.write(u'%s	%s\n%s'
                                            % (page.title(asLink=True),
                                               numRefs,
                                               self.splitLine()))
                    self.articles.flush()
                    # else:
                    #     notredirects.append(page.title())
                except pywikibot.NoPage:
                    nopage.append(page.title())
            self.articles.write(u'Delete:\n')
            for p in nopage:
                self.articles.write(u'%s\n' % p)
                self.articles.flush()
            self.articles.write(u'\nNot:\n')
            for n in notredirects:
                self.articles.write(u'%s\n' % n)
                self.articles.flush()
        except KeyboardInterrupt:
            quit()

    def splitLine(self):
        if self.counter % 100:
            return ''
        else:
            return (u'<!-- ***** %dth title is above this line. ***** -->\n'
                    % self.counter)

def main(*args):
    append = False
    filename = "redirects.txt"
    try:
        titlefile = codecs.open(filename, encoding='utf-8',
                                mode=(lambda x: x and 'a' or 'w')(append))
    except IOError:
        pywikibot.output("%s cannot be opened for writing." %
                         filename)
        return

    checker = OrphanChecker(titlefile, *args)

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