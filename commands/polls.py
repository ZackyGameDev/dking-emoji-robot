# -*- coding: UTF-8 -*-

import discord
from random import *
from discord.ext import commands
from discord.utils import get
from utils.functions import console_log

class PollCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.client.remove_command("help")

    def check_count_reaction(self, desired_count, message):
        def predicate(reaction, user):
            return reaction.message == message and reaction.count>=desired_count
        return predicate   

    @commands.command()
    @commands.has_role('Owner')
    async def poll(self, ctx, question, Description='', Emotes='', *options: str):
        console_log("New poll created.")
        if len(options) <= 1:
            await ctx.send("```Error! A poll must have more than one option.```")
            return
        if len(options) > 2:
            await ctx.send("```Error! Poll can have no more than two options.```")
            return
        emote = Emotes.split(' ')
        if emote[0] in str(ctx.guild.emojis) and emote[1] in str(ctx.guild.emojis):
            reactions = [get(ctx.guild.emojis, name=emote[0]) , get(ctx.guild.emojis, name=emote[1])]
        else:
            reactions = ['👍', '👎']

        description = []
        description = Description
        for x, option in enumerate(options):
            description += '\n{} {}'.format(reactions[x], option)

        await ctx.message.delete()
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

        await commands.Bot.wait_for(self.client, 'reaction_add', 
                                       check=self.check_count_reaction(int(4), react_message))
        await ctx.send(embed=discord.Embed(
            title="Majority has voted!",
            color=discord.Colour.from_hsv(random(), 1, 1),
        ).set_author(
            name=f'{ctx.me}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.me.id}/{ctx.me.avatar}.png'
        ))
        msg = await ctx.fetch_message(react_message.id)
        Reacts = str(msg.reactions).split(',')

        results = "Votes in favour are: **{}**".format(Reacts[0].split('True count=')[1].replace('>','').replace(']',''))
        results = results + "\nVotes in not favour are: **{}**".format(Reacts[1].split('True count=')[1].replace('>','').replace(']',''))
        if int(Reacts[0].split('True count=')[1].replace('>','').replace(']','')) > int(Reacts[1].split('True count=')[1].replace('>','').replace(']','')): winner = "In Favour"
        else: winner = "Not in Favour"
#NICE
        users = set()
        for reaction in msg.reactions:
            async for user in reaction.users():
                users.add(user)
        results += f"\n\nUser Voted: {', '.join(user.name for user in users)}"
        await ctx.send(embed=discord.Embed(
            description= results,
            title=winner,
            color=discord.Colour.from_hsv(random(), 1, 1),
        ).set_author(
            name=f'{ctx.me}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.me.id}/{ctx.me.avatar}.png'
        ))

def setup(client):
    client.add_cog(PollCommands(client))
