#!/usr/bin/python
"""
This script can move pages.

These command line parameters can be used to specify which pages to work on:

&params;

Furthermore, the following command line parameters are supported:

-from and -to     The page to move from and the page to move to.

-noredirect       Leave no redirect behind.

-notalkpage       Do not move this page's talk page (if it exists)

-prefix           Move pages by adding a namespace prefix to the names of the
                  pages. (Will remove the old namespace prefix if any)
                  Argument can also be given as "-prefix:namespace:".

-always           Don't prompt to make changes, just do them.

-skipredirects    Skip redirect pages (Warning: increases server load)

-summary          Prompt for a custom summary, bypassing the predefined message
                  texts. Argument can also be given as "-summary:XYZ".

-pairsfile        Read pairs of file names from a file. The file must be in a
                  format [[frompage]] [[topage]] [[frompage]] [[topage]] ...
                  Argument can also be given as "-pairsfile:filename"

"""
#
# (C) Pywikibot team, 2006-2021
#
# Distributed under the terms of the MIT license.
#
import re

import pywikibot
from pywikibot import i18n, pagegenerators
from pywikibot.bot import CurrentPageBot
from pywikibot.exceptions import PageRelatedError


# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {'&params;': pagegenerators.parameterHelp}  # noqa: N816


class MovePagesBot(CurrentPageBot):

    """Page move bot."""

    def __init__(self, **kwargs) -> None:
        """Initializer."""
        self.available_options.update({
            'prefix': None,
            'noredirect': False,
            'movetalkpage': True,
            'skipredirects': False,
            'summary': None,
        })
        super().__init__(**kwargs)

        self.appendAll = False
        self.regexAll = False
        self.noNamespace = False

    def moveOne(self, page, new_page_title) -> None:
        """Move on page to new_page_title."""
        try:
            msg = self.opt.summary
            if not msg:
                msg = i18n.twtranslate(page.site, 'movepages-moving')
            pywikibot.output(f'Moving page {page} to [[{new_page_title}]]')
            page.move(
                new_page_title, reason=msg,
                movetalk=self.opt.movetalkpage,
                noredirect=self.opt.noredirect)
        except PageRelatedError as error:
            pywikibot.output(error)

    def skip_page(self, page):
        """Treat only non-redirect pages if 'skipredirects' is set."""
        if self.getOption('skipredirects') and page.isRedirectPage():
            pywikibot.warning(f'Page {page} on {page.site} is a redirect; skipping')
            return True
        return super().skip_page(page)

    def treat_page(self):
        """Treat a single page."""
        page = self.current_page
        pagetitle = page.title(with_ns=False)
        namesp = page.site.namespace(page.namespace())

        if self.appendAll:
            new_page_title = f"{self.page_start}{pagetitle}{self.page_end}"
            if not self.noNamespace and namesp:
                new_page_title = f'{namesp}:{new_page_title}'
        elif self.regexAll:
            new_page_title = self.regex.sub(self.replace_pattern, pagetitle)
            if not self.noNamespace and namesp:
                new_page_title = f'{namesp}:{new_page_title}'
        if self.opt.prefix:
            new_page_title = f'{self.opt.prefix}{pagetitle}'
        if self.opt.prefix or self.appendAll or self.regexAll:
            if self.user_confirm('Change the page title to {!r}?'.format(new_page_title)):
                self.moveOne(page, new_page_title)
            return

        # else:
        choice = pywikibot.input_choice('What do you want to do?',
                                        [('change page name', 'c'),
                                         ('append to page name', 'a'),
                                         ('use a regular expression', 'r'),
                                         ('next page', 'n')])
        if choice == 'c':
            new_page_title = pywikibot.input('New page name:')
            self.moveOne(page, new_page_title)
        elif choice == 'a':
            self.page_start = pywikibot.input('Append this to the start:')
            self.page_end = pywikibot.input('Append this to the end:')
            new_page_title = f"{self.page_start}{pagetitle}{self.page_end}"
            if namesp:
                if pywikibot.input_yn('Do you want to remove the '
                                      'namespace prefix "{}:"?'.format(namesp),
                                      automatic_quit=False):
                    self.noNamespace = True
                else:
                    new_page_title = ('{}:{}'.format(namesp, new_page_title))
            choice2 = pywikibot.input_choice(
                'Change the page title to {!r}?'.format(new_page_title),
                [('yes', 'y'), ('no', 'n'), ('all', 'a')])
            if choice2 == 'y':
                self.moveOne(page, new_page_title)
            elif choice2 == 'a':
                self.appendAll = True
                self.moveOne(page, new_page_title)
        elif choice == 'r':
            search_pattern = pywikibot.input('Enter the search pattern:')
            self.replace_pattern = pywikibot.input('Enter the replace pattern:')
            self.regex = re.compile(search_pattern)
            if page.title() == page.title(with_ns=False):
                new_page_title = self.regex.sub(self.replace_pattern,
                                                page.title())
            else:
                if pywikibot.input_yn(f'Do you want to remove the namespace prefix "{namesp}:"?', automatic_quit=False):
                    new_page_title = self.regex.sub(self.replace_pattern, page.title(with_ns=False))
                    self.noNamespace = True
                else:
                    new_page_title = self.regex.sub(self.replace_pattern, page.title())
            choice2 = pywikibot.input_choice(
                'Change the page title to {!r}?'.format(new_page_title),
                [('yes', 'y'), ('no', 'n'), ('all', 'a')])
            if choice2 == 'y':
                self.moveOne(page, new_page_title)
            elif choice2 == 'a':
                self.regexAll = True
                self.moveOne(page, new_page_title)


