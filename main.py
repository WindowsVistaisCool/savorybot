import discord
import cogs
import requests
import json
#import threading
#from flask import Flask, request
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_slash import SlashCommand
from datetime import datetime

client = commands.Bot(command_prefix=cogs.util.store('config.json', 'pfx', True))
client.remove_command('help')
#app = Flask(__name__)
#auth = cogs.util.store('config.json', 'apiAuth', True)
dcpnt = DiscordComponents(client)
slash = SlashCommand(client)

@client.event
async def on_ready():
    await cogs.util.get_ready(client)

client.run(cogs.util.store('config.json', 'token', True))
