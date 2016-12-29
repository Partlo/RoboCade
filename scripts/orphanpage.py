import wikipedia as pywikibot
import pagegenerators
import codecs


class OrphanChecker:
    def __init__(self, articles=None, *args):
        self.counter = 0
        self.articles = articles
        self.site = pywikibot.getSite()
        self.parenthetical = False
        self.max_ref_links = None
        self.fix = False
        first_page = None
        all_pages = False
        text_file_name = None

        for arg in pywikibot.handleArgs(*args):
            if arg.startswith('-start'):
                first_page = arg[7:]
                if not first_page:
                    first_page = pywikibot.input(u'At which page do you want to start?')
            elif arg == '-paren':
                self.parenthetical = True
            elif arg == '-all':
                all_pages = True
            elif arg.startswith('-filename'):
                text_file_name = arg[10:]
                if not text_file_name:
                    text_file_name = pywikibot.input(u'Please enter the local file name:')
            elif arg.startswith('-max'):
                self.max_ref_links = int(arg[5:])
                if not self.max_ref_links:
                    self.max_ref_links = int(pywikibot.input(u'What is the maximum number of references?'))

        if self.max_ref_links is None:
            self.max_ref_links = int(pywikibot.input(
                u'What is the maximum number of references?'))

        if all_pages:
            if first_page is None:
                first_page = pywikibot.input(
                    u'At which page do you want to start?')
            namespace = pywikibot.Page(self.site, first_page).namespace()
            first_page_title = pywikibot.Page(self.site, first_page).title(withNamespace=False)
            self.gen = pagegenerators.AllpagesPageGenerator(first_page_title,
                                                            namespace,
                                                            includeredirects='only')
        elif text_file_name:
            self.gen = pagegenerators.TextfilePageGenerator(text_file_name)

    def run(self):
        done = []
        not_done = []
        try:
            for page in self.gen:
                try:
                    for p in page.linkedPages():
                        pywikibot.output(p.title())
                    pages = list(page.getReferences(internal=True, follow_redirects=False))
                    num_refs = len(pages)
                    if self.fix:
                        for p in pages:
                            if p.title() == page.title():
                                continue
                            elif p.title() == page.title() + '/Canon':
                                continue
                            elif p.title() == page.title() + '/Legends':
                                continue
                            else:
                                pywikibot.output("%s --> %s" % (page.title(), p.title()))
                                not_done.append([page.title(), p.title()])
                                break
                    else:
                        pywikibot.output("%s has %s pages linking to it" % (page.title(), num_refs))
                        if num_refs <= int(self.max_ref_links):
                            done.append([page.title(), num_refs])
                        else:
                            not_done.append([page.title(), num_refs])
                except pywikibot.NoPage:
                    done.append([page.title(), -1])
        finally:
            self.articles.write(u'Delete:\n')
            for p in done:
                self.articles.write(u'%s	%s\n' % (p[0], p[1]))
                self.articles.flush()
            self.articles.write(u'\nNot:\n')
            for n in not_done:
                self.articles.write(u'%s	%s\n' % (n[0], n[1]))
                self.articles.flush()

    def split_line(self):
        if self.counter % 100:
            return ''
        else:
            return (u'<!-- ***** %dth title is above this line. ***** -->\n'
                    % self.counter)


def main(*args):
    append = False
    filename = "redirects.txt"
    try:
        title_file = codecs.open(filename, encoding='utf-8',
                                 mode=(lambda x: x and 'a' or 'w')(append))
    except IOError:
        pywikibot.output("%s cannot be opened for writing." %
                         filename)
        return

    checker = OrphanChecker(title_file, *args)

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