def main(*args) -> None:
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    :param args: command line arguments
    :type args: str
    """
    oldName = None
    options = {}
    fromToPairs = []

    # Process global args and prepare generator args parser
    local_args = pywikibot.handle_args(args)
    genFactory = pagegenerators.GeneratorFactory()
    local_args = genFactory.handle_args(local_args)

    for arg in local_args:
        if arg.startswith('-pairsfile'):
            if len(arg) == len('-pairsfile'):
                filename = pywikibot.input('Enter the name of the file containing pairs:')
            else:
                filename = arg[len('-pairsfile:'):]
            oldName1 = None
            for page in pagegenerators.TextfilePageGenerator(filename):
                if oldName1:
                    fromToPairs.append([oldName1, page.title()])
                    oldName1 = None
                else:
                    oldName1 = page.title()
            if oldName1:
                pywikibot.warning(
                    'file {} contains odd number of links'.format(filename))
        elif arg == '-noredirect':
            options['noredirect'] = True
        elif arg == '-notalkpage':
            options['movetalkpage'] = False
        elif arg == '-always':
            options['always'] = True
        elif arg == '-skipredirects':
            options['skipredirects'] = True
        elif arg.startswith('-from:'):
            if oldName:
                pywikibot.warning('-from:{} without -to:'.format(oldName))
            oldName = arg[len('-from:'):]
        elif arg.startswith('-to:'):
            if oldName:
                fromToPairs.append([oldName, arg[len('-to:'):]])
                oldName = None
            else:
                pywikibot.warning('{} without -from'.format(arg))
        elif arg.startswith('-prefix'):
            if len(arg) == len('-prefix'):
                options['prefix'] = pywikibot.input('Enter the prefix:')
            else:
                options['prefix'] = arg[8:]
        elif arg.startswith('-summary'):
            if len(arg) == len('-summary'):
                options['summary'] = pywikibot.input('Enter the summary:')
            else:
                options['summary'] = arg[9:]

    if oldName:
        pywikibot.warning('-from:{} without -to:'.format(oldName))
    site = pywikibot.Site()
    for pair in fromToPairs:
        page = pywikibot.Page(site, pair[0])
        bot = MovePagesBot(**options)
        bot.moveOne(page, pair[1])

    gen = genFactory.getCombinedGenerator(preload=True)
    if gen:
        bot = MovePagesBot(generator=gen, **options)
        bot.run()
    elif not fromToPairs:
        pywikibot.bot.suggest_help(missing_generator=True)


if __name__ == '__main__':
    main()
