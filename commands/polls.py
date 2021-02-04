# -*- coding: UTF-8 -*-

import discord
from random import *
from discord.ext import commands

class PollCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.client.remove_command("help")

    thumbs_up = "\N{THUMBS UP SIGN}"

    def check_count_reaction(self, emoji, desired_count, message):
        def predicate(reaction, user):
            return reaction.message == message and reaction.emoji == emoji and reaction.count>=desired_count
        return predicate

    @commands.command()
    async def poll(self, ctx: commands.Context, destination, number: int, condition):
        msg = await ctx.send(f"{ctx.author.mention} is looking to go to {destination} and " 
                        "is looking for {number} other people to come.\n"
                        "When:\n {condition}\nReact with {thumbs_up} if you're interested! "
                        "{ctx.guild.default_role.mention}")
        await msg.add_reaction(thumbs_up)
        reaction, user = await ctx.wait_for('reaction_add', check=check_count_reaction(thumbs_up, number+1, msg))
        users = await reaction.users().flatten()
        users = [u for u in users if not u.bot]
        await ctx.send(f"{ctx.author.mention}, {', '.join(m.mention for m in users)} are coming with you!")

def setup(client):
    client.add_cog(PollCommands(client))
