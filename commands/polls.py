# -*- coding: UTF-8 -*-

import discord
from random import *
from discord.ext import commands

class PollCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.client.remove_command("help")

    @commands.command()
    async def poll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.send("```Error! A poll must have more than one option.```")
            return
        if len(options) > 2:
            await ctx.send("```Error! Poll can have no more than two options.```")
            return

        if len(options) == 2 and options[0] == "yes" and options[1] == "no":
            reactions = ['👍', '👎']
        elif options[0] in ctx.guild.emojis:
                reactions = [ctx.get(ctx.message.server.emojis, name=str(options[0])), ctx.get(ctx.message.server.emojis, name=str(options[1]))]
        else:
            reactions = ['👍', '👎']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}\n'.format(reactions[x], option)

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
        reaction = await ctx.wait_for_reaction([], react_message)
        await ctx.send("You responded with {}".format(reaction.emoji))

def setup(client):
    client.add_cog(PollCommands(client))
