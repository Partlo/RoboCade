import pywikibot
import re
from pywikibot import pagegenerators, textlib


class RedirectFixer:
    def __init__(self, regex=False):
        self.site = pywikibot.getSite()
        self.acceptall = False
        self.regex = regex
        self.editSummary = "Bot: Fixing redirects"

    def fix_redirect(self, text, redirect, correct=None, rep=None, type=None):
        replacements = []
        exceptions = []
        func = lambda s: s[:1].lower() + s[1:] if s else ''
        if type:
            return

        if not rep and not correct:
            return
        if rep:
            oldR = re.compile(re.escape(rep[0]), re.UNICODE)
            text = textlib.replaceExcept(text, oldR, rep[1], exceptions)

        if redirect.endswith(")"):
            if correct.endswith(")"):
                replacements.append(("[[%s]]" % redirect, "[[%s]]" % correct))
                replacements.append(("[[%s]]" % func(redirect), "[[%s]]" % func(correct)))
                replacements.append(("[[%s|" % redirect, "[[%s|" % correct))
                replacements.append(("[[%s|" % func(redirect), "[[%s|" % correct))

            else:
                replacements.append(("[[%s]]" % redirect, "[[%s]]" % correct))
                replacements.append(("[[%s]]" % func(redirect), "[[%s]]" % func(correct)))
                replacements.append(("[[%s|%s]]" % (redirect, correct), "[[%s]]" % correct))
                replacements.append(("[[%s|%s]]" % (func(redirect), func(correct)), "[[%s]]" % func(correct)))
                replacements.append(("[[%s|%s]]" % (func(redirect), correct), "[[%s]]" % correct))
                replacements.append(("[[%s|" % redirect, "[[%s|" % correct))
                replacements.append(("[[%s|" % func(redirect), "[[%s|" % correct))

        else:
            if correct.endswith(")"):
                short = correct.split(" /")[0]
                if short == redirect:
                    replacements.append(("[[%s]]" % redirect, "[[%s|%s]]" % (correct, short)))
                    replacements.append(("[[%s]]" % func(redirect), "[[%s|%s]]" % (correct, func(short))))
                else:
                    replacements.append(("[[%s]]" % redirect, "[[%s|%s]]" % (correct, redirect)))
                    replacements.append(("[[%s]]" % func(redirect), "[[%s|%s]]" % (correct, func(redirect))))
                replacements.append(("[[%s|" % redirect, "[[%s|" % correct))
                replacements.append(("[[%s|" % func(redirect), "[[%s|" % correct))

            else:
                replacements.append(("[[%s]]" % redirect, "[[%s]]" % correct))
                replacements.append(("[[%s]]" % func(redirect), "[[%s]]" % func(correct)))
                replacements.append(("[[%s|" % redirect, "[[%s|" % correct))
                replacements.append(("[[%s|" % func(redirect), "[[%s|" % correct))

        flags = re.UNICODE
        for i in range(len(replacements)):
            old, new = replacements[i]
            if not self.regex:
                old = re.escape(old)
            oldR = re.compile(old, flags)
            replacements[i] = oldR, new

        for old, new in replacements:
            text = textlib.replaceExcept(text, old, new, exceptions)

        return text

    def check_page(self, page):
        links = page.linkedPages()
        old_text = page.get()
        new_text = page.get()

        if len(links):
            pywikibot.getall(self.site, links)
        else:
            return

        for page2 in links:
            if page2.isRedirectPage():
                target = page2.getRedirectTarget()
                new_text = self.fix_redirect(new_text, page2.title(), target.title())
            else:
                continue
            pywikibot.showDiff(old_text, new_text)
            choice = pywikibot.inputChoice(
                u'Do you want to accept these changes?',
                ['Yes', 'No', 'Edit', 'All', 'Quit'],
                ['y', 'N', 'e', 'a', 'q'], 'N')
            if choice == 'q':
                return False
            if choice == 'a':
                self.acceptall = True
            if choice == 'e':
                err = pywikibot.input(u'Enter the target text:',)
                fix = pywikibot.input(u'Enter the target replacement:',)
                new_text = self.fix_redirect(old_text, page2.title(), target.title(), rep=[err, fix])
            if choice == 'y':
                old_text = new_text
                return True

        if new_text == page.get():
            pywikibot.output(u'No changes were necessary in %s'
                             % page.title(asLink=True))
        else:
            page.put_async(new_text, self.editSummary)

        return True

def main(*args):
    regex = False
    genFactory = pagegenerators.GeneratorFactory()

    for arg in pywikibot.handleArgs():
        if arg == '-regex':
            regex = True
        genFactory.handleArg(arg)

    fixer = RedirectFixer(regex)

    gen = genFactory.getCombinedGenerator()
    for page in pagegenerators.PreloadingGenerator(gen):
        result = fixer.check_page(page)
        if not result:
            break

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()