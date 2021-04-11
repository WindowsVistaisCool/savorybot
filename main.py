import json
import random
import string
import slashrequest as srq
import discord
from discord.ext import commands
from discord_slash import SlashCommand, utils
from slashrequest import store
from datetime import datetime
from asyncio import sleep

client = commands.Bot(command_prefix='goonbot ')
client.remove_command('help')
header = store('config.json', 'token', True)

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="SavoryApple and Moose"))
	print("ready")

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		e = discord.Embed(title="You do not have permission to do this!", color=discord.Color.red())
		await ctx.send(embed=e)
	elif isinstance(error, commands.CommandNotFound):
		e = discord.Embed(title="Command not found!", color=discord.Color.red())
		await ctx.send(embed=e)
	else:
		e = discord.Embed(title="An exception occurred", description=error)
		await ctx.send(embed=e)

#slashcommands
@slash.slash(name="about")
async def _about(ctx, sub=None):
	await ctx.send(content="This command is still work in progress, sorry!", hidden=True)

@slash.slash(name='getnecronstick')
async def _getnecronstick(ctx):
	username = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(3, 16)))
	# add random locations later
	e = discord.Embed(title="A wild item appeared!", color=discord.Color.green(), description="Hurry to pick it up at the `Dark Auction` in `Hub 1`before it dissapears!" timestamp=datetime.utcnow())
	e.add_field(name="Necron stick!", value=f"Dropped by `{username}`")
	e.set_footer(text="10 seconds!")
	d = await ctx.send(embed=e)
	await sleep(10)
	g = discord.Embed(title="The item disappeared!", color=discord.Color.red())
	await d.edit(embed=g)

@client.command()
@commands.is_owner()
async def stop(ctx):
	await ctx.send("stopping bot cuz u gay")
	await client.close()

try:
	client.run(header)
except:
	print("token failure")
