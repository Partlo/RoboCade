import pywikibot
import re
import time

pages = {
    "User:Cade Calrayn/Project Jocasta/Nominations": """{{Title-shortcut|WP:CAN}}
{{Wookieepedia:Comprehensive_article_nominations/Header}}
<div style="border:2px solid #c6d9f0; padding:.5em 1em 1em 1em; border-top:none;">
[[File:Premium-ComprehensiveArticle.svg|right|80px]]
This page is for '''Comprehensive article nominations'''. A [[Wookieepedia:Comprehensive articles|Comprehensive article]] is an article that adheres to certain quality standards but cannot reach [[Wookieepedia:Good articles|Good]] or [[Wookieepedia:Featured articles|Featured status]] due to its limited content. On this page, users can nominate articles that they believe are ready to be reviewed to achieve Comprehensive status.

The article-nomination process is not a way to showcase your favorite articles, but rather articles that are of high quality. Articles placed on this page will be extensively reviewed by experienced editors, including the presiding [[Wookieepedia:EduCorps|EduCorps]] review panel. The nomination process will require the article nominator to respond to objections and improve the article until the requisite number of users supports the nomination.

In undertaking a nomination on this page, the nominator is taking responsibility for their nominated article. This means they need to thoroughly read the following instructions, implement them into their nominated article, and respond to given objections. Nominators are encouraged to ask more experienced editors for guidance and assistance, but self-sufficiency is a requirement of the article-nomination process. It is not inherently the job of reviewers to rewrite elements of an article, but rather to guide nominators to be able to fix issues themselves.

Your nomination is your responsibility. Nominations that severely neglect the following rules or otherwise fall idle after one week will be subject to immediate removal.

*[[Wookieepedia:Comprehensive article nominations/History|Comprehensive article nominations history]]
*[[Wookieepedia:Comprehensive article nominations/instructions|Comprehensive article checklist]]

<center><span style="font-variant: small-caps; font-size: 20px">'''READ THIS FIRST!'''</span> </center>

----
<big>''A Comprehensive article must&hellip;''</big>

#&hellip;be well-written and comprehensively detailed.
#&hellip;be unbiased, with a [[Wookieepedia:Neutral point of view|neutral point of view]].
#&hellip;have comprehensive Appearances and Sources lists.
#&hellip;be fully referenced, including all quotes and images. See [[Wookieepedia:Sourcing]] for more information.
#&hellip;follow the [[Wookieepedia:Manual of Style|Manual of Style]], [[Wookieepedia:Layout Guide|Layout Guide]], and all other [[:Category:Policies on Wookieepedia|policies on Wookieepedia]].
#&hellip;be stable during and following the review process. This means the article does not change significantly from day to day with new content and is not the subject of ongoing edit wars. This does not apply to [[Wookieepedia:Vandalism|vandalism]] or other administrative edits, such as [[Wookieepedia:Protection policy|page protection]].
#&hellip;not be tagged with any sort of improvement tags (i.e. more sources, expand, etc).
#&hellip;have no redlinks.
#&hellip;provide at least one quote on the article if available. A leading quote at the beginning of the article is preferred but not required if no quotes are available. Although quotes may be placed in the body of the article, a maximum of one quote is allowed at the beginning of each section or subsection.
#&hellip;include a "Behind the scenes" section for [[in-universe]] articles.
#&hellip;include a reasonable number of images of the highest quality to illustrate the article, as source availability permits.
#&hellip;provide an introduction that gives a good summary of the topic if it reaches 165 words, not counting the "Behind the scenes" section (not including captions, quotes, headers, etc). Conversely, an article must not have an introduction if it is less than 165 words, not counting the "Behind the scenes" section. For clarification, please refer to [[:File:NominationFlowchart.png|this flowchart]].
#&hellip;not exceed 250 words in length if it provides an introduction. This word total counts the introduction, the article body, and "Behind the scenes" material, but not captions, quotes, headers, etc. However, any article that does not provide an introduction per Rule #12 is eligible to be nominated for Comprehensive status regardless of word count. For clarification, please refer to [[:File:NominationFlowchart.png|this flowchart]].
#&hellip;not be deliberately shortened if it approaches the 250-word limit.
#&hellip;be properly titled in accordance with Wookieepedia's treatment of [[Canon]] and [[Star Wars Legends|Legends]] articles; i.e., no nomination may have "/Canon" in the title.

----
<big>''How to nominate:''</big>

#Select an article you feel is worthy of Comprehensive status. Nominated articles must meet all fifteen requirements stated above.
#Add {{Tl|CAnom}} at the top of the article you are nominating, and save the page. Please note that if the article you are nominating has been nominated for Comprehensive article status previously, you will need to specify the number of the nomination as a parameter (e.g. {{Tlp|CAnom|second}}).
#Open the redlink in a new tab to create the nomination page, modifying the preloaded instructions as necessary.
#Copy the code provided to the [{{fullurl:Wookieepedia:Comprehensive article nominations|action=edit&section=1}} bottom of this page].
#[[Help:Purge|Purge the article]] to update the template.
#Other users will object to the nomination with issues and suggested improvements (errors, style, organization, images, notability, sources, etc).
#The nominator should then adjust the article until the objections are satisfied. The objector is responsible for striking their objection when it has been addressed, not the nominator. Additionally, reviewers will often copy-edit the article themselves as desired to fix any issues.
#Following their review, other users will vote to support the nomination. Users may not vote on their own nomination.
#Each user shall be limited to four active Comprehensive article nominations at any given time. Any additional nominations will be subject to immediate removal.
#Users must successfully complete one Comprehensive article nomination before they can have two nominations active on the CAN page at one time. Likewise, users must complete two successful CA nominations before they can have three, and three successful CA nominations before they can have four.

----
<big>''How to review:''</big>

#To review an article, users should read the article completely, keeping a sharp eye out for mistakes.
#The article should be reviewed with the criteria listed above, and any issues should be placed under the '''Object''' section of the article's nomination page. Objections should be clearly explained, and detail how the article can be improved.
#Objections should then be addressed by the nominator. Once the objector is satisfied, they should strike their objection. The nominator should not strike reviewers' objections for them.
#Once a reviewer is satisfied with the article, they can vote to support it. Please note that in order to support a nomination, you must have 50 mainspace edits.
#If a nomination has been active for over one week and has no active objections, it may pass with a total of either three [[Wookieepedia:EduCorps|EduCorps]] votes or two EduCorps and three user votes. Alternatively, if a nomination is between two and seven days old and has no active objections, it can pass with a total of four EduCorps votes.
#Once the nomination is successful, the article will be considered a "Comprehensive article." As such, an EduCorps member will archive the nomination, tag the article with the {{Tlp|Top|ca}} template, tag its talk page with the {{Tl|CA}} template, and place the article on the Comprehensive articles page. Only members of the EduCorps are allowed to perform these archiving tasks.

----
<center>'''All nominations will be considered idle and are subject to immediate removal by EduCorps vote if objections are not addressed after a period of 1 week.'''</center>

'''Note:''' Reduxed articles require only three support votes to maintain their Comprehensive status, all of which must come from EduCorps members. Reduxed articles will be subject to immediate removal if objections are not addressed after a period of 10 days, pending the support of at least three EduCorps members.
</div>
<br />
{{TOClimit|4}}


=Comprehensive article nominations=

{{/Sample}}

{{/Target (second nomination)}}

{{/Extra}}
""",
    "User:Cade Calrayn/Project Jocasta/Nominations/Target (second nomination)": """==[[Korvalus Tower]]==
*'''Nominated by''': [[User:Cade Calrayn|<span style="font-weight: bold; color:#890400;">Cade</span>]] [[File:StupidRepublicEmblem-Traced-TORkit.svg|18px]] [[User talk:Cade Calrayn|<span style="font-weight: bold; color:#890400;">Calrayn</span>]] 19:04, 30 June 2021 (UTC)
*'''Nomination comments''': grumble

{{CANvotes|Wookieepedia:Comprehensive article nominations/Korvalus Tower (second nomination)}}
====Support====
#'''[[User:IFYLOFD|<span style="color:darkorange">IFYLOFD</span>]]''' <sup>([[User talk:IFYLOFD|<span style="color:black">Talk</span>]])</sup> 14:18, 1 July 2021 (UTC)
#{{EC}} [[User:OOM 224|<span style="font-family:franklin gothic;color:#d1a111">OOM 224</span>]] [[User talk:OOM 224|<span style="color:#11711c">'''<sup>༼༽talk༼༽</sup>'''</span>]] 20:17, 7 July 2021 (UTC)

====Object====
=====Floyd=====
*<s>One question: Does "turbolaser" need to be capitalized throughout? In most other articles and appearances it isn't.</s> '''[[User:IFYLOFD|<span style="color:darkorange">IFYLOFD</span>]]''' <sup>([[User talk:IFYLOFD|<span style="color:black">Talk</span>]])</sup> 02:22, 1 July 2021 (UTC)
**It's not a traditional turbolaser, it's a [[Firestorm Turbolaser]], which is a proper name. [[User:Cade Calrayn|<span style="font-weight: bold; color:#890400;">Cade</span>]] [[File:StupidRepublicEmblem-Traced-TORkit.svg|18px]] [[User talk:Cade Calrayn|<span style="font-weight: bold; color:#890400;">Calrayn</span>]] 03:42, 1 July 2021 (UTC)
***Fair enough, threw me off a bit when I was reading it. '''[[User:IFYLOFD|<span style="color:darkorange">IFYLOFD</span>]]''' <sup>([[User talk:IFYLOFD|<span style="color:black">Talk</span>]])</sup> 14:18, 1 July 2021 (UTC)

=====CC-8=====
*If the player goes inside the tower is there any details about the interior that can be described? [[User:Commander Code-8|<b><span style="color: Purple">Commander Code-8</span></b>]] <sup>[[User talk:Commander Code-8|<span style="color: Maroon">Hello There!</span>]]</sup> 03:30, 5 July 2021 (UTC)
**Done. [[User:Cade Calrayn|Cade Calrayn]] ([[User talk:Cade Calrayn|talk]])

=====OOM=====
*<s>I'm just going to skim-review this because I haven't finished the Jedi Knight storyline yet, but there's an inconsistency between "the Korvalus Tower" and simply "Korvalus Tower." Which one is correct?</s>
**It's only mentioned in the quest log and the map name, and the quest log says "the Korvalus Tower Turbolaser". It's unclear but I just went with Korvalus Tower.
*<s>Only the immediate location of the tower and the planet it's on is needed in the infobox</s>
**Done.
*<s>Quote should be mentioned in the article body itself. Also, seeing that the body is getting rather long, I'd use a paragraph break there.</s> [[User:OOM 224|<span style="font-family:franklin gothic;color:#d1a111">OOM 224</span>]] [[User talk:OOM 224|<span style="color:#11711c">'''<sup>༼༽talk༼༽</sup>'''</span>]] 08:48, 7 July 2021 (UTC)
**Did the paragraph break, but I don't see what you're talking about with the quote. It's self-explanatory and the context is given in the discussion of Operation Firestorm. [[User:Cade Calrayn|Cade Calrayn]] ([[User talk:Cade Calrayn|talk]]) 20:06, 7 July 2021 (UTC)
***Fair enough, seems like I missed that bit [[User:OOM 224|<span style="font-family:franklin gothic;color:#d1a111">OOM 224</span>]] [[User talk:OOM 224|<span style="color:#11711c">'''<sup>༼༽talk༼༽</sup>'''</span>]] 20:17, 7 July 2021 (UTC)

====Comments====

<!-- DO NOT WRITE BELOW THIS LINE! -->
<noinclude>{{SpecialCategorizer|[[Category:Project Jocasta test pages|{{SUBPAGENAME}}]]}}</noinclude>
""",
    "User:Cade Calrayn/Project Jocasta/Target": """{{Top|leg}}
{{CAnom|second}}
{{Structure
|image=[[File:Fray_Landing_Memorial.png]]
|name=Fray Landing Memorial
|constructed=Between [[3640 BBY|3640]]<ref name="Encyclopedia">''[[Star Wars: The Old Republic Encyclopedia]]'' establishes that the [[Battle of Ilum]], and the finale of the base game of ''[[Star Wars: The Old Republic]]'', occurred in [[3640 BBY]].</ref>&ndash;[[3638 BBY]]<ref name="Time">{{TOR_updates|1.7}}</ref>[[xyz]]
|destroyed=
|location=[[Western Ice Shelf]], [[Ilum/Legends|Ilum]]<ref name="Codex">{{TORcite|type=codex|Fray Landing}}</ref>{{Top|ca}}
|poi=
|rebuilt=
|builder=[[Republic Military/Legends|Republic Military]]<ref name="Codex" />
|height=
|width=
|affiliation=[[Galactic Republic/Legends|Galactic Republic]]<ref name="Codex" />}}
{{Quote|Remember Fray!|A rallying cry inspired by the memorial|Star Wars: The Old Republic}}
'''Fray Landing Memorial''' was a memorial constructed by the [[Republic Military/Legends|Republic Military]] at the site of the [[Galactic Republic/Legends|Galactic Republic's]] [[Fray Landing Base]] on the [[Western Ice Shelf]] of the [[Planet/Legends|planet]] [[Ilum/Legends|Ilum]] to commemorate the lives lost at the base during the early days of the [[Battle of Ilum]] against the [[Sith Empire (Post–Great Hyperspace War)|Sith Empire]]<ref name="Codex">{{TORcite|type=codex|Fray Landing}}</ref> in [[3640 BBY]],<ref name="Encyclopedia" /> when Imperial forces overran Fray Landing. Consisting of a torch sconce, the memorial was built by other Republic [[Soldier/Legends|soldiers]]<ref name="Codex" /> sometime before the [[Gree (species)/Legends|Gree]] [[Species/Legends|species]] took over the Western Ice Shelf<ref name="Event">{{TORcite|type=event|Return of the Gree}}</ref> in [[3638 BBY]].<ref name="Time" /> "Remember Fray" became a rallying cry among the Republic as the war continued, and the battle there helped [[Supreme Chancellor/Legends|Supreme Chancellor]] [[Leontyne Saresh]] secure a massive increase in military spending.<ref name="Codex" />

==Behind the scenes==
Fray Landing Memorial was introduced to the [[BioWare]] [[video game]] ''[[Star Wars: The Old Republic]]'' in [[2013]] with Game Update 1.7: Return of the Gree.<ref name="Codex" /> The Memorial is located at the former site of the Republic faction's PvP base on Ilum; Game Update 1.7 overhauled the Western Ice Shelf and removed the PvP zone from the base, renaming it to Fray Landing.<ref name="Patch1-7">{{TORweb|url=/patchnotes/1.7.0/return-gree|text=Game Update 1.7: Return of the Gree|archivedate=20130215181739}}</ref> In [[January]] [[2012]], the early days of player-vs-player combat on the planet Ilum, combat imbalance between the two factions after Game Update 1.1 allowed Imperial players were able to repeatedly push all the way into the then-unnamed Republic base. Republic players were immediately killed by mobs of Imperials upon respawning in the base,<ref name="YouTube">{{Youtube|video=TL0kDP_Cexo|text=This is Ilum - Patch 1.1 (Republic Perspective)|channel=UCCN2DcCbII6OAS-wDuTAmhg|channelname=suzpaz|archivedate=20120403162737}}</ref> necessitating an emergency patch to fix the issue.<ref name="Patch">{{TORweb|url=/patchnotes/1.1.0a/1192012|text=Patch Notes 1/19/2012|archivedate=20120205071534}}</ref>

==Appearances==
*''[[Star Wars: The Old Republic]]'' {{1st}}

==Notes and references==
{{Reflist}}

[[Category:Monuments and memorials]]
[[Category:Western Ice Shelf locations]]
"""
}


