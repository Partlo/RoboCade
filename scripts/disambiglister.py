import wikipedia as pywikibot
import pagegenerators
import catlib


class DisambigLister:
    def __init__(self):
        self.site = pywikibot.getSite()
        self.cat = catlib.Category(self.site, 'Category:Disambiguation pages')
        self.gen = pagegenerators.CategorizedPageGenerator(self.cat)
        self.paren_list = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": [], "H": [], "I": [], "J": [],
                           "K": [], "L": [], "M": [], "N": [], "O": [], "P": [], "Q": [], "R": [], "S": [], "T": [],
                           "U": [], "V": [], "W": [], "X": [], "Y": [], "Z": [], "0-9": []}
        self.other_list = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": [], "H": [], "I": [], "J": [],
                           "K": [], "L": [], "M": [], "N": [], "O": [], "P": [], "Q": [], "R": [], "S": [], "T": [],
                           "U": [], "V": [], "W": [], "X": [], "Y": [], "Z": [], "0-9": []}

    def run(self):
        try:
            for page in self.gen:
                if page.title()[0:1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                    first = '0-9'
                else:
                    first = page.title()[0:1]

                if page.title().find('"') != -1:
                    continue

                if page.title().find("(disambiguation)") != -1:
                    self.paren_list[first].append(page.title(asLink=True))
                else:
                    self.other_list[first].append(page.title(asLink=True))

            letters = ["0-9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                       "S", "T", "U", "V", "W", "X", "Y", "Z"]
            new_paren_text = u'{{DisambigList}}\n'
            new_other_text = u'{{DisambigList|1}}\n'

            for letter in letters:
                paren_section = u'==%s==\n' % letter
                for page in self.paren_list[letter]:
                    paren_section += u'*%s\n' % page
                paren_section += u'\n'
                new_paren_text += paren_section

                other_section = u'==%s==\n' % letter
                for page in self.other_list[letter]:
                    other_section += u'*%s\n' % page
                other_section += u'\n'
                new_other_text += other_section

            paren_page = pywikibot.Page(self.site, 'Wookieepedia:Links to (disambiguation) pages')
            paren_page.put(new_paren_text, 'Updating list')
            other_page = pywikibot.Page(self.site, 'Wookieepedia:Links to disambiguating pages')
            other_page.put(new_other_text, 'Updating list')

        except KeyboardInterrupt:
            quit()


def main(*args):
    checker = DisambigLister()
    checker.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()