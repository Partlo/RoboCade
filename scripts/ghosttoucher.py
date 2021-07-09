import pywikibot
from pywikibot import pagegenerators


def main(*args):

    try:
        # config.cosmetic_changes = False
        gen = pagegenerators.GeneratorFactory()
        exceptions = []
        for arg in pywikibot.handle_args(*args):
            if arg.startswith('-excepttext:'):
                exceptions.append(arg[12:])
            else:
                gen.handle_arg(arg)
        gener = None
        gener = gen.getCombinedGenerator(gener)
        generator = pagegenerators.PreloadingGenerator(gener)
        ready = False
        for page in generator:
            try:
                # if page.title() == "Sludge Kintan":
                #     ready = True
                # if not ready:
                #     continue
                text = page.get()
                if any(e in text for e in exceptions):
                    print(f"Skipping page {page.title()} due to exception text")
                    continue
                page.put(text, "Bot: Ghost edit to update WhatLinksHere. Tell Cade if you see this.")
            except pywikibot.NoPage:
                pywikibot.output('%s does not exist, skipping' % page.title(asLink=True))
            except pywikibot.IsRedirectPage:
                pywikibot.output('%s is a redirect; skipping.' % page.title(asLink=True))
            except pywikibot.LockedPage:
                pywikibot.output('%s is protected; skipping.' % page.title(asLink=True))

    except KeyboardInterrupt:
        pywikibot.output("Stopping")

    finally:
        pywikibot.stopme()

if __name__ == '__main__':
    main()
