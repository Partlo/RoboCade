__author__ = 'cadec_000'

def main(*args):
    import pywikibot
    import config
    import pagegenerators

    try:
        config.cosmetic_changes = False
        wook = pywikibot.getSite('en', 'starwars')
        gen = pagegenerators.GeneratorFactory()
        for arg in pywikibot.handleArgs(*args):
            gen.handleArg(arg)
        gener = None
        gener = gen.getCombinedGenerator(gener)
        generator = pagegenerators.PreloadingGenerator(gener,
                                                       pageNumber=60)
        for page in generator:
            try:
                text = page.get()
                page.put(text, "Bot: Ghost edit to update WhatLinksHere. Tell Cade if you see this.")
            except pywikibot.NoPage:
                pywikibot.output('%s does not exist, skipping' % page.title(asLink=True))
            except pywikibot.IsRedirectPage:
                pywikibot.output('%s is a redirect; skipping.' % page.title(asLink=True))
            except pywikibot.LockedPage:
                pywikibot.output('%s is protected; skipping.' % page.title(asLink=True))
            except pywikibot.PageNotSaved:
                pywikibot.output('%s not saved.' % page.title(asLink=True))

    finally:
        pywikibot.stopme()

if __name__ == '__main__':
    main()