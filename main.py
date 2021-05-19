import json
import random
import string
import commandListener
import discord
from discord.ext import commands
from commandListener import store as jbin
from discord_slash import SlashCommand, utils
from datetime import datetime
from asyncio import sleep

def store(file, key=None, read=False, val=None, *, pop=False):
	with open(file, 'r') as v:
		x = json.load(v)
	if x is None: return
	if read is not False:
		if key is None:
			return x
		else:
			return x[key]
	elif pop is True:
			return
	else:
		if val is None:
			with open(file, 'w') as v:
				json.dump(key, v, indent=4)
			return
		x[key] = val
		with open(file, 'w') as v:
			json.dump(x, v, indent=4)

client = commands.Bot(command_prefix=store('config.json', 'pfx', True))
client.remove_command('help')
slash = SlashCommand(client)
header = store('config.json', 'token', True)		

@client.event
async def on_message(message):
	e = await commandListener.msg(message, client)
	if e == 1: return
	await client.process_commands(message)

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Bonzo"))
	print("Ready")

@client.event
async def on_command_error(ctx, error):
	await commandListener.commandErrorListener(ctx, error)
	
#applications
@slash.slash(name='apply')
async def _apply(ctx, ign, skycrypt):
	await commandListener.apply(client, ctx, ign, skycrypt)

@client.group(name='a')
async def accept(ctx):
	role = ctx.guild.get_role(789592786287915010)
	if ctx.author.id != 392502213341216769 and role not in ctx.author.roles:
		await ctx.send('`CheckFailure:` You do not have permission to do this!')
		return
	await ctx.message.delete()
	if ctx.invoked_subcommand is None: await ctx.send(f"(bad sub err [null]) example: `{ctx.prefix}a g 1234567890` accepts a guild application with the id of 1234567890")

@accept.command(name='g')
async def acceptGuild(ctx, appID):
	await commandListener.acceptGuild(ctx, appID)

@client.command()
async def delapp(ctx, appID):
	await commandListener.delApp(ctx, appID)
	
#slash commands
@slash.slash(name="about")
async def _about(ctx):
	await commandListener.about(ctx)

# @slash.slash(name='pinglist')
# async def _pinglist(ctx, action, str):
# 	await commandListener.pinglist(ctx, action, str)

# TODO: command creation suggestions
@slash.slash(name="suggest")
async def _suggest(ctx, type, request):
	await commandListener.suggest(client, ctx, type, request)

@slash.slash(name='docs')
async def _docs(ctx):
	await ctx.send("https://reddocs.gitbook.io",hidden=True)

@slash.slash(name='genusername')
async def _genusername(ctx, setnick=False):
	await commandListener.genuser(ctx, setNick)

# clean up THIS mess
async def boogie(msg):
	await sleep(40)
	await msg.delete()

# convert this later
@slash.slash(name='version')
async def _version(ctx):
	await ctx.send("The latest version is listed in the <#839513996940148746> channel", hidden=True)

@client.command()
@commands.is_owner()
async def s(ctx, *, message='poopie farts'):
	await ctx.message.delete()
	if 'usr' in message:
		message.replace(' usr', '')
		message = f"<@!{message}>"
	await ctx.send(message)

async def _getnecronstick(ctx):
	d = ['t', 't', 't', 't', 't', 'f']
	b = random.choice(d)
	if b == 'f':
		e = discord.Embed(title="No item(s) were found!", color=discord.Color.red())
		await ctx.send(embeds=[e])
		return
	await commandListener.getitem(ctx, 'Necron\'s handle', 30)

#disabled
@slash.slash(name='getrocks')
async def _getrocks(ctx):
	await commandListener.getitem(ctx, 'Jolly Pink Rock', 60, rocks=True)

@client.command()
@commands.is_owner()
async def purge(ctx, message):
	await ctx.message.delete()
	await ctx.channel.purge(limit=int(message))

try:
	client.run(header)
except:
	print("token failure")
