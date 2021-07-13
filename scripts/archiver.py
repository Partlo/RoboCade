import pywikibot
import re
import time
from typing import Tuple


class ArchiveException(Exception):
    def __init__(self, message):
        self.message = message

class ArchiveCommand:

    def __init__(self, successful: bool, nom_type: str, article_name: str, suffix: str):
        self.successful = successful
        self.nom_type = nom_type
        self.article_name = article_name
        self.suffix = suffix

    @staticmethod
    def parse_command(command):
        """ Parses the nomination type, result, article name and optional suffix from the given command. """

        match = re.search("(?P<result>([Ss]uccessful|[Uu]nsuccessful|[Ff]ailed)) (?P<ntype>[CGFJ]A)N: (?P<article>.*?)(?P<suffix> \([A-z]+ nomination\))?$", command.strip())
        if not match:
            assert False, "Invalid command"

        result_str = match.groupdict().get('result', '').lower()
        if result_str == "successful":
            successful = True
        elif result_str == "unsuccessful" or result_str == "failed":
            successful = False
        else:
            assert False, f"Invalid result {result_str}"

        nom_type = match.groupdict().get('ntype')
        if nom_type not in ["CA", "GA", "FA"]:
            assert False, f"Unrecognized nomination type {nom_type}"

        article_name = match.groupdict().get('article')
        suffix = match.groupdict().get('suffix') or ''

        return ArchiveCommand(successful, nom_type, article_name, suffix)


