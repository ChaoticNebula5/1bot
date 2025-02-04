"""This file contains the client along with all events except the error event, which is in ./cogs/errors.py"""

import discord
from discord.ext import commands
from itertools import cycle
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button
from asyncio import sleep
from help_command import CustomHelpCommand


class Client(commands.AutoShardedBot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True

        # Initialising AutoShardedBot
        super().__init__(
            command_prefix=["1 ", "1"],
            case_sensitive=True,
            intents=intents,
            owner_ids=[748791790798372964, 825292137338765333],
        )

        """
        The line below makes the help command case insensitive so that you can run 'help fun' or 'help Fun'.
        """
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

    async def on_ready(self):
        print("-----\nThe bot is now online")
        print(f"{len(self.guilds)} servers\n-----")

        buttons = create_actionrow(
            *[
                create_button(
                    label="Command list",
                    style=ButtonStyle.URL,
                    emoji=self.get_emoji(885086857484992553),
                    url="https://1bot.netlify.app/commands",
                ),
                create_button(
                    label="Support Server",
                    style=ButtonStyle.URL,
                    emoji=self.get_emoji(885083336240926730),
                    url="https://discord.gg/KRjZaV9DP8",
                ),
                create_button(
                    style=ButtonStyle.URL,
                    label="Add me",
                    emoji=self.get_emoji(885088268314611732),
                    url="https://dsc.gg/1bot",
                ),
            ]
        )

        self.help_command = CustomHelpCommand(buttons)
        self.loop.create_task(self.change_status())

    # Send prefix when mentioned
    async def on_message(self, message):
        if (
            message.content == f"<@!{self.user.id}>"
            or message.content == f"<@{self.user.id}>"
        ):
            await message.channel.send(
                "My prefix is `1`. You can add a space after it, but it's optional."
            )
        else:
            await self.process_commands(message)

    # Changing status
    async def change_status(self):
        statuses = cycle(
            [
                "1 help | you can run my commands in DMs too!",
                "1 help | 1bot.netlify.app",
            ]
        )

        while not self.is_closed():
            await self.change_presence(activity=discord.Game(name=next(statuses)))
            await sleep(8)

    # Store message details when it is deleted

    sniped_messages = {}

    async def on_message_delete(self, message):
        if not message.guild:
            return

        try:
            self.sniped_messages[message.guild.id].update(
                {
                    message.channel.id: (
                        message.content,
                        message.author,
                        message.channel,
                        message.created_at,
                    )
                }
            )
        except KeyError:
            self.sniped_messages[message.guild.id] = {
                message.channel.id: (
                    message.content,
                    message.author,
                    message.channel,
                    message.created_at,
                )
            }
