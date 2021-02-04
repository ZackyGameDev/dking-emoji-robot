# -*- coding: UTF-8 -*-
import discord
from random import random
from discord.ext import commands

help_message = """
`-e <text>`:
Use this command to use nitro emojis.
e.g. `-e sundarDasta is og`

`-erand \'optional text\' <randomOptionsToSelectFrom>`:
Use this command to let this bot choose from your arguments (emojis also supported)
e.g. `-erand sundarDasta 69`

`-ePing`:
See the latency of this robot

`-ehelp`:
Shows this message
"""

class HelpCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.client.remove_command("help")

    #code by DKING08 :)
    @commands.command() 
    async def ehelp(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(
            description=help_message,
            color=discord.Color.from_hsv(random(), 1, 1)
        ).set_author(
            name=f'{ctx.me}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.me.id}/{ctx.me.avatar}.png'
        ))

def setup(client):
    client.add_cog(HelpCommand(client))