# noinspection PyMethodMayBeStatic
class Archiver:
    def __init__(self, *, test_mode=False, auto=False):
        self.site = pywikibot.Site()
        self.site.login()
        self.test_mode = test_mode
        self.auto = auto
        self.talk_ns = "User talk" if self.test_mode else "Talk"

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

    def input_prompts(self, old_text, new_text):
        if self.auto:
            return

        pywikibot.showDiff(old_text, new_text, context=3)

        choice = pywikibot.input_choice(
            'Do you want to accept these changes?',
            [('Yes', 'y'), ('No', 'n')],
            default='N')
        if choice == 'n':
            assert False

    def archive_process(self, command: ArchiveCommand) -> Tuple[bool, str]:
        page = pywikibot.Page(self.site, self.prefix() + command.article_name)
        if not page.exists():
            return False, f"Target: {self.prefix() + command.article_name} does not exist"

        nom_page_name = f"{self.nom_pages[command.nom_type]}/{command.article_name}{command.suffix}"
        nom_page = pywikibot.Page(self.site, nom_page_name)
        if not nom_page.exists():
            return False, f"{nom_page_name} does not exist"

        talk_page = pywikibot.Page(self.site, f"{self.talk_ns}:{self.prefix() + command.article_name}")

        try:
            # Remove nomination subpage from nomination page
            print(f"Removing nomination from parent page")
            self.remove_nomination_from_parent_page(nom_type=command.nom_type, subpage=f"{command.article_name}{command.suffix}")

            print()
            time.sleep(1)

            # Apply archive template to nomination subpage
            print(f"Archiving {nom_page_name}")
            self.archive_nomination_page(nomination_page=nom_page, nom_type=command.nom_type, successful=command.successful)

            print()
            time.sleep(1)

            # Remove nomination template from the article itself (and add status if necessary)
            if command.successful:
                edit_comment = f"Successful {command.nom_type}N"
            else:
                edit_comment = f"Unsuccessful {command.nom_type}N"
            print(f"Marking {command.article_name} as {edit_comment}")
            self.edit_target_article(page=page, successful=command.successful, nom_type=command.nom_type, edit_comment=edit_comment)

            print()
            time.sleep(1)

            # Calculate the revision IDs for the nomination
            completed, nominated = self.calculate_revisions(page=page, nom_type=command.nom_type, edit_comment=edit_comment)

            # Create or update the talk page with the {Ahm} status templates
            self.update_talk_page(talk_page=talk_page, nom_type=command.nom_type, successful=command.successful,
                                  nom_page_name=nom_page_name, nominated=nominated, completed=completed)

            print()
            time.sleep(1)

            # Update nomination history
            self.update_nomination_history(
                nom_type=command.nom_type, page=page, nom_page_name=nom_page_name, successful=command.successful,
                nominated_revision=nominated, completed_revision=completed)
        except AssertionError as e:
            print(e)
            return False, self.extract_err_msg(e)
        except Exception as e:
            print(e)
            return False, self.extract_err_msg(e)

        print("Done!")
        return True, ""
        
    def extract_err_msg(self, e):
            try:
                return str(e.args[0] if str(e.args[0]).startswith('(') else e.args)
            except Exception as _:
                return str(e.args)

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
            assert False, f"Cannot find /{subpage} in nomination page"

        self.input_prompts(text, new_text)

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
            if line == "<!-- DO NOT WRITE BELOW THIS LINE! -->":
                continue
            elif not found and self.categories[nom_type] in line:
                found = True
            else:
                new_lines.append(line)
        new_lines.append("</div>")

        new_text = "\n".join(new_lines)
        if not found:
            assert False, f"Cannot find category in nomination page"

        self.input_prompts(text, new_text)

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

        self.input_prompts(text, new_text)

        history_page.put(new_text, f"Archiving {nom_page_name}")

    def edit_target_article(self, *, page, successful, nom_type, edit_comment):
        text = page.get()
        nt = "CA" if nom_type == "JA" else nom_type
        
        if successful:
            former_status = None
            match = re.search("{{[Tt]op.*?\|([cgf]a)[|}]", text)
            if match:
                former_status = match.group(1)

            text1 = re.sub("({{[Tt]op.*?)\|f?[cgf]a([|}])", "\\1\\2", text)
            text2 = re.sub("{{[Tt]op([|\}])", f"{{{{Top|{nt.lower()}\\1", text1)
            if text1 == text2:
                assert False, "Could not add status to {{Top}} template"
        else:
            text2 = text
        text3 = re.sub("{{" + nt + "nom[|}].*?\n", "", text2)
        if text2 == text3:
            assert False, "Could not remove nomination template from page"

        self.input_prompts(text, text3)

        page.put(text3, edit_comment)

        return former_status

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
            assert False, "Could not find completed revision"
        elif nominated_revision is None:
            assert False, "Could not find nomination revision"
        return completed_revision, nominated_revision

    def update_talk_page(self, *, talk_page, nom_type, successful, nom_page_name, nominated, completed):
        """ Updates the talk page of the target article with the appropriate {{Ahm}} templates, and updates the {{Ahf}}
          status. Also adds a {{Talkheader}} template if necessary. """

        nom_type = "CA" if nom_type == "JA" else nom_type
        result = "Success" if successful else "Failure"
        status = nom_type if successful else f"F{nom_type}N"

        history_text = f"""{{{{Ahm
|date={nominated['timestamp'].strftime('%B %d, %Y')}
|oldid={nominated['revid']}
|process={nom_type}N
|result={result}
}}}}
{{{{Ahm
|date={completed['timestamp'].strftime('%B %-d, %Y')}
|link={nom_page_name}
|process={status}
|oldid={completed['revid']}
}}}}
{{{{Ahf|status={status}}}}}"""

        if not talk_page.exists():
            text = f"""{{{{Talkheader}}}}
{{{{{nom_type}}}}}
{{{{Ahh}}}}
{history_text}"""

            self.input_prompts("", text)
            talk_page.put(text, "Creating talk page with article nomination history")
            return

        text = talk_page.get()
        lines = text.splitlines()
        new_lines = []
        if "{{ahf|" in text.lower():
            if successful:
                new_lines.append(f"{{{{{nom_type}}}}}")
            found = False
            for line in lines:
                if "{{ahf|" in line.lower():
                    new_lines.append(history_text)
                    found = True
                    continue
                new_lines.append(line)
            if not found:
                assert False, "Could not find {ahf} template"

        elif "{{talkheader" not in text.lower():
            if successful:
                new_lines = ["{{Talkheader}}", f"{{{{{nom_type}}}}}", history_text, *lines]
            else:
                new_lines = ["{{Talkheader}}", history_text, *lines]

        else:
            if successful:
                new_lines.append(f"{{{{{nom_type}}}}}")
            found = False
            for line in lines:
                if not found and not line.startswith("{") and not line.startswith("|"):
                    found = True
                    new_lines.append(history_text)
                new_lines.append(line)

        new_text = "\n".join(new_lines)

        self.input_prompts(text, new_text)

        talk_page.put(new_text, "Updating talk page with article nomination history")


def main(*args):

    archiver = Archiver(test_mode=False, auto=False)

    archiver.archive_process("Successful GAN: Oseon 8920")


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
