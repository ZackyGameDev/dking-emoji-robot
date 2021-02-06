# -*- coding: UTF-8 -*-

import discord
from random import *
from discord.ext import commands

class EmojifyCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        self.client.remove_command("help")

    @commands.command(aliases=["e"])
    async def emojify(self, ctx: commands.Context, *, args):
        '''`-e <text>`:
        Use this command to use nitro emojis.
        e.g. `-e sundarDasta is og`'''
        reply: str = args # Will format this later

        # Getting emojis
        emojis: dict = {}
        for i in ctx.guild.emojis:
            if i.animated: 
                emojis[f"{i.name}"]: str = f"<a:{i.name}:{i.id}>"
            else: 
                emojis[f"{i.name}"]: str = f"<:{i.name}:{i.id}>"

        # Creating reply
        for emoji in emojis: reply: str = reply.replace(emoji, emojis[emoji])
        
        # Sending reply
        await ctx.message.delete() # deleting original message
        
        if len(args.split()) == 1 and args in emojis: # if it's a single emoji a arg, set emoji to embed image
            await ctx.send(embed=discord.Embed(
                color=discord.Colour.from_hsv(random(), 1, 1)
            ).set_author(
                name=f'{ctx.author}',
                icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
            ).set_image(
                url=self.client.get_emoji(int(emojis[args][-19:-1])).url
            ))
        
        elif len(args.split()) == 2 and args.split()[0] in emojis and args.split()[1] in emojis: # if it's a two emojis a arg, set emoji to embed image other one to thumbnail
            await ctx.send(embed=discord.Embed(
                color=discord.Colour.from_hsv(random(), 1, 1)
            ).set_author(
                name=f'{ctx.author}',
                icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
            ).set_image(
                url=self.client.get_emoji(int(emojis[args.split()[0]][-19:-1])).url
            ).set_thumbnail(
                url=self.client.get_emoji(int(emojis[args.split()[1]][-19:-1])).url  # this is a bad way to do this, but it works so idc
            ))
        
        else: # else send formated string as embed description
            await ctx.send(embed=discord.Embed(
                description=reply,
                color=discord.Colour.from_hsv(random(), 1, 1)
            ).set_author(
                name=f'{ctx.author}',
                icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
            ))

    #another code by Dking
    @commands.command() 
    async def erand(self, ctx: commands.Context, *, args):
        '''
        `-erand \'optional text\' <randomOptionsToSelectFrom>`:
        Use this command to let this bot choose from your arguments (emojis also supported)
        e.g. `-erand sundarDasta 69`'''
        try: 
            reply: str = args
            Question = ''
            if reply.startswith('\''):
                Question = reply.replace("\'",'',1).replace('\'',';',1)
                Question2 = Question.split(';')
                Question = Question2[0]
            reply = reply.replace('\'' + Question + '\'', '').strip()
            emojis: dict = {}
            for i in ctx.guild.emojis:
                if i.animated: 
                    emojis[f"{i.name}"]: str = f"<a:{i.name}:{i.id}>"
                else: 
                    emojis[f"{i.name}"]: str = f"<:{i.name}:{i.id}>"

            for emoji in emojis: reply: str = reply.split(' ')[randint(0, len(reply.split(' '))-1)].replace(emoji, emojis[emoji])
            #await ctx.message.delete() # deleting original message
            if args in emojis: # if it's a single emoji a arg, set emoji to embed image
                await ctx.send('yes sir')
                await ctx.send(embed=discord.Embed(
                    title=Question,
                    color=discord.Colour.from_hsv(random(), 1, 1)
                ).set_author(
                    name=f'{ctx.author}',
                    icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
                ).set_image(
                    url=self.client.get_emoji(int(emojis[args][-19:-1])).url
                ))
            else: # else send formated string as embed description
                await ctx.send(embed=discord.Embed(
                    description=reply,
                    title=Question,
                    color=discord.Colour.from_hsv(random(), 1, 1)
                ).set_author(
                    name=f'{ctx.author}',
                    icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
                ))
        except Exception as e:
            await ctx.send(e)

def setup(client):
    client.add_cog(EmojifyCommand(client))