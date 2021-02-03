import time
import os
from random import *
from discord import Game, Embed, Color
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix="-", case_insensitive=True)
client.remove_command("help")
client_status = cycle(["working overtime", "listening to music subjectively good in my opinion", "playing some videogames", "contemplating robot existance", "trying to be online", "listening to -ehelp", "Zacky is my developer", "Dking is Grinding"])

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

@client.event
async def on_ready():
    print("i'm online yey")
    change_status.start()
    
@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)

# Stole this command code from https://github.com/ZackyGameDev/event-hoster-discord-bot/blob/master/event-hoster.py#L177
@client.command()
async def eping(ctx):
    start = time.perf_counter()
    message = await ctx.send(embed=Embed(
        description="Calculating Ping...",
        color=Color.red()
    ))
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(embed=Embed(
        description=':stopwatch: **Response Delay: {:.2f}ms'.format(
            duration) + f"**\n:heartbeat: **Websocket Latency: {round(client.latency*1000)}ms**",
        color=Color.green()
    ))
    
@tasks.loop(minutes=2)
async def change_status():
    await client.change_presence(activity=Game(next(client_status)))

#code by DKING08 :)
@client.command() 
async def ehelp(ctx: commands.Context):
    await ctx.send(embed=Embed(
        description=help_message,
        color=Color.from_hsv(random(), 1, 1)
    ).set_author(
        name=f'{ctx.me}',
        icon_url=f'https://cdn.discordapp.com/avatars/{ctx.me.id}/{ctx.me.avatar}.png'
    ))

@client.command()
async def poll(ctx, question, *options: str):
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
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)

    react_message = await ctx.send(embed=Embed(
                title=question,
                color=Color.from_hsv(random(), 1, 1),
                description = ''.join(description)
            ).set_author(
                name=f'{ctx.author}',
                icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
            ))

    for reaction in reactions[:len(options)]:
        await ctx.add_reaction(react_message, reaction)

    await react_message.edit(embed=Embed(
                title=question,
                color=Color.from_hsv(random(), 1, 1),
                description = ''.join(description)
            ).set_author(
                name=f'{ctx.author}',
                icon_url=f'https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png'
            ))

#another code by Dking
@client.command() 
async def erand(ctx: commands.Context, *, args):
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
            await ctx.send(embed=Embed(
                title=Question,
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
                title=Question,
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
