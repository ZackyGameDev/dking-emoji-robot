# -*- coding: UTF-8 -*-
import discord
from random import random
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.client.remove_command("help")
        
        # Getting the help messages from the docstrings of all the functions
        commands_list: list = list(self.client.commands)
        self.help_messages: list = [i.help for i in commands_list if i.help != None]
        self.help_messages.sort()
        self.help_message = "\n".join(self.help_messages)
    
    @commands.command() 
    async def ehelp(self, ctx: commands.Context):
        '''`-ehelp`:
        Shows this message'''

        await ctx.send(embed=discord.Embed(
            description=self.help_message,
            color=discord.Color.from_hsv(random(), 1, 1)
        ).set_author(
            name=f'{ctx.me}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.me.id}/{ctx.me.avatar}.png'
        ))

def setup(client):
    client.add_cog(HelpCommand(client))