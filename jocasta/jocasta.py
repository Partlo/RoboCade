from typing import Tuple
import time
from discord import Client, Message
from discord.abc import GuildChannel
from discord.channel import TextChannel
from scripts.archiver import Archiver, ArchiveCommand


MAIN = "wookieepedia"
NOM_CHANNEL = "article-nominations"


class JocastaBot(Client):
    """
    :type channels: dict[str, GuildChannel]
    :type emoji_storage: dict[str, int]
    """

    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        print("JocastaBot online!")

        self.archiver = Archiver(test_mode=False, auto=True)

        self.channels = {}
        self.emoji_storage = {}

    async def on_ready(self):
        print('Jocasta on as {0}!'.format(self.user))

        for c in self.get_all_channels():
            self.channels[c.name] = c

        for e in self.emojis:
            self.emoji_storage[e.name] = e.id

    # noinspection PyTypeChecker
    def text_channel(self, name) -> TextChannel:
        return self.channels[name]

    def emoji_by_name(self, name):
        if self.emoji_storage.get(name):
            return self.get_emoji(self.emoji_storage[name])
        return name

    def is_mention(self, message: Message):
        for mention in message.mentions:
            print(mention)
            if mention == self.user:
                return True
        return False

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if message.channel.name == "social":
            print(message.content)

        if not self.is_mention(message):
            return

        print(f'Message from {message.author}: [{message.content}]')

        if "Hello!" in message.content:
            await message.channel.send("Hello there!")
            return

        command = self.is_archive_command(message)
        if command:
            if message.channel.name != "article-nominations":
                pass
            elif message.author.display_name != "Cade Calrayn" and not any(r.name in ["AgriCorps", "EduCorps", "Inquisitorius"] for r in message.author.roles):
                await message.channel.send("Sorry, this command is restricted to members of the review panels.")
            else:
                await message.add_reaction("⏲️")
                archive_result, response = self.process_archive_command(command)
                await message.remove_reaction("⏲️", self.user)

                if archive_result:
                    await message.add_reaction(self.emoji_by_name(response))
                else:
                    await message.add_reaction("❗")
                    await message.channel.send(response)
            return

    def is_archive_command(self, message: Message):
        command = None
        try:
            command = ArchiveCommand.parse_command(message.content)
        except AssertionError as e:
            print(str(e.args))
        return command

    def process_test_command(self, command: ArchiveCommand):
        time.sleep(5)

        if command.article_name == "Fail":
            return True, False, "Something went wrong!"
        elif command.successful:
            return True, command.nom_type[:2]
        else:
            return True, "👍"

    def process_archive_command(self, command: ArchiveCommand) -> Tuple[bool, str]:

        result, msg, err_msg = False, None, None
        try:
            result, msg = self.archiver.archive_process(command)
        except Exception as e:
            try:
                err_msg = str(e.args[0])
            except Exception as _:
                err_msg = str(e.args)

        if result and command.successful:
            return True, command.nom_type[:2]
        elif result:
            return True, "👍"
        elif msg:
            return False, msg
        else:
            return False, err_msg


client = JocastaBot()

