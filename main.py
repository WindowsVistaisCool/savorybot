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
slash = SlashCommand(client)
header = store('config.json', 'token', True)

async def getitem(ctx, item, time, *, username=None, rocks=False):
	# add item list or something
	def genuser():
		rank = [False, False, False, False, False, 'VIP', 'VIP', 'VIP', 'VIP', 'VIP+', 'VIP+', 'VIP+', 'MVP', 'MVP', 'MVP+', 'MVP+', 'MVP+', 'MVP+', 'MVP++']
		randnames = ['ender', 'Pro', 'itz', 'YT', 'Chill', 'Mom', 'Playz', 'Games', 'fortnite', 'prokid', 'monkey', 'Gamer', 'GirlGamer', 's1mp', 'lowping', 'ihave', 'getgud', 'istupid', '123', 'minecraft', 'LMAO', 'non']
		username = f'{random.choice(rank)} {random.choice(randnames) for i in range(random.randint(1, 8))}'
		return username
	def getname():
		if username is None:
			e = genuser()
			return e
		else:
			return username
	locations = ['Graveyard', 'Castle', 'Wizard Tower', 'Barn', 'Dark Auction', 'Auction House', 'Lumber Merchant', 'Plumber Joe\'s House', 'Community Center', 'Jacob\'s House', 'Catacombs Entrance', 'Coal Mines', 'Bank', 'Builder\'s House', 'Maddox the Slayer', 'Tia the Fairy']
	location = random.choice(locations)
	e = discord.Embed(title="Dropped item(s) were found!", color=discord.Color.green(), description=f"Hurry to pick it up at the `{location}` in `Hub {random.randint(1, 40)}` before it dissapears!", timestamp=datetime.utcnow())
	if rocks is True:
		for x in range(8):
			e.add_field(name=f"`{item}` ({x + 1})", value=f"Dropped by `{getname()}`", inline=False)
	else:
		e.add_field(name=f"`{item}`", value=f"Dropped by `{getname()}`")
	e.set_footer(text=f"{time} seconds!")
	d = await ctx.send(embed=e)
	await sleep(time)
	g = discord.Embed(title="The item disappeared!", color=discord.Color.red())
	e.set_footer(text="Rip item")
	await d.edit(embed=g)
	await sleep(10)
	await d.delete()

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
@slash.slash(name='apply')
async def _apply(ctx, position):
	await ctx.send(content="This command is still work in progress, sorry! Use the old apply method (look in channels for #guild-applications).", hidden=True)

@slash.slash(name="about")
async def _about(ctx, sub=None):
	await ctx.send(content="This command is still work in progress, sorry!", hidden=True)

@slash.slash(name='checkguild')
async def _checkguild(ctx, user):
	await ctx.send(content="This command is still work in progress, sorry!", hidden=True)

@slash.slash(name='getnecronstick')
async def _getnecronstick(ctx):
	d = ['t', 't', 't', 't', 't', 'f']
	b = random.choice(d)
	if b == 'f':
		e = discord.Embed(title="No item(s) were found!", color=discord.Color.red())
		await ctx.send(embed=e)
		return
	await getitem(ctx, 'Necron\'s handle', 30)

@slash.slash(name='getrocks')
async def _getrocks(ctx):
	await getitem(ctx, 'Jolly Pink Rock', 60, rocks=True)

@slash.slash(name='getwitheress')
async def _getwitheress(ctx):
	await ctx.send("50,000 was successfuly hacked into your Minecraft account!", hidden=True)

@client.command()
@commands.is_owner()
async def stop(ctx):
	await ctx.send("stopping bot cuz u gay")
	await client.close()

try:
	client.run(header)
except:
	print("token failure")
