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
    @commands.has_role('Owner')
    async def poll(self, ctx, question, Description='', Emotes='', *options: str):
        if len(options) <= 1:
            await ctx.send("```Error! A poll must have more than one option.```")
            return
        if len(options) > 2:
            await ctx.send("```Error! Poll can have no more than two options.```")
            return
        for i in ctx.guild.emojis:
            if i.animated: 
                emojis[f"{i.name}"]: str = f"<a:{i.name}:{i.id}>"
            else: 
                emojis[f"{i.name}"]: str = f"<:{i.name}:{i.id}>"
        emote = Emotes.split(' ')
        # Creating reply
        emojis: dict = {}
        for emoji in emojis: 
            options[0]: str = emote[0].replace(emoji, emojis[emoji])
            options[1]: str = emote[1].replace(emoji, emojis[emoji])
        if emote[0] in emojis and emote[1] in emojis:
            reactions = [options[0] , options[1]]
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
                                       check=self.check_count_reaction(int(3), react_message))
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
        #NICE
        if int(Reacts[0].split('True count=')[1].replace('>','').replace(']','')) > int(Reacts[1].split('True count=')[1].replace('>','').replace(']','')): winner = "In Favour"
        else: winner = "Not in Favour"
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
