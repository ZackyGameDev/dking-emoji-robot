# -*- coding: UTF-8 -*-

import discord
from random import *
from discord.ext import commands
from discord.utils import get

class PollCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.client.remove_command("help")

    def check_count_reaction(self, desired_count, message):
        def predicate(reaction, user):
            return reaction.message == message and reaction.count>=desired_count
        return predicate   

    @commands.command()
    async def poll(self, ctx, question, Description='', *options: str):
        if len(options) <= 1:
            await ctx.send("```Error! A poll must have more than one option.```")
            return
        if len(options) > 2:
            await ctx.send("```Error! Poll can have no more than two options.```")
            return
        if len(options) == 2 and options[0] == "yes" and options[1] == "no":
            reactions = ['👍', '👎']
        else:
            reactions = ['👍', '👎']

        description = []
        description = Description
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)

        react_message = await ctx.send(embed=discord.Embed(
            title=question,
            color=discord.Colour.from_hsv(random(), 1, 1),
            description = ''.join(description)
        ).set_author(
            name=f'{ctx.author}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
        ))

        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

        await react_message.edit(embed=discord.Embed(
            title=question,
            color=discord.Colour.from_hsv(random(), 1, 1),
            description = ''.join(description)
        ).set_author(
            name=f'{ctx.author}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
        ))
        await commands.Bot.wait_for(self.client, 'reaction_add', 
                                       check=self.check_count_reaction(int(1), react_message))
        reaction = get(react_message.reactions, emoji='👍')
        if reaction.count >= 1: D = 'Vote is in favour'
        else: D = "Vote is in against the favour"
        await ctx.send(embed=discord.Embed(
            title="Majority has voted!",
            description=D,
            color=discord.Colour.from_hsv(random(), 1, 1),
        ).set_author(
            name=f'{ctx.me}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.me.id}/{ctx.me.avatar}.png'
        ))

def setup(client):
    client.add_cog(PollCommands(client))
