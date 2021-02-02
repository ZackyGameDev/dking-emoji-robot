import os
from random import random
from discord import Game, Embed, Color
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix="-")
client.remove_command("help")
client_status = cycle(["working overtime", "listening to music subjectively good in my opinion", "playing some videogames", "contemplating robot existance", "trying to be online", "listening to -ehelp", "Zacky is my developer", "Dking is Grinding"])

@client.event
async def on_ready():
    print("i'm online yey")
    change_status.start()

@tasks.loop(minutes=2)
async def change_status():
    await client.change_presence(activity=Game(next(client_status)))

#code by DKING08 :)
@client.command() 
async def ehelp(ctx: commands.Context):
    await ctx.send(embed=Embed(
        description='Commands: \n `-e text` Use this command to use nitro emojis, example, `-e sundarDasta is og`\n`-erand choices` Use this command to let this bot choose from your arguments (emojis also supported), example, `-erand sundarDasta 69`',
        color=Color.from_hsv(random(), 1, 1)
    ).set_author(
        name=f'{ctx.me}',
        icon_url=f'https://cdn.discordapp.com/avatars/{ctx.me.id}/{ctx.me.avatar}.png'
    ))

#another code by Dking
@client.command() 
async def erand(ctx: commands.Context, *, args):
    try: 
        reply: str = args

        emojis: dict = {}
        for i in ctx.guild.emojis:
            if i.animated: 
                emojis[f"{i.name}"]: str = f"<a:{i.name}:{i.id}>"
            else: 
                emojis[f"{i.name}"]: str = f"<:{i.name}:{i.id}>"

        for emoji in emojis: reply: str = reply.replace(emoji, emojis[emoji])

        reply = random.choice(reply.split(' '))

        # Sending reply
        await ctx.message.delete() # deleting original message
        if reply in emojis: # if it's a single emoji a arg, set emoji to embed image
            await ctx.send(embed=Embed(
                color=Color.from_hsv(random(), 1, 1)
            ).set_author(
                name=f'{ctx.author}',
                icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
            ).set_image(
                url=client.get_emoji(int(emojis[args][-19:-1])).url
            ))
        else: # else send formated string as embed description
            await ctx.send(embed=Embed(
                description=reply,
                color=Color.from_hsv(random(), 1, 1)
            ).set_author(
                name=f'{ctx.author}',
                icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
            ))
    except Exception as e:
        await ctx.send(e)

@client.command() 
async def e(ctx: commands.Context, *, args):
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

    # # Creating reply
    # reply = str()
    # args = args.split()
    # for arg in args:
    #     if arg in emojis:
    #         reply += emojis[arg]
    #     else:
    #         reply += f" {arg}"
    
    # Sending reply
    await ctx.message.delete() # deleting original message
    if len(args.split()) == 1 and args in emojis: # if it's a single emoji a arg, set emoji to embed image
        await ctx.send(embed=Embed(
            color=Color.from_hsv(random(), 1, 1)
        ).set_author(
            name=f'{ctx.author}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
        ).set_image(
            url=client.get_emoji(int(emojis[args][-19:-1])).url
        ))
    elif len(args.split()) == 2 and args.split()[0] in emojis and args.split()[1] in emojis: # if it's a two emojis a arg, set emoji to embed image other one to thumbnail
        await ctx.send(embed=Embed(
            color=Color.from_hsv(random(), 1, 1)
        ).set_author(
            name=f'{ctx.author}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
        ).set_image(
            url=client.get_emoji(int(emojis[args.split()[0]][-19:-1])).url
        ).set_thumbnail(
            url=client.get_emoji(int(emojis[args.split()[1]][-19:-1])).url  # this is a bad way to do this, but it works so idc
        ))
    else: # else send formated string as embed description
        await ctx.send(embed=Embed(
            description=reply,
            color=Color.from_hsv(random(), 1, 1)
        ).set_author(
            name=f'{ctx.author}',
            icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
        ))

client.run(os.getenv("TOKEN"))
