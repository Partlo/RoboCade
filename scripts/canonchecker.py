import pywikibot
from pywikibot import pagegenerators, textlib
from pywikibot.data.api import Request
import codecs
import re


class CanonChecker:
    def __init__(self, articles=None, *args):
        self.counter = 0
        self.articles = articles
        self.site = pywikibot.getSite()
        self.parenthetical = False
        self.fix = False
        first_page = None
        all_pages = False
        text_file_name = None

        for arg in pywikibot.handleArgs(*args):
            if arg.startswith('-start'):
                if len(arg) == 6:
                    first_page = pywikibot.input(
                        u'At which page do you want to start?')
                else:
                    first_page = arg[6:]
            elif arg == '-paren':
                self.parenthetical = True
            elif arg == '-all':
                all_pages = True
            elif arg.startswith('-filename'):
                text_file_name = arg[10:]
                if not text_file_name:
                    text_file_name = pywikibot.input(
                        u'Please enter the local file name:')

        if all_pages:
            if first_page is None:
                first_page = pywikibot.input(
                    u'At which page do you want to start?')
            namespace = pywikibot.Page(self.site, first_page).namespace()
            first_page_title = pywikibot.Page(self.site, first_page).title(withNamespace=False)
            self.gen = pagegenerators.AllpagesPageGenerator(first_page_title,
                                                            namespace,
                                                            includeredirects='only')
        elif text_file_name:
            self.gen = pagegenerators.TextfilePageGenerator(text_file_name)

    def run(self):
        result = {"First Order-Resistance conflict", "Lorrd/Canon", "Vibroblade/Canon", "Cesta/Canon", "Turret droid/Canon", "Venator-class Star Destroyer/Canon", "Asajj Ventress/Canon", "Desert Plain/Canon", "Grand Walkway/Canon", "Holorecorder/Canon", "Immobilizer 418", "Slick's platoon/Canon", "Heavy repeating blaster/Canon", "Settlement", "Valc/Canon", "Low Altitude Assault Transport/Canon", "Emergency Powers Act/Canon", "Dug debris loader/Canon", "Fly/Canon", "Thalassia/Canon", "Ando Prime Centrum/Canon", "Twi'leks", "Mugaar/Canon", "Chrome/Canon", "Radnor/Canon", "Quartermaster/Canon", "Loovria/Canon", "Droid attack flare/Canon", "Zeb Orrelios", "Tent/Canon", "Barracks/Canon", "Yanjon/Canon", "Phaeda/Canon", "Starships", "Controller/Canon", "Unidentified Gotal bounty hunter/Canon", "Point Tarron/Canon", "Cluster missile/Canon", "Deepdock/Canon", "Plasma torch/Canon", "Kyuzo war helmet", "Silver Sea/Canon", "Lucazec system/Canon", "Firefight", "Rex", "Star Wars: Story Before The Force Awakens", "Ship-scale disruptors", "Champalan Embassy/Canon", "Padme Amidala", "Holographic projector/Canon", "Repulsorfield", "Defoliator/Canon", "Shimmersilk/Canon", "Velcar sector/Canon", "Hovertrain/Canon", "Star Wars Rebels: Season One", "Entralla/Canon", "Marg Sabl/Canon", "R2D2", "Domed city/Canon", "Bimmiel/Canon", "Second Battle of Florrum/Canon", "Treaty of Malastare/Canon", "TriPlanetary Press/Canon", "Dagoyan Masters", "Artificial intelligence/Canon", "Homing missile/Canon", "Lemcke/Canon", "Daalang/Canon", "Sensor array/Canon", "Shaum Hii/Canon", "Waldo Flats/Canon", "Fern/Canon", "ACD-950 Podracer/Canon", "Life Support/Canon", "Moon Goddess/Canon", "Corellian Run/Canon", "Translator droid/Canon", "Sergeant Major", "Exhaust port", "Umbaran airbase/Canon", "Wiyentaah/Canon", "Meteor shower/Canon", "Resolute/Canon", "Galactic Courts of Justice/Canon", "Chief Petty Officer/Canon", "Han's heavy blaster pistol", "Stone Guardian/Canon", "Armory/Canon", "Bravo Five/Canon", "Grevious", "Seraph-class urban landspeeder/Canon", "Voice modulator/Canon", "Lawquane farmstead/Canon", "Rishi moon/Canon", "Comm unit/Canon", "Sienar Advanced Projects Laboratory/Canon", "Safe/Canon", "Mechanic/Canon", "Rebel Alliance", "Womb/Canon", "Nub/Canon", "Dubrillion/Canon", "2000 BBY/Canon", "Hour", "Unidentified Concordia city/Canon", "6000 BBY/Canon", "Baobab Publishing/Canon", "Braata/Canon", "Rishi Station/Canon", "Subspace radio/Canon", "Fertilizer/Canon", "Mission to Oba Diah (pre-Naboo Crisis)", "Bandfill/Canon", "Star Wars: The Force Awakens Beginner's Game", "Place of Sickness/Canon", "Farana/Canon", "Lorahns/Canon", "Warrick family/Canon", "Scanner/Canon", "Clone commander", "Bush/Canon", "Intellex V/Canon", "Sublight drive/Canon", "Stasis/Canon", "Republic frigate", "Stun cuffs/Canon", "Force", "Container ship/Canon", "Grievous's Recusant-class light destroyer/Canon", "Concussion grenade launcher/Canon", "Christophsian/Canon", "Flimsi/Canon", "Uscru Entertainment District/Canon", "Lake/Canon", "Saddle/Canon", "Nuknog/Canon", "S-130 Shelter speeder/Canon", "Epaulet/Canon", "Theed Power Generator", "Circular saw/Canon", "Garnac's hunting guild/Canon", "Longe Voltrans/Canon", "501st Legion/Canon", "Rebel base/Canon", "Hyperwave transceiver/Canon", "Desevro/Canon", "Polycarbonate/Canon", "Blasters", "Doctor Aphra", "Rey's Survival Guide", "Mos Eisley Cantina", "Zygerrian slave ship", "Riflor/Canon", "Laser rifle/Canon", "Holoscreen/Canon", "Shipwrights' Trace/Canon", "Clan Mother", "Jedi Temple communication center/Canon", "Count Dooku", "Tarkin", "Unidentified Neimoidian envoy/Canon", "Iziz power generator/Canon", "Double jocimer/Canon", "Clay/Canon", "Supreme Commander of the Droid Army/Canon", "Dark Side of the Force", "Hilt/Canon", "Clone cadet/Canon", "Prime minister", "Wrist blaster/Canon", "Bescane/Canon", "Trian/Canon", "Bomb/Canon", "Taggart (smuggler)/Canon", "Shadowlands/Canon", "Senate Chamber", "Kalinda/Canon", "Tonnika sisters/Canon", "Rishi/Canon", "Devil's Doorknob/Canon", "Rishi Moon", "Saber throw", "The Whip/Canon", "Life-support module/Canon", "Obi-wan kenobi", "Star Wars: Republic 50: The Defense of Kamino", "Power coupling/Canon", "New Cov/Canon", "Mission to rescue Admiral Ackbar", "E'Y-Akh Desert/Canon", "Bacta patch/Canon", "Kerane Valley/Canon", "Jump trooper", "Fleet/Canon", "Pintle gun/Canon", "Toydarian Royal Delegation/Canon", "Fleet Command/Canon", "Petty Officer/Canon", "Dorenian Beshniquel/Canon", "Battle of Abregado/Canon", "Palace District/Canon", "Chancellor", "Echani/Canon", "Kaminoan (language)/Canon", "Herdessa/Canon", "Pad Nine", "Unidentified OOM command battle droid (Christophsis)/Canon", "Staff/Canon", "Barrel (weapon part)/Canon", "Confederacy of Independent Systems/Canon", "Officer/Canon", "Paradise Road/Canon", "Power pack/Canon", "23 ABY/Canon", "Vandyne/Canon", "Thugs of Thule/Canon", "Papanoida's Coruscant apartment/Canon", "Null/Canon", "Holographer/Canon", "Doctor Aphra 1: Aphra, Part I", "Poison dart/Canon", "Borosk/Canon", "Communications relay/Canon", "70 BBY/Canon", "Oil/Canon", "Galactic Republic/Canon", "Clown/Canon", "MandalTech/Canon", "Otoh Villages/Canon", "Hover train/Canon", "University of Rudrig/Canon", "Articles of Secession/Canon", "Cyphar/Canon", "Hok/Canon", "Pad nine", "Flour/Canon", "Ciutric/Canon", "Pune Zignat/Canon", "The Redoubt/Canon", "Bank of the Core/Canon", "Jedi Temple/Canon", "Survival capsule/Canon", "Starfighter combat/Canon", "Raxus system/Canon", "Clone Trooper", "Frangawl shrine/Canon", "Dagoyan Temple", "773/Canon", "Eyes", "Proximity mine/Canon", "Rudrig/Canon", "Aeten/Canon", "Bounty hunters", "Tarrin/Canon", "Dragon snake bog", "Medkit/Canon", "Jabba", "ARC-170 starfighter", "Star Wars: Darth Maul&mdash;Son of Dathomir 2", "Darth Vader", "Acceleration compensator/Canon", "Heavy laser cannon/Canon", "Velmor/Canon", "Fives", "Repeating blaster/Canon", "Destroyer/Canon", "Frangawl shrine", "First Order Military", "Cad Bane's Munificent-class star frigate/Canon", "Holomap/Canon", "Ion bomb/Canon", "General Grievous", "Plankton/Canon", "Captain Rex", "Cody", "Vergence/Canon", "Keitum/Canon", "Transponder code/Canon", "US Magazine Collector's Edition - Star Wars Rogue One", "Pulse bomb/Canon", "Rocket launcher", "Empire", "Lifeform scanner/Canon", "FX-series", "Chieftain/Canon", "Tipoca City/Canon", "Christophsis blockade/Canon", "7G", "Llanic system/Canon", "Imperial escort carrier/Canon", "Twi'lek freedom fighters hideout/Canon", "Vriichon brothers/Canon", "Macroscope/Canon", "Mon Gazza/Canon", "Iskalon/Canon", "Kriselist/Canon", "Kril'dor/Canon", "Processional Way/Canon", "Spartan/Canon", "Sonic emitter/Canon", "B1 battle droids", "Tunic/Canon", "The Corkscrew/Canon", "Salvage yard/Canon", "Blizzard 4/Canon", "Thyferra/Canon", "Aleen system/Canon", "Rail jet/Canon", "Landing craft/Canon", "Plo Koon's Delta-7B Aethersprite-class light interceptor", "Geonosian War Room/Canon", "Stone guardian/Canon", "Humans", "Temple district/Canon", "City Bigspace/Canon", "Meet the Rebels", "Boonta/Canon", "Fornax/Canon", "Chief of State (Alliance)/Canon", "Frigate/Canon", "Monastery/Canon", "Concussion grenade/Canon", "Particle shield/Canon", "Electropole/Canon", "Gate", "City Municipal Authorities Building/Canon", "Dead Man's Turn/Canon", "D-Squad's Maxillipede shuttle/Canon", "Chalcedon/Canon", "Nova Star Medal of the Empire/Canon", "Ardra/Canon", "Death Watch hideout/Canon", "ID transponder", "Plo's Bros/Canon", "Glass/Canon", "Mytus/Canon", "Propaganda Bureau/Canon", "Fencing/Canon", "Magnetic field/Canon", "Sun/Canon", "Sapphire/Canon", "BT30 quadra-Podracer/Canon", "Farstine/Canon", "Unidentified Imperial officer (Freighter 651)", "Kwenn/Canon", "Theed Spaceport/Canon", "Rush Clovis's office/Canon", "501st", "Commander Cody", "B'Thazoshe Bridge/Canon", "Ogoth Tiir/Canon", "Happyland/Canon", "Rago/Canon", "Fungi/Canon", "Alarm system/Canon", "Minister of Industry/Canon", "Generis/Canon", "Cetacean/Canon", "Slugthrower rifle/Canon", "Borgo Prime/Canon", "Plasma rocket/Canon", "Indupar/Canon", "BT310 quadra-Podracer/Canon", "Steps Into Shadow", "Alpha-3 Nimbus", "Ruhau-whale/Canon", "Gray Three/Canon", "Luminara Unduli's lightsaber/Canon", "Sith alchemy/Canon", "Sonic blaster/Canon", "Picador/Canon", "Onderonian/Canon", "Sauce/Canon", "Assault rifle/Canon", "Feline/Canon", "Nut/Canon", "Thermite/Canon", "Bellnar", "Holocomm/Canon", "Land mine/Canon", "Alliance Diplomatic Corps/Canon", "Chang/Canon", "Howdah/Canon", "The Notch/Canon", "Citadel Challenge/Canon", "Zealots of Psusan/Canon", "Bardotta system/Canon", "Disease/Canon", "Temple District/Canon", "Faya/Canon", "Mission to Jabba's Palace (Darth Vader)", "Force Choke/Canon", "Porcine/Canon", "Genassa/Canon", "Tibanna/Canon", "Jiroch/Canon", "Barb Mentir/Canon", "Heavy turbolaser turret/Canon", "Interpreter droid/Canon", "Fil/Canon", "Shad (city)/Canon", "Kaal/Canon", "Republic Senate non-communication law/Canon", "Escape pod/Canon", "Kamino/Canon", "Jedi ambassador shuttle", "Aqua droid/Canon", "Silver/Canon", "Point-defense laser cannon", "Eopie stew/Canon", "North Ridge/Canon", "Dennogra/Canon", "Dyne 577 radial atomizer engine/Canon", "Illuminator/Canon", "Birgis/Canon", "Aduba/Canon", "Kay-Tap square/Canon", "Namadii/Canon", "Chekkoo Enclave/Canon", "Diablo Cut/Canon", "PLEX rocket launcher/Canon", "Planet/Canon", "Duffel bag/Canon", "Garlic/Canon", "Rintonne/Canon", "Separatist Nightmare/Canon", "Utapese/Canon", "Wingmate/Canon", "Plastex/Canon", "Bad Kitty/Canon", "50 BBY/Canon", "Toydarian palace/Canon", "Living sphere/Canon", "Spa/Canon", "Sculptor/Canon", "Jellyfish/Canon", "Fresia/Canon", "Doctor Aphra 2: Aphra, Part II", "Belasco/Canon", "Nixor/Canon", "Neuranium/Canon", "Group Two/Canon", "Unidentified Umbaran airbase/Canon", "Lothal Year", "Life support/Canon", "G'wenee/Canon", "Star Wars: The Force Awakens, Part II", "Division/Canon", "Outer Curved Street/Canon", "Rishi eel/Canon", "CD-3.2 hyperdrive/Canon", "Coruscant power generator engineer/Canon", "Unidentified Zillo Beast/Canon", "Outer Rim", "Ring/Canon", "Star Wars: Princess Leia, Part V", "Ord Pardorn/Canon", "Bravo Three/Canon", "Charros/Canon", "Lothal Imperial Naval Academy", "Biocomputer/Canon", "99/Canon", "Seswenna Sector/Canon", "Doonium/Canon", "Jaemus/Canon", "Window/Canon", "Koro-2 all-environment Exodrive airspeeder/Canon", "Hindane Darcc/Canon", "Mushroom/Canon", "Prospector/Canon", "Marauder/Canon", "Bonadan Embassy/Canon", "Randon/Canon", "Hyperspace beacon/Canon", "Groin popper/Canon", "Byss (Outer Rim Territories)/Canon", "Entralla Route/Canon", "Frangawl sacrificial ceremony/Canon", "Cat/Canon", "Holofeed/Canon", "B1 battle droid/Canon", "Ministry of Economic Development/Canon", "Reugeot 905", "Algae/Canon", "Riley's sibling", "Retrothruster", "Translator unit/Canon", "Silk/Canon", "Halmad/Canon", "Star map", "BX-series droid commando/Canon", "Chant of Resurrection/Canon", "Theta-class shuttle", "Author/Canon", "Friday/Canon", "Unidentified T-series tactical droid (Naboo)/Canon", "Energy binder/Canon", "Ketaris/Canon", "Kit Fisto's Delta-7B Aethersprite-class light interceptor/Canon", "Horizontal booster/Canon", "Imperial Starfighter Corps", "Mind Trick", "Icefall Plains/Canon", "Helska/Canon", "Ozu/Canon", "Clone trooper pilot/Canon", "Mollusk/Canon", "Marshal/Canon", "Lefrani/Canon", "Bow/Canon", "Star Wars Rogue One Ultimate Visual Guide", "Molator/Canon", "Ord Trasi/Canon", "Sonic Grenade/Canon", "Tion Cluster/Canon", "Docking ring/Canon", "Battle droid/Canon", "Winter/Canon", "Bread/Canon", "Camera/Canon", "Quarren city/Canon", "Crustacean/Canon", "Holowan Mechanicals/Canon", "Laser cutter/Canon", "Ord Bueri/Canon", "Mama the Hutt's house/Canon", "Jedi Council/Canon", "Low Altitude Assault Transport carrier", "Mass-driver cannon/Canon", "Aleena (language)/Canon", "Unidentified T-series tactical droid (Christophsis)/Canon", "Vegetable/Canon", "Enarc/Canon", "Mutant/Canon", "Shock rod/Canon", "Historian/Canon", "Kalarba/Canon", "Trade route/Canon", "Nez Peron/Canon", "Lahsbane/Canon", "Laserball/Canon", "Sneeve/Canon", "Daalang system/Canon", "Battlecruiser/Canon", "Power suit/Canon", "Unit 26/Canon", "Custard/Canon", "Mortar gun", "Atrivis sector/Canon", "Mortician/Canon", "Giju Run/Canon", "Thermal detonators", "Hunting rifle/Canon", "Maul", "Iego council/Canon", "Wood/Canon", "Keyboard/Canon", "Blowtorch/Canon", "Slaving collar/Canon", "Obi-Wan Kenobi's Arquitens-class light cruiser/Canon", "Ord Biniir/Canon", "Reactor core", "Bank/Canon", "Balamak/Canon", "Ray Shield Fortress/Canon", "Deysum/Canon", "Platoon/Canon", "Arms Emporium/Canon", "Mystic/Canon", "Cake/Canon", "Wrist comm/Canon", "Contruum/Canon", "Disney-Lucasfilm Press", "Umbaran Airbase", "Buzz saw/Canon", "Bioluminescence/Canon", "Moltok/Canon", "TIE striker", "Mortar/Canon", "Nubian Design Collective/Canon", "Point-defense laser cannon/Canon", "Execute Battalion/Canon", "Shinie/Canon", "Lorta/Canon", "Heavy blaster rifle/Canon", "Bravo Squad/Canon", "Trench's flagship/Canon", "Cut Lawquane's farmstead/Canon", "Grand Army of the Republic broadcast/Canon", "Garrison/Canon", "Sabine My Rebel Sketchbook", "Zardossa Stix Pyramid/Canon", "Star Wars: Princess Leia, Part IV", "Lola Sayu defense fleet/Canon", "Aquarium/Canon", "Orrineswa River/Canon", "Gemologist/Canon", "Phosphorus/Canon", "Claw/Canon", "CT-327/Canon", "Dagger/Canon", "Togoria/Canon", "Mind trick/Canon", "Sernpidal/Canon", "Attack droid/Canon", "Star Wars: Darth Vader 3: Vader, Part III", "Computer virus/Canon", "Geyser/Canon", "Nass", "Antenna/Canon", "Subspace radio", "Dwartii/Canon", "Level 5/Canon", "Library/Canon", "Gyro-stabilizer", "Sarka/Canon", "R series", "Theft of the Death Star plans", "Torpedo/Canon", "Throne/Canon", "The Pits/Canon", "Banqueting rotunda/Canon", "Yelsain/Canon", "Nanth'ri system/Canon", "Nexus Ortai/Canon", "Edusa/Canon", "Skin glider/Canon", "Heavy pulse cannon/Canon", "Coruscant Ministry of Ingress/Canon", "Banker/Canon", "Reena University/Canon", "Sinkhole/Canon", "Larva/Canon", "Jestefad/Canon", "Special Forces", "Gemon-4 ion engine/Canon", "Atmosphere/Canon", "CT-00-2010/Canon", "Shad Furies/Canon", "Cutup", "Celanon Spur/Canon", "Koorivar homeworld/Canon", "Geonosians", "Plug-F Mammoth Split-X engine/Canon", "Iziz rebel safe house/Canon", "Coronet/Canon", "Delta-7B Aethersprite-class interceptor", "Sublight thruster/Canon", "Dentaal/Canon", "Core Founder/Canon"}
        skip = set()
        counter = 0
        params = {'action': 'query', 'prop': ['info']}
        store = False

        Rlink = re.compile(r'\[\[(?P<title>[^\]\|\[]*)(\|[^\]]*)?\]\]')
        try:
            for page in self.gen:
                counter += 1
                pywikibot.output('%s    %s' % (counter, page.title()))
                try:
                    this_text = textlib.removeLanguageLinks(page.get(get_redirect=True), page.site())
                except pywikibot.NoPage:
                    pywikibot.output("Error: %s is not a page" % page.title())
                    continue
                except pywikibot.IsRedirectPage:
                    pywikibot.output("Error: %s is a redirect" % page.title())
                    continue
                except pywikibot.SectionError:
                    return []
                this_text = textlib.removeCategoryLinks(this_text, page.site())
                this_text = textlib.removeDisabledParts(this_text)
                this_text = self.site().resolvemagicwords(this_text)

                for match in Rlink.finditer(this_text):
                    title = match.group('title')
                    title = title.replace("_", " ").strip(" ")
                    if title.startswith("#"):
                        # this is an internal section link
                        continue
                    if not page.site().isInterwikiLink(title):
                        title = title[0].capitalize() + title[1:]
                        if title in result:
                            continue
                        elif title in skip:
                            continue
                        params['titles'] = title
                        query = Request(**params)
                        data = query.submit()

                        try:
                            if 'missing' in data['query']['pages'].values()[0] and title.endswith('/Canon'):
                                store = True
                            if 'redirect' in data['query']['pages'].values()[0]:
                                store = True
                        except KeyError:
                            print "Error encountered while processing %s" % title
                            print data['query']

                        if store and title not in result:
                            pywikibot.output('Bad Link:    %s' % title)
                            result.add(title)
                        else:
                            skip.add(title)
                        store = False
        finally:
            for x in result:
                self.articles.write(u'%s\n' % x)
                self.articles.flush()

    def split_line(self):
        if self.counter % 100:
            return ''
        else:
            pywikibot.output("%s lines" % self.counter)
            return (u'<!-- ***** %dth title is above this line. ***** -->\n'
                    % self.counter)


def main(*args):
    append = False
    filename = "tor.txt"
    try:
        title_file = codecs.open(filename, encoding='utf-8',
                                 mode=(lambda x: x and 'a' or 'w')(append))
    except IOError:
        pywikibot.output("%s cannot be opened for writing." %
                         filename)
        return
    checker = CanonChecker(title_file)

    try:
        checker.run()
    finally:
        if title_file:
            title_file.close()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
