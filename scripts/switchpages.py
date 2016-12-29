#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
This script can move pages.

These command line parameters can be used to specify which pages to work on:

&params;

Furthermore, the following command line parameters are supported:

-from and -to     The page to move from and the page to move to.

-noredirect       Leave no redirect behind.

-prefix           Move pages by adding a namespace prefix to the names of the
                  pages. (Will remove the old namespace prefix if any)
                  Argument can also be given as "-prefix:namespace:".

-always           Don't prompt to make changes, just do them.

-skipredirects    Skip redirect pages (Warning: increases server load)

-summary          Prompt for a custom summary, bypassing the predefined message
                  texts. Argument can also be given as "-summary:XYZ".

-pairs            Read pairs of file names from a file. The file must be in a
                  format [[frompage]] [[topage]] [[frompage]] [[topage]] ...
                  Argument can also be given as "-pairs:filename"

"""
#
# (C) Leonardo Gregianin, 2006
# (C) Andreas J. Schwab, 2007
# (C) Pywikibot team, 2006-2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import sys
import re
import pywikibot
from pywikibot import i18n
from movepages import MovePagesBot
import pagegenerators

def main():
    gen = None
    prefix = None
    oldName = None
    newName = None
    noredirect = False
    always = False
    skipredirects = False
    summary = None
    fromToPairs = []

    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()

    for arg in pywikibot.handleArgs():
        if arg.startswith('-pairs'):
            if len(arg) == len('-pairs'):
                filename = pywikibot.input(
                    u'Enter the name of the file containing pairs:')
            else:
                filename = arg[len('-pairs:'):]
            oldName1 = None
            for page in pagegenerators.TextfilePageGenerator(filename):
                if oldName1:
                    fromToPairs.append([oldName1, page.title()])
                    oldName1 = None
                else:
                    oldName1 = page.title()
            if oldName1:
                pywikibot.warning(
                    u'file %s contains odd number of links' % filename)
        elif arg == '-always':
            always = True
        elif arg == '-skipredirects':
            skipredirects = True
        elif arg.startswith('-from:'):
            if oldName:
                pywikibot.warning(u'-from:%s without -to:' % oldName)
            oldName = arg[len('-from:'):]
        elif arg.startswith('-to:'):
            if oldName:
                fromToPairs.append([oldName, arg[len('-to:'):]])
                oldName = None
            else:
                pywikibot.warning(u'%s without -from' % arg)
        elif arg.startswith('-summary'):
            if len(arg) == len('-summary'):
                summary = pywikibot.input(u'Enter the summary:')
            else:
                summary = arg[9:]
        else:
            genFactory.handleArg(arg)

    if oldName:
        pywikibot.warning(u'-from:%s without -to:' % oldName)
    for pair in fromToPairs:
        page = pywikibot.Page(pywikibot.getSite(), pair[0])
        if page.title().endswith('/Canon'):
            noredirect = False
        else:
            noredirect = True
        bot = MovePagesBot(None, prefix, noredirect, always, skipredirects, summary)
        bot.moveOne(page, pair[1])

    if not gen:
        gen = genFactory.getCombinedGenerator()
    if gen:
        preloadingGen = pagegenerators.PreloadingGenerator(gen)
        bot = MovePagesBot(preloadingGen, prefix, noredirect, always,
                           skipredirects, summary)
        bot.run()
    elif not fromToPairs:
        pywikibot.showHelp()

if __name__ == '__main__':
    try:
        main()
    finally:
        pywikibot.stopme()
