import time
import os
import discord
from random import *
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix="-", case_insensitive=True)
client_status = cycle(["working overtime", "listening to music subjectively good in my opinion", "playing some videogames", "contemplating robot existance", "trying to be online", "listening to -ehelp", "Zacky is my developer", "Dking is Grinding"])

def boot() -> None:
    # getting list of all paths to extensions
    filelist = []
    for root, dirs, files in os.walk("commands/"):
        for file in files:
            filelist.append(os.path.join(root, file))

    # And then loading them
    for file in filelist:
        if file.endswith('.py'):
            file = file.replace('/', '.').replace('\\', '.')[:-3]
            try: 
                client.load_extension(file)
            except: 
                pass

boot()

@client.event
async def on_ready():
    print("i'm online yey")
    change_status.start()
    
@tasks.loop(minutes=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(client_status)))

# Stole this command code from https://github.com/ZackyGameDev/event-hoster-discord-bot/blob/master/event-hoster.py#L177
@client.command()
async def eping(ctx):
    start = time.perf_counter()
    message = await ctx.send(embed=discord.Embed(
        description="Calculating Ping...",
        color=discord.Colour.red()
    ))
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(embed=discord.Embed(
        description=':stopwatch: **Response Delay: {:.2f}ms'.format(
            duration) + f"**\n:heartbeat: **Websocket Latency: {round(client.latency*1000)}ms**",
        color=discord.Colour.green()
    ))

@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)

client.run(os.getenv("TOKEN"))
