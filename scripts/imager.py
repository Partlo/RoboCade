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
        for page in self.gen:
			text = page.get()
			name = page.title()
			print name
			try:
				new_text = re.sub(r"\{\{Image\}\}\n", r"", text)
				new_text = re.sub(r"\|image=", r"|image=[[File:%s.png]]" % name, new_text)
				if text != new_text:
					pywikibot.showDiff(text, new_text)
					choice = pywikibot.inputChoice(u'Do you want to accept these changes?',
								['Yes', 'No', 'Quit'],
								['y', 'N', 'q'], 'N')
					if choice == 'q':
						break
					elif choice == 'y':
						page.put_async(new_text, "Adding image")
						continue
					else:
						continue
			except Exception as e:
				print e
				continue
		
def main(*args):
	filename = "images.txt"
	checker = Imager(*args)
	checker.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()