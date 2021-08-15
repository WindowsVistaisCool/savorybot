import discord
import requests
import json
#import threading
#from flask import Flask, request
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_slash import SlashCommand
from datetime import datetime
import cogs

def read(file, key=None, read=False):
    with open(file, 'r') as v:
        x = json.load(v)
    if x is None: return
    if key is None:
        return x
    return x[key]

pfx = read('config.json', 'pfx')
client = commands.Bot(command_prefix=pfx)
client.remove_command('help')
#app = Flask(__name__)
#auth = cogs.util.store('config.json', 'apiAuth', True)
dcpnt = DiscordComponents(client)
slash = SlashCommand(client)

async def get_ready(bot):
    load_cogs(bot)
    await ready_status(bot, read('config.json', None, True))
    print("Ready")

def load_cogs(bot):
    cogs.applications.load(bot)
    cogs.btesting.load(bot)
    cogs.hystats.load(bot)
    cogs.listeners.load(bot)
    cogs.misc.load(bot)
    # cogs.owner.load(bot)
    cogs.polls.load(bot)
    cogs.trusted.load(bot)

async def ready_status(client, x):
    f = x['testMode']
    def type():
        d = x['activity']
        if f:
            return discord.Game(name='Test mode (commands don\'t work)')
        elif x['atype'] == 'l':
            return discord.Activity(type=discord.ActivityType.listening, name=d)
        elif x['atype'] == 'w':
            return discord.Activity(type=discord.ActivityType.watching, name=d)
        elif x['atype'] == 'c':
            return discord.Activity(type=discord.ActivityType.competing, name=d)
        elif x['atype'] == 's':
            return discord.Streaming(name=d, url=x['surl'])
        else:
            return discord.Game(name=d)
    def stat():
        l = x['status']
        if l == 'dnd' or f:
            return discord.Status.dnd
        elif l == 'online':
            return discord.Status.online
        elif l == 'idle':
            return discord.Status.idle
        else:
            return discord.Status.invisible
    if x['atype'] != 'n' or f:
        await client.change_presence(status=stat(), activity=type())

@client.event
async def on_ready():
    await get_ready(client)
# @slash.subcommand(base='hy', name='profiles')
# async def _profiles(ctx, user):
#     await hystats.profiles.profiles(client, ctx, user)
#
# @slash.subcommand(base='hy', name='status')
# async def _status(ctx, username):
#     await hystats.status(client, ctx, username)

client.run(read('config.json', 'token'))
