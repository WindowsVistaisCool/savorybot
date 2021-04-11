import json
import slashrequest as srq
import discord
from discord.ext import commands
from discord_slash import SlashCommand, utils
from slashrequest import store
from datetime import datetime
from asyncio import sleep

client = commands.Bot(command_prefix='red ')
#client.remove_command('help')

@client.event
async def on_ready():
	print("ready")

@client.command():
async def monke(ctx):
	await ctx.send("you are gaee")

try:
	client.run(store('config.json', 'token', True))
except:
	print("token failure")
