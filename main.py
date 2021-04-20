import json
import random
import string
import commandListener
import slashrequest as srq
import discord
from discord.ext import commands
from discord_slash import SlashCommand, utils
from datetime import datetime
from asyncio import sleep

def store(file, key=None, read=False, val=None, *, app=False, appKey=None, pop=False):
	with open(file, 'r') as v:
		x = json.load(v)
	if read is not False:
		if key is None:
			return x
		else:
			return x[key]
	elif pop is True:
		if app is True:
			x[key].pop(appKey)
			with open(file, 'w') as v:
				json.dump(x, v, indent=4)
		else:
			return
	else:
		if val is None:
			with open(file, 'w') as v:
				json.dump(key, v, indent=4)
			return
		if app is True:
			x[key][appKey] = val
		else:
			x[key] = val
		with open(file, 'w') as v:
			json.dump(x, v, indent=4)

client = commands.Bot(command_prefix='goonbot ')
client.remove_command('help')
slash = SlashCommand(client)
header = store('config.json', 'token', True)

@client.event
async def on_message(message):
	ctx = await client.get_context(message)
	if message.channel.id == 789303598957199441:
		if message.content != "verify" and message.author.id != 829885999270068276:
			await message.delete()
			return
		elif message.content == 'verify':
			await message.delete()
			r = ctx.guild.get_role(788914323485491232)
			if r in ctx.author.roles:
				e = await ctx.send("You have already been verified!")
				await sleep(3)
				await e.delete()
				return
			d = ctx.guild.get_role(788890991028469792)
			await message.author.remove_roles(d)
			await message.author.add_roles(r)
			g = await ctx.send("You have been verified")
			await sleep(5)
			await g.delete()
		elif message.content == 'embed':
			await message.delete()
			if message.author.id != 392502213341216769: return
			e = discord.Embed(title="Verification", color=discord.Color.blurple())
			e.add_field(name="Verify", value="To verify, type *`verify`* in this channel.", inline=False)
			e.add_field(name="Join Guild",value="To join the Guild, you first must verify, then see the `#guild-applications` channel.", inline=False)
			e.set_footer(text="Thank you for joining our server!")
			await ctx.send(embed=e)
			
			
	await client.process_commands(message)

@client.command()
@commands.is_owner()
async def award(ctx, member: discord.Member):
	await ctx.message.delete()
	r = ctx.guild.get_role(831611831461740554)
	await member.add_roles(r)
	await ctx.send(f"{member} was given the Dev Award role. Good job")

@client.event
async def on_ready():
	stuff = {
		"large_image": "jerry_battle.png",
		"large_text": "Jerry Simulator",
		"small_image": "jerrytube_ico.png",
		"small_text": "JerryTube 3D"
	}
	await client.change_presence(activity=discord.Streaming(url="https://www.youtube.com/watch?v=doEqUhFiQS4", assets=stuff, platform="JerryTube 3D", name="Jerry Simulator", game="Minecraft 1.8.9 Vanilla/OptiFine (Multiplayer)"))
	print("ready")

@client.event
async def on_command_error(ctx, error):
	await commandListener.commandErrorListener(ctx, error)

#applications
@slash.slash(name='apply')
async def _apply(ctx, ign, sbstats, position=None):
	await commandListener.apply(client, ctx, ign, sbstats, position)

@client.group(name='a')
@commands.has_role('Staff')
async def accept(ctx):
	await ctx.message.delete()
	if ctx.invoked_subcommand is None: await ctx.send("example: `goonbot a g 1234567890` accepts a guild application with the id of 1234567890\n`goonbot a t 1234567890` accepts an application for trusted role of app id 1234567890 (doesnt work yet)")
	
@accept.command(name='g')
async def acceptGuild(ctx, appID):
	await commandListener.acceptGuild(ctx, appID)

#slash commands
@slash.slash(name="about")
async def _about(ctx):
	await commandListener.about(ctx)

@slash.slash(name='checkguild')
async def _checkguild(ctx, ign):
	await ctx.send(content="This command is still work in progress, sorry!", hidden=True)

async def boogie(msg):
	await sleep(40)
	await msg.delete()

@slash.slash(name='extra')
async def _monke(ctx, subcommand):
	if subcommand == 'monke':
		e = await ctx.send(content="monkemxnia wants to smooch expicmnxia on the lips")
		await boogie(e)
	elif subcommand == 'moose':
		e = await ctx.send(content="u will swish with monkemxnia's mouthwater if you dont run this")
		await boogie(e)
	else:
		await ctx.send(content="This command is not finished yet!",hidden=True)

#disabled
@slash.slash(name='getnecronstick')
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
