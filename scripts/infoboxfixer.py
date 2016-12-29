import wikipedia as pywikibot
import pagegenerators
import codecs
import re


class Imager:
    def __init__(self, articles=None, *args):
        self.counter = 0
        self.articles = articles
        self.site = pywikibot.getSite()
        textfilename = None

        for arg in pywikibot.handleArgs(*args):
            if arg.startswith('-filename'):
                textfilename = arg[10:]
                if not textfilename:
                    textfilename = pywikibot.input(
                        u'Please enter the local file name:')
		
        if textfilename:
            self.gen = pagegenerators.TextfilePageGenerator(textfilename)

    def run(self):
		always = False
		for page in self.gen:
			text = page.get()
			name = page.title()
			print name
			try:
				new_text = text
				era_text = re.sub(r"\{\{[Ee]ras(\||\})", r"", text)
				if text == era_text:
					print "%s is missing {{Eras}}, adding" % name
					new_text = "{{Eras}}\n" + text
					pywikibot.showDiff(text, new_text)
					choice = pywikibot.inputChoice(u'Do you want to accept these changes?',
								['Yes', 'No', 'Quit'],
								['y', 'N', 'q'], 'N')
					if choice == 'q':
						break
					elif choice == 'y':
						pass
					else:
						pass
				# if new_text == re.sub(r"\|skin=", r"", new_text):
					# new_text = re.sub(r"\|cyber=", r"|skin=\n|cyber=", new_text)
				# if new_text == re.sub(r"\|cyber=", r"", new_text):
					# new_text = re.sub(r"\|era=", r"|cyber=\n|era=", new_text)
				
				new_text = re.sub(r"\| (.*?)=", r"|\1=", new_text)
				if new_text == re.sub(r"\|poi=", r"", new_text):
					new_text = re.sub(r"\|affiliation=", r"|poi=\n|affiliation=", new_text)
				if new_text == re.sub(r"\|imageBG=", r"", new_text):
					new_text = re.sub(r"\|image=", r"|imageBG=\n|image=", new_text)
					
				# if new_text != re.sub(r"\|casual2=\r\n\}\}", r"", new_text):
					# new_text = re.sub(r"\|casual2=\r\n\}\}", r"|casual2=\n|casual3=\n|casual4=\n|civilian=}}", new_text)
				# elif new_text != re.sub(r"\|casual2=\}\}", r"", new_text):
					# new_text = re.sub(r"\|casual2=\}\}", r"|casual2=\n|casual3=\n|casual4=\n|civilian=}}", new_text)
				# elif new_text == re.sub(r"\|casual3=", r"", new_text) and new_text == re.sub(r"\|casual4=", r"", new_text):
					# if new_text != re.sub(r"\|casual2=(([^\{]|\r\n)*?)\}\}", r"", new_text):
						# new_text = re.sub(r"\|casual2=(([^\{]|\r\n)*?)\}\}", r"|casual2=\1|casual3=\n|casual4=\n|civilian=}}", new_text)
						# new_text = re.sub(r"(.)\|casual3=", r"\1\n|casual3=", new_text)
					# else:
						# new_text = re.sub(r"\|casual2=", r"|casual3=\n|casual4=\n|civilian=\n|casual2=", new_text)
				# elif new_text != re.sub(r"\|casual3=", r"", new_text) and new_text == re.sub(r"\|casual4=", r"", new_text):
					# if new_text != re.sub(r"\|casual3=(([^\{]|\r\n)*?)\}\}", r"", new_text):
						# new_text = re.sub(r"\|casual3=(([^\{]|\r\n)*?)\}\}", r"|casual3=\1\n|casual4=\n|civilian=}}", new_text)
						# new_text = re.sub(r"(.)\|casual4=", r"\1\n|casual4=", new_text)
					# else:
						# new_text = re.sub(r"\|casual3=", r"|casual4=\n|civilian=\n|casual3=", new_text)
				# new_text = re.sub(r"\r\n\r\n\|casual(.)=", r"\r\n|casual\1=", new_text)
				# new_text = re.sub(r"\|civilian=\r\n\|civilian=", r"|civilian=", new_text)
				# new_text = re.sub(r"\|civilian=\r\n\|casual3=\r\n\|casual4=\r\n\|civilian=", r"|casual3=\n|casual4=\n|civilian=", new_text)
				if text != new_text:
					if always:
						page.put_async(new_text, "Adding missing parameters")
						continue
					else:
						pywikibot.showDiff(text, new_text)
						choice = pywikibot.inputChoice(u'Do you want to accept these changes?',
									['Yes', 'No', 'Always', 'Quit'],
									['y', 'N', 'a', 'q'], 'N')
						if choice == 'q':
							break
						elif choice == 'y':
							page.put_async(new_text, "Adding missing parameters")
							continue
						elif choice == 'a':
							page.put_async(new_text, "Adding missing parameters")
							always = True
							continue
						else:
							continue
			except Exception as e:
				print e
				continue
		
def main(*args):
	checker = Imager(*args)
	checker.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()