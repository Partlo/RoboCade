# -*- coding: utf-8  -*-
import pywikibot
from pywikibot import pagegenerators
from pywikibot.textlib import removeLanguageLinks, removeCategoryLinks, removeDisabledParts
from pywikibot.data.api import Request, APIError
import time
import codecs
import re

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def write_to_file(filename, results, header=None):
    try:
        output_file = codecs.open(filename, encoding='utf-8',
                                  mode=(lambda x: x and 'a' or 'w')(False))
    except IOError:
        pywikibot.output("%s cannot be opened for writing." % filename)
        return
    for x in results:
        output_file.write(u'%s\n' % x)
        output_file.flush()
    output_file.close()

def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    append = False
    filename = "tor.txt"
    source_file = None
    result_1 = set()
    result_2 = set()
    result_3 = set()
    skip = set()
    failed = []
    counter = 0
    store = False
    Rlink = re.compile(r'\[\[(?P<title>[^\]\|\[]*)(\|[^\]]*)?\]\]')

    gen_factory = pagegenerators.GeneratorFactory()

    for arg in pywikibot.handle_args(args):
        if arg.startswith('-filename'):
            source_file = arg[10:]
            if not source_file:
                source_file = pywikibot.input(u'Please enter the local file name:')
        else:
            gen_factory.handleArg(arg)

    if source_file:
        gen = pagegenerators.TextfilePageGenerator(source_file)
    else:
        gen = gen_factory.getCombinedGenerator()

    if gen:
        try:
            for page in gen:
                counter += 1
                pywikibot.output('%s    %s' % (counter, page.title()), toStdout=True)
                try:
                    this_text = removeLanguageLinks(page.get(get_redirect=True))
                except pywikibot.NoPage:
                    pywikibot.output("Error: %s is not a page" % page.title(), toStdout=True)
                    continue
                except pywikibot.IsRedirectPage:
                    pywikibot.output("Error: %s is a redirect" % page.title(), toStdout=True)
                    continue
                except pywikibot.SectionError:
                    return []
                this_text = removeCategoryLinks(this_text)
                this_text = removeDisabledParts(this_text)

                matches = []
                for match in Rlink.finditer(this_text):
                    title = match.group('title')
                    title = title.replace("_", " ").strip(" ")
                    if title.startswith("#") or title.lower().startswith("file:"):
                        continue
                    if page.site.isInterwikiLink(title):
                        continue

                    title = title[0].capitalize() + title[1:]
                    if title in result_1:
                        continue
                    elif title in result_2:
                        continue
                    elif title in skip:
                        continue
                    else:
                        matches.append(title)

                for titles in chunks(matches, 10):
                    title_list = '|'.join(titles)

                    data = None
                    num_requests = 3
                    while num_requests > 0:
                        try:
                            query = Request(action="query", site=page.site, prop=['info'], titles=title_list)
                            data = query.submit()
                        except:
                            print ": Sleeping for 2 seconds"
                            num_requests -= 1
                            time.sleep(2)
                        finally:
                            if data:
                                num_requests = 0

                    if not data:
                        print "ERROR"
                        failed.append('|'.join(titles))
                        continue

                    for i, p in data['query']['pages'].iteritems():
                        try:
                            if 'missing' in p:
                                pywikibot.output('Bad Link:    %s' % p['title'], toStdout=True)
                                if p['title'].endswith("/Canon"):
                                    result_1.add(p['title'])
                                else:
                                    result_3.add(p['title'])
                            elif 'redirect' in p:
                                pywikibot.output('Redirect:    %s' % p['title'], toStdout=True)
                                result_2.add(p['title'])
                            else:
                                skip.add(p['title'])
                        except KeyError:
                            print "Error encountered while processing page"
                            print p

                # for match in Rlink.finditer(this_text):
                #     title = match.group('title')
                #     title = title.replace("_", " ").strip(" ")
                #     if title.startswith("#"):
                #         # this is an internal section link
                #         continue
                #     if not page.site.isInterwikiLink(title):
                #         title = title[0].capitalize() + title[1:]
                #         if title in result:
                #             continue
                #         elif title in skip:
                #             continue
                #         try:
                #             query = Request(action="query", site=page.site, prop=['info'], titles=title)
                #             data = query.submit()
                #         except APIError:
                #             print "ERROR"
                #
                #         try:
                #             if 'missing' in data['query']['pages'].values()[0] and title.endswith('/Canon'):
                #                 store = True
                #             if 'redirect' in data['query']['pages'].values()[0]:
                #                 store = True
                #         except KeyError:
                #             print "Error encountered while processing %s" % title
                #             print data['query']
                #
                #         if store and title not in result:
                #             pywikibot.output('Bad Link:    %s' % title, toStdout=True)
                #             result.add(title)
                #         else:
                #             skip.add(title)
                #         store = False
        except KeyboardInterrupt:
            print "\nAborting run"
        finally:
            write_to_file("result_1.txt", result_1)
            write_to_file("redirects.txt", result_2)
            write_to_file("other_redlinks.txt", result_3)
            write_to_file("skip.txt", skip)
            write_to_file("failed.txt", failed)

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
