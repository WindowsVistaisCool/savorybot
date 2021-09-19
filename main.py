import discord
import cogs
import requests
import json
#import threading
#from flask import Flask, request
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_slash import SlashCommand
import datetime, time

intents = discord.Intents.default()
intents.typing = False
intents.integrations = False
intents.webhooks = False
intents.invites = False
intents.presences = False
client = commands.Bot(command_prefix=cogs.util.store('config.json', 'pfx', True), owner_ids=[406629388059410434], intents=intents)
client.remove_command('help')
#app = Flask(__name__)
#auth = cogs.util.store('config.json', 'apiAuth', True)
dcpnt = DiscordComponents(client)
slash = SlashCommand(client)

@client.event
async def on_ready():
    await cogs.util.get_ready(client)
    global starttime
    starttime = time.time()

@client.command()
async def uptime(ctx):
    e = discord.Embed(title="Current uptime", description=f"The current uptime is: {str(datetime.timedelta(seconds=int(round(time.time()-starttime))))}", color=0x23272A)
    await ctx.send(embed=e)

client.run(cogs.util.store('config.json', 'token', True))
