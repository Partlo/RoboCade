from urllib2 import Request, urlopen, URLError
import urllib2
import datetime
import userlib
import wikipedia
import pagegenerators
import json
import ast


class InactiveChecker:
    def __init__(self, start=None):
        self.wook = wikipedia.getSite('en', 'starwars')
        self.current = datetime.datetime.utcnow()
        self.limit = 365
        self.editSummary = "Marking user as inactive"
        self.months = {"01": "January", "02": "February", "03": "March", "04": "April",
                       "05": "May", "06": "June", "07": "July", "08": "August",
                       "09": "September", "10": "October", "11": "November", "12": "December"}

        if start:
            gen = pagegenerators.AllpagesPageGenerator(start,
                                                       namespace=2,
                                                       site=self.wook)
        else:
            gen = pagegenerators.AllpagesPageGenerator(namespace=2,
                                                            site=self.wook)
        self.userList = pagegenerators.PreloadingGenerator(gen,
                                                           pageNumber=60)

    def getApiUrl(self, username, check=False):
        def pad(n):
            if n < 10:
                return '0' + str(n)
            else:
                return str(n)

        def ISODateString(d):
            result = str(d.year) + '-' + pad(d.month + 1) + '-' + pad(d.day) + 'T' + pad(d.hour) + ':' \
                     + pad(d.minute) + ':' + pad(d.second) + 'Z'
            return result

        if check:
            query = 'http://starwars.wikia.com' + \
                    '/api.php?action=query&list=usercontribs&ucnamespace=0&uclimit=1&ucprop=title|timestamp&format=json' + \
                    '&ucuser='  + urllib2.quote(username.encode("utf-8")) + \
                    '&ucstart=' + ISODateString(self.current) + \
                    '&ucend='   + ISODateString(self.current - datetime.timedelta(days=self.limit))
        else:
            query = 'http://starwars.wikia.com' + \
                    '/api.php?action=query&list=usercontribs&ucnamespace=0&uclimit=1&ucprop=title|timestamp&format=json' + \
                    '&ucuser='  + urllib2.quote(username.encode("utf-8"))
        return query

    def check_activity(self, user):
        # Check to make sure the user exists
        if user.username.find('/') != -1:
            if (user.username.find('/sig') != -1) or (user.username.find('/Sig') != -1):
                return "active subpage"
            new_user = userlib.User(self.wook, user.username.split('/')[0])
            result = self.check_activity(new_user)
            if result == "inactive":
                return "inactive subpage"
            else:
                return "active subpage"
        else:
            try:
                if user.exists():
                    if user.registrationTime() != 0:
                        reg = str(user.registrationTime(force=True))
                        registered = datetime.datetime(year=int(reg[0:4]),
                                                       month=int(reg[4:6]),
                                                       day=int(reg[6:8]),
                                                       hour=int(reg[8:10]),
                                                       minute=int(reg[10:12]),
                                                       second=int(reg[12:14]))
                        diff = self.current - registered
                        if diff.days < 365:
                            return "active"
                    request = Request(self.getApiUrl(user.username, check=True))
                    response = urlopen(request)
                    message = json.loads(response.read())
                    if len(message["query"]["usercontribs"]) > 0:
                        return "active"
                    else:
                        return "inactive"
                else:
                    return "dne"
            except userlib.InvalidUser:
                return "bad"

    def convert_date(self, datestr):
        year = datestr[0:4]
        month = self.months[datestr[5:7]]
        day = datestr[8:10]
        if day[0] == "0":
            day = day[1]

        return "%s %s, %s" % (month, day, year)

    def tag_inactive(self, page, subpage=False):
        excepttext = ["{{Inactive", "{{inactive",
                      "{{Doppelganger", "{{doppelganger",
                      "{{Confirmedsock", "{{confirmedsock",
                      "{{Suspectedsock", "{{suspectedsock",
                      "{{Sockpuppeteer", "{{sockpuppeteer",
                      "{{WikiaStaff", "{{wikiaStaff",
                      "{{Banned", "{{banned"]
        try:
            if subpage:
                if not page.isRedirectPage():
                    wikipedia.output(u'Redirecting subpage User:%s to inactive userpage.' % page.title())
                    new_text = "#REDIRECT [[User:%s]]" % page.title().split('/')[0][5:]
                    page.put(new_text, "Owner is inactive.")
                else:
                    wikipedia.output(u'User:%s is a subpage of an inactive user and is already redirected.' % page.title())
            else:
                userpage = page.getUserPage()
                if userpage.isRedirectPage():
                    wikipedia.output(u'Userpage for User:%s is a redirect.' % page.username)
                    return

                for text in excepttext:
                    if userpage.get().find(text) != -1:
                        wikipedia.output(u'User:%s is tagged.' % page.username)
                        return

                wikipedia.output(u'Tagging User:%s as inactive.' % page.username)
                request = Request(self.getApiUrl(page.username))
                response = urlopen(request)
                message = json.loads(response.read())
                if len(message["query"]["usercontribs"]) > 0:
                    last_edit = self.convert_date(message["query"]["usercontribs"][0]["timestamp"])
                    new_text = "{{Inactive|%s}}" % last_edit
                else:
                    new_text = "{{Inactive|None}}"
                    userpage.put(new_text, comment=self.editSummary)

        except wikipedia.LockedPage:
            wikipedia.output("Not permitted to edit page.")
        except wikipedia.NoUsername:
            wikipedia.output("Not permitted to edit page.")

    def run(self):
        for userpage in self.userList:
            # Create User item
            user = userlib.User(self.wook, userpage.title()[5:])
            result = self.check_activity(user)

            if result == "active":
                wikipedia.output(u'User:%s is an active user.' % user.username)
                continue
            elif result == "inactive":
                self.tag_inactive(user)
            elif result == "inactive subpage":
                self.tag_inactive(userpage, subpage=True)
            elif result == "active subpage":
                #wikipedia.output(u'User:%s is a subpage of an active user.' % userpage.title())
                continue
            elif result == "dne":
                wikipedia.output(u'User %s does not exist.' % user.username)


def main(*args):
    start = None
    for arg in wikipedia.handleArgs(*args):
        if arg.startswith('-start'):
            if len(arg) == '6':
                start = wikipedia.input(
                    u'Please enter the userpage to start with:')
            else:
                start = arg[7:]
    checker = InactiveChecker(start)
    checker.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        wikipedia.stopme()