# noinspection PyMethodMayBeStatic
class Archiver:
    def __init__(self):
        self.site = pywikibot.Site()
        self.test_mode = False
        # self.test_mode = True
        self.talk_ns = "User talk" if self.test_mode else "Talk"

        # for name, text in pages.items():
        #     page = pywikibot.Page(self.site, name)
        #     if name == "User:Cade Calrayn/Project Jocasta/Target":
        #         page.put(text, "Added CAnom")
        #     else:
        #         page.put(text, "Resetting")
        #     time.sleep(1)
        # print()


    nom_pages = {
        "JA": "User:Cade Calrayn/Project Jocasta/Nominations",
        "CA": "Wookieepedia:Comprehensive article nominations",
        "GA": "Wookieepedia:Good article nominations",
        "FA": "Wookieepedia:Featured article nominations"
    }

    categories = {
        "JA": "Category:Project Jocasta test pages",
        "CA": "Category:Wookieepedia Comprehensive article nomination pages",
        "GA": "Category:Wookieepedia Good article nomination pages",
        "FA": "Category:Wookieepedia Featured article nomination pages"
    }

    def prefix(self):
        if self.test_mode:
            return "User:Cade_Calrayn/Project_Jocasta/"
        return ""

    def archive_process(self, arg):
        # "CAN: Matteus Zaym (second nomination)"
        match = re.search("(?P<result>(Successful|Unsuccessful|Failed)) (?P<ntype>[CGFJ]A)N: (?P<article>.*?)(?P<suffix> \([A-z]+ nomination\))?$", arg)
        if not match:
            assert False, "Invalid command"

        result_str = match.groupdict().get('result')
        if result_str == "Successful":
            successful = True
        elif result_str == "Unsuccessful" or result_str == "Failed":
            successful = False
        else:
            assert False

        nom_type = match.groupdict().get('ntype')
        if nom_type not in self.nom_pages:
            assert False

        article_name = match.groupdict().get('article')
        suffix = match.groupdict().get('suffix', '')

        page = pywikibot.Page(self.site, self.prefix() + article_name)
        if not page.exists():
            assert False, f"Target: {self.prefix() + article_name} does not exist"

        nom_page_name = f"{self.nom_pages[nom_type]}/{article_name}{suffix}"
        nom_page = pywikibot.Page(self.site, nom_page_name)
        if not nom_page.exists():
            assert False, f"{nom_page_name} does not exist"

        talk_page = pywikibot.Page(self.site, f"{self.talk_ns}:{self.prefix() + article_name}")

        # Remove nomination subpage from nomination page
        print(f"Removing nomination from parent page")
        self.remove_nomination_from_parent_page(nom_type=nom_type, subpage=f"{article_name}{suffix}")

        print()
        time.sleep(1)

        # Apply archive template to nomination subpage
        print(f"Archiving {nom_page_name}")
        self.archive_nomination_page(nomination_page=nom_page, nom_type=nom_type, successful=successful)

        print()
        time.sleep(1)

        # Remove nomination template from the article itself (and add status if necessary)
        # if successful:
        #     edit_comment = f"Successful {nom_type}N"
        # else:
        #     edit_comment = f"Unsuccessful {nom_type}N"
        # print(f"Marking {article_name} as {edit_comment}")
        # self.edit_target_article(page=page, nom_type=nom_type, edit_comment=edit_comment)

        print()
        time.sleep(1)

        edit_comment = "CA"

        # Calculate the revision IDs for the nomination
        completed_revision, nominated_revision = self.calculate_revisions(page=page, nom_type=nom_type, edit_comment=edit_comment)

        # Create or update the talk page with the {Ahm} status templates
        # self.update_talk_page(talk_page=talk_page, nom_type=nom_type, successful=successful, nom_page_name=nom_page_name,
        #                       nominated_revision=nominated_revision, completed_revision=completed_revision)

        print()
        time.sleep(1)

        # Update nomination history
        self.update_nomination_history(nom_type=nom_type, page=page, nom_page_name=nom_page_name, successful=successful,
                                       nominated_revision=nominated_revision, completed_revision=completed_revision)

    def remove_nomination_from_parent_page(self, *, nom_type, subpage):
        """ Removes the {{/<nom title>}} transclusion from the parent nomination page. """

        parent_page = pywikibot.Page(self.site, self.nom_pages[nom_type])
        if not parent_page.exists():
            assert False, f"{self.nom_pages[nom_type]} does not exist"

        expected = "{{/" + subpage + "}}"
        print(expected)

        text = parent_page.get()
        if expected not in text:
            assert False, f"Cannot find /{subpage} in nomination page"

        lines = text.splitlines()
        new_lines = []
        found = False
        white = False
        for line in lines:
            if not found:
                if line.strip() == expected:
                    found = True
                    white = True
                else:
                    new_lines.append(line)
            elif white:
                if line.strip() != "":
                    new_lines.append(line)
                    white = False
            else:
                new_lines.append(line)
        new_text = "\n".join(new_lines)
        if not found:
            assert False

        parent_page.put(new_text, f"Archiving {subpage}")

    def archive_nomination_page(self, *, nomination_page, nom_type, successful):
        """ Applies the {nom_type}_archive template to the nomination page. """

        text = nomination_page.get()
        result = "successful" if successful else "unsuccessful"

        lines = text.splitlines()
        nt = "CA" if nom_type == "JA" else nom_type
        new_lines = [f"{{{{subst:{nt} archive|{result}}}}}"]
        found = False
        for line in lines:
            if not found and self.categories[nom_type] in line:
                found = True
            else:
                new_lines.append(line)

        new_text = "\n".join(new_lines)
        if not found:
            assert False

        nomination_page.put(new_text, f"Archiving {result} nomination")

    def determine_title_format(self, *, page):
        """ Examines the target article's usage of {{Top}} and extracts the title= and title2= parameters, in order to
          generate a properly-formatted pipelink to the target. """

        text = page.get()
        page_title = page.title().replace(self.prefix(), "")

        pagename = re.match("{{[Tt]op\|[^\n]+\|title=''{{PAGENAME}}''", text)
        if pagename:
            return f"''[[{page_title}]]''"

        title1 = None
        title_match = re.match("{{[Tt]op\|[^\n]+\|title=(?P<title>.*?)[|}]", text)
        if title_match:
            title1 = title_match.groupdict()['title']
            if title1 == f"''{page_title}''":
                return f"''[[{page_title}]]''"

        match = re.match("^(?P<title>.+?) \((?P<paren>.*?)\)$", page_title)
        if match:
            title2 = None
            title2_match = re.match("{{[Tt]op\|[^\n]+\|title2=(?P<title>.*?)[|}]", text)
            if title2_match:
                title2 = title2_match.groupdict()['title']

            if title1 or title2:
                title1 = title1 or match.groupdict()['title']
                title2 = title2 or match.groupdict()['paren']
                return f"[[{page_title}|{title1} ({title2})]]"
            else:
                return f"[[{page_title}]]"
        elif title1 and title1 != page_title:
            return f"[[{page_title}|{title1}]]"
        else:
            return f"[[{page_title}]]"

    def update_nomination_history(self, nom_type, successful, page, nom_page_name, nominated_revision, completed_revision):
        result = "Success" if successful else "Failure"
        formatted_link = self.determine_title_format(page=page)
        nom_date = nominated_revision['timestamp'].strftime('%Y/%m/%d')
        end_date = completed_revision['timestamp'].strftime('%Y/%m/%d')

        new_row = f"|-\n|{formatted_link}||{nom_date}||{end_date}||[[{nom_page_name}|{result}]]"

        history_page = pywikibot.Page(self.site, f"{self.nom_pages[nom_type]}/History")
        text = history_page.get()
        new_text = text.replace("|}", new_row + "\n|}")
        history_page.put(new_text, f"Archiving {nom_page_name}")

    def edit_target_article(self, *, page, nom_type, edit_comment):
        text = page.get()
        nt = "CA" if nom_type == "JA" else nom_type

        text1 = re.sub("({{[Tt]op.*?)\|f?[cgf]a([|}])", "\\1\\2", text)
        if text == text1:
            assert False
        text2 = re.sub("{{[Tt]op([|\}])", f"{{{{Top|{nt.lower()}\\1", text1)
        if text1 == text2:
            assert False
        text3 = re.sub("{{" + nt + "nom[|}].*?\n", "", text2)
        if text2 == text3:
            assert False

        page.put(text3, edit_comment)

    def calculate_revisions(self, *, page, nom_type, edit_comment):
        """ Examines the target article's revision history to identify the revisions where the nomination template was
         added and removed. """

        nominated_revision = None
        completed_revision = None
        nt = "CA" if nom_type == "JA" else nom_type
        for revision in page.revisions():
            if revision['comment'] == edit_comment:
                completed_revision = revision
            if f"Added {nt}nom" in revision['tags'] or revision['comment'] == f"Added {nt}nom":
                nominated_revision = revision
                break

        if completed_revision is None:
            assert False
        elif nominated_revision is None:
            assert False
        return completed_revision, nominated_revision

    def update_talk_page(self, *, talk_page, nom_type, successful, nom_page_name, nominated_revision, completed_revision):
        """ Updates the talk page of the target article with the appropriate {{Ahm}} templates, and updates the {{Ahf}}
          status. Also adds a {{Talkheader}} template if necessary. """

        nom_type = "CA" if nom_type == "JA" else nom_type
        result = "Success" if successful else "Failure"
        status = nom_type if successful else f"F{nom_type}N"

        history_text = f"""{{{{Ahm
|date={nominated_revision['timestamp'].strftime('%B %d, %Y')}
|oldid={nominated_revision['revid']}
|process={nom_type}N
|result={result}
}}}}
{{{{Ahm
|date={completed_revision['timestamp'].strftime('%B %d, %Y')}
|link={nom_page_name}
|process={nom_type}
|oldid={completed_revision['revid']}
}}}}
{{{{Ahf|status={status}}}}}"""

        if not talk_page.exists():
            text = f"""{{{{Talkheader}}}}
{{{{{nom_type}}}}}
{{{{Ahh}}}}
{history_text}"""
            talk_page.put(text, "Creating talk page with article nomination history")
            return

        text = talk_page.get()
        lines = text.splitlines()
        new_lines = []
        if "{{ahf|" in text.lower():
            found = False
            for line in lines:
                if "{{ahf|" in line.lower():
                    new_lines.append(history_text)
                    found = True
                    continue
                new_lines.append(line)
                if not found:
                    assert False

        elif "{{talkheader" not in text.lower():
            new_lines = ["{{Talkheader}}", history_text, *lines]

        else:
            found = False
            for line in lines:
                if not found and not line.startswith("{") and not line.startswith("|"):
                    found = True
                    new_lines.append(history_text)
                new_lines.append(line)

        new_text = "\n".join(new_lines)
        talk_page.put(new_text, "Updating talk page with article nomination history")


def main(*args):

    archiver = Archiver()

    # archiver.archive_process("Successful JAN: Target (second nomination)")
    archiver.archive_process("Successful CAN: Korvalus Tower (second nomination)")


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
