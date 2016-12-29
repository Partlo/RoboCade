import pywikibot
from pywikibot import pagegenerators

def main(*args):
    add_cat = None
    gen = None
    # summary message
    summary_commandline = False
    # Array which will collect commandline parameters.
    # First element is original text, second element is replacement text.
    commandline_replacements = []
    # A list of 2-tuples of original text and replacement text.
    replacements = []
    # Don't edit pages which contain certain texts.
    exceptions = {
        'title':         [],
        'text-contains': [],
        'inside':        [],
        'inside-tags':   [],
        'require-title': [],  # using a seperate requirements dict needs some
    }                         # major refactoring of code.

    # Should the elements of 'replacements' and 'exceptions' be interpreted
    # as regular expressions?
    regex = False
    # Predefined fixes from dictionary 'fixes' (see above).
    fix = None
    # the dump's path, either absolute or relative, which will be used
    # if -xml flag is present
    xmlFilename = None
    useSql = False
    PageTitles = []
    # will become True when the user presses a ('yes to all') or uses the
    # -always flag.
    acceptall = False
    # Will become True if the user inputs the commandline parameter -nocase
    caseInsensitive = False
    # Will become True if the user inputs the commandline parameter -dotall
    dotall = False
    # Will become True if the user inputs the commandline parameter -multiline
    multiline = False
    # Do all hits when they overlap
    allowoverlap = False
    # Do not recurse replacement
    recursive = False
    # This is the maximum number of pages to load per query
    maxquerysize = 60
    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()
    # Load default summary message.
    # BUG WARNING: This is probably incompatible with the -lang parameter.
    editSummary = i18n.twtranslate(pywikibot.getSite(), 'replace-replacing',
                                   {'description': u''})
    # Between a regex and another (using -fix) sleep some time (not to waste
    # too much CPU
    sleep = None
    # Do not save the page titles, rather work on wiki
    filename = None  # The name of the file to save titles
    titlefile = None  # The file object itself
    # If we save, primary behaviour is append rather then new file
    append = True
    # Default: don't write titles to exception file and don't read them.
    excoutfilename = None  # The name of the file to save exceptions
    excoutfile = None  # The file object itself
    # excinfilename: reserved for later use (reading back exceptions)
    # If we save exceptions, primary behaviour is append
    excappend = True

    # Read commandline parameters.
    for arg in pywikibot.handleArgs(*args):
        if arg == '-regex':
            regex = True
        elif arg.startswith('-xmlstart'):
            if len(arg) == 9:
                xmlStart = pywikibot.input(
                    u'Please enter the dumped article to start with:')
            else:
                xmlStart = arg[10:]
        elif arg.startswith('-xml'):
            if len(arg) == 4:
                xmlFilename = i18n.input('pywikibot-enter-xml-filename')
            else:
                xmlFilename = arg[5:]
        elif arg == '-sql':
            useSql = True
        elif arg.startswith('-page'):
            if len(arg) == 5:
                PageTitles.append(pywikibot.input(
                    u'Which page do you want to change?'))
            else:
                PageTitles.append(arg[6:])
        elif arg.startswith('-saveexcnew'):
            excappend = False
            if len(arg) == 11:
                excoutfilename = pywikibot.input(
                    u'Please enter the filename to save the excepted titles' +
                    u'\n(will be deleted if exists):')
            else:
                excoutfilename = arg[12:]
        elif arg.startswith('-saveexc'):
            if len(arg) == 8:
                excoutfilename = pywikibot.input(
                    u'Please enter the filename to save the excepted titles:')
            else:
                excoutfilename = arg[9:]
        elif arg.startswith('-savenew'):
            append = False
            if len(arg) == 8:
                filename = pywikibot.input(
                    u'Please enter the filename to save the titles' +
                    u'\n(will be deleted if exists):')
            else:
                filename = arg[9:]
        elif arg.startswith('-save'):
            if len(arg) == 5:
                filename = pywikibot.input(
                    u'Please enter the filename to save the titles:')
            else:
                filename = arg[6:]
        elif arg.startswith('-replacementfile'):
            if len(arg) == len('-replacementfile'):
                replacefile = pywikibot.input(
                    u'Please enter the filename to read replacements from:')
            else:
                replacefile = arg[len('-replacementfile')+1:]
            try:
                commandline_replacements.extend(
                    [x.lstrip(u'\uFEFF').rstrip('\r\n')
                     for x in codecs.open(replacefile, 'r', 'utf-8')])
            except IOError:
                raise pywikibot.Error(
               '\n%s cannot be opened. Try again :-)' % replacefile)
        elif arg.startswith('-excepttitle:'):
            exceptions['title'].append(arg[13:])
        elif arg.startswith('-requiretitle:'):
            exceptions['require-title'].append(arg[14:])
        elif arg.startswith('-excepttext:'):
            exceptions['text-contains'].append(arg[12:])
        elif arg.startswith('-exceptinside:'):
            exceptions['inside'].append(arg[14:])
        elif arg.startswith('-exceptinsidetag:'):
            exceptions['inside-tags'].append(arg[17:])
        elif arg.startswith('-fix:'):
            fix = arg[5:]
        elif arg.startswith('-sleep:'):
            sleep = float(arg[7:])
        elif arg == '-always':
            acceptall = True
        elif arg == '-recursive':
            recursive = True
        elif arg == '-nocase':
            caseInsensitive = True
        elif arg == '-dotall':
            dotall = True
        elif arg == '-multiline':
            multiline = True
        elif arg.startswith('-addcat:'):
            add_cat = arg[8:]
        elif arg.startswith('-summary:'):
            editSummary = arg[9:]
            summary_commandline = True
        elif arg.startswith('-allowoverlap'):
            allowoverlap = True
        elif arg.startswith('-query:'):
            maxquerysize = int(arg[7:])
        else:
            if not genFactory.handleArg(arg):
                commandline_replacements.append(arg)

    if pywikibot.verbose:
        pywikibot.output(u"commandline_replacements: " +
                         ', '.join(commandline_replacements))

    if (len(commandline_replacements) % 2):
        raise pywikibot.Error, 'require even number of replacements.'
    elif (len(commandline_replacements) == 2 and fix is None):
        replacements.append((commandline_replacements[0],
                             commandline_replacements[1]))
        if not summary_commandline:
            editSummary = i18n.twtranslate(pywikibot.getSite(),
                                           'replace-replacing',
                                           {'description': ' (-%s +%s)'
                                            % (commandline_replacements[0],
                                               commandline_replacements[1])})
    elif (len(commandline_replacements) > 1):
        if (fix is None):
            for i in xrange(0, len(commandline_replacements), 2):
                replacements.append((commandline_replacements[i],
                                     commandline_replacements[i + 1]))
            if not summary_commandline:
                pairs = [(commandline_replacements[i],
                           commandline_replacements[i + 1])
                         for i in range(0, len(commandline_replacements), 2)]
                replacementsDescription = '(%s)' % ', '.join(
                    [('-' + pair[0] + ' +' + pair[1]) for pair in pairs])
                editSummary = i18n.twtranslate(pywikibot.getSite(),
                                               'replace-replacing',
                                               {'description':
                                                replacementsDescription})
        else:
            raise pywikibot.Error(
                'Specifying -fix with replacements is undefined')
    elif fix is None:
        old = pywikibot.input(u'Please enter the text that should be replaced:')
        new = pywikibot.input(u'Please enter the new text:')
        change = '(-' + old + ' +' + new
        replacements.append((old, new))
        while True:
            old = pywikibot.input(
                u'Please enter another text that should be replaced,\n'
                u'or press Enter to start:')
            if old == '':
                change += ')'
                break
            new = i18n.input('pywikibot-enter-new-text')
            change += ' & -' + old + ' +' + new
            replacements.append((old, new))
        if not summary_commandline:
            default_summary_message = i18n.twtranslate(pywikibot.getSite(),
                                                       'replace-replacing',
                                                       {'description': change})
            pywikibot.output(u'The summary message will default to: %s'
                             % default_summary_message)
            summary_message = pywikibot.input(
                u'Press Enter to use this default message, or enter a ' +
                u'description of the\nchanges your bot will make:')
            if summary_message == '':
                summary_message = default_summary_message
            editSummary = summary_message

    else:
        # Perform one of the predefined actions.
        fixname = fix  # Save the name for passing to exceptions function.
        try:
            fix = fixes.fixes[fix]
        except KeyError:
            pywikibot.output(u'Available predefined fixes are: %s'
                             % fixes.fixes.keys())
            return
        if "regex" in fix:
            regex = fix['regex']
        if "msg" in fix:
            if isinstance(fix['msg'], basestring):
                editSummary = i18n.twtranslate(pywikibot.getSite(),
                                               str(fix['msg']))
            else:
                editSummary = pywikibot.translate(pywikibot.getSite(),
                                                  fix['msg'])
        if "exceptions" in fix:
            exceptions = fix['exceptions']
            # Try to append common extensions for multiple fixes.
            # It must be either a dictionary or a function that returns a dict.
            if 'include' in exceptions:
                incl = exceptions['include']
                if callable(incl):
                    baseExcDict = incl(fixname)
                else:
                    try:
                        baseExcDict = incl
                    except NameError:
                        pywikibot.output(
                            u'\nIncluded exceptions dictionary does not exist.'
                            u' Continuing with the exceptions\ngiven in fix.\n')
                        baseExcDict = None
                if baseExcDict:
                    for l in baseExcDict:
                        try:
                            exceptions[l].extend(baseExcDict[l])
                        except KeyError:
                            exceptions[l] = baseExcDict[l]
        if "recursive" in fix:
            recursive = fix['recursive']
        if "nocase" in fix:
            caseInsensitive = fix['nocase']
        try:
            replacements = fix['replacements']
            # enable regex/replacements as a dictionary for different langs
            if isinstance(replacements, dict):
                replacements = replacements[pywikibot.getSite().lang]
        except KeyError:
            pywikibot.output(
                u"No replacements given in fix.")
            return

    # Set the regular expression flags
    flags = re.UNICODE
    if caseInsensitive:
        flags = flags | re.IGNORECASE
    if dotall:
        flags = flags | re.DOTALL
    if multiline:
        flags = flags | re.MULTILINE

    # Pre-compile all regular expressions here to save time later
    for i in range(len(replacements)):
        old, new = replacements[i]
        if not regex:
            old = re.escape(old)
        oldR = re.compile(old, flags)
        replacements[i] = oldR, new

    for exceptionCategory in ['title', 'require-title',
                              'text-contains', 'inside']:
        if exceptionCategory in exceptions:
            patterns = exceptions[exceptionCategory]
            if not regex:
                patterns = [re.escape(pattern) for pattern in patterns]
            patterns = [re.compile(pattern, flags) for pattern in patterns]
            exceptions[exceptionCategory] = patterns

    if xmlFilename:
        try:
            xmlStart
        except NameError:
            xmlStart = None
        gen = XmlDumpReplacePageGenerator(xmlFilename, xmlStart,
                                          replacements, exceptions)
    elif useSql:
        whereClause = 'WHERE (%s)' % ' OR '.join(
            ["old_text RLIKE '%s'" % prepareRegexForMySQL(old.pattern)
             for (old, new) in replacements])
        if exceptions:
            exceptClause = 'AND NOT (%s)' % ' OR '.join(
                ["old_text RLIKE '%s'" % prepareRegexForMySQL(exc.pattern)
                 for exc in exceptions])
        else:
            exceptClause = ''
        query = u"""
SELECT page_namespace, page_title
FROM page
JOIN text ON (page_id = old_id)
%s
%s
LIMIT 200""" % (whereClause, exceptClause)
        gen = pagegenerators.MySQLPageGenerator(query)
    elif PageTitles:
        pages = [pywikibot.Page(pywikibot.getSite(), PageTitle)
                 for PageTitle in PageTitles]
        gen = iter(pages)

    gen = genFactory.getCombinedGenerator(gen)
    if not gen:
        # syntax error, show help text from the top of this file
        pywikibot.showHelp('replace')
        return

    preloadingGen = pagegenerators.PreloadingGenerator(gen,
                                                       pageNumber=maxquerysize)

    # Finally we open the file for page titles or set parameter article to None
    if filename:
        try:
            # This opens in strict error mode, that means bot will stop
            # on encoding errors with ValueError.
            # See http://docs.python.org/library/codecs.html#codecs.open
            titlefile = codecs.open(filename, encoding='utf-8',
                                    mode=(lambda x: x and 'a' or 'w')(append))
        except IOError:
            pywikibot.output("%s cannot be opened for writing." %
                             filename)
            return
    # The same process with exceptions file:
    if excoutfilename:
        try:
            excoutfile = codecs.open(
                excoutfilename, encoding='utf-8',
                mode=(lambda x: x and 'a' or 'w')(excappend))
        except IOError:
            pywikibot.output("%s cannot be opened for writing." %
                             excoutfilename)
            return
    bot = ReplaceRobot(preloadingGen, replacements, exceptions, acceptall,
                       allowoverlap, recursive, add_cat, sleep, editSummary,
                       titlefile, excoutfile)

    funcs = bot.run, bot.run
    for func in funcs:
        try:
            func()
        except urllib2.HTTPError:
            pass
        finally:
            # Just for the spirit of programming (they were flushed)
            if titlefile:
                titlefile.close()
            if excoutfile:
                excoutfile.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()