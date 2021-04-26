import json
import random
import string
import commandListener
import discord
from discord.ext import commands
from discord_slash import SlashCommand, utils
from datetime import datetime
from asyncio import sleep
from slashrequest import sc as srq

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

client = commands.Bot(command_prefix='kiembot ')
client.remove_command('help')
slash = SlashCommand(client)
header = store('config.json', 'token', True)

@client.event
async def on_message(message):
	ctx = await client.get_context(message)
	if message.channel.id == 789303598957199441:
		if message.content != "verify" and message.author.id != 829885999270068276:
			if message.author.id == 392502213341216769:
				if message.content == 'embed':
					await message.delete()
					e = discord.Embed(title="Verification", color=discord.Color.blurple())
					e.add_field(name="Verify", value="To verify, type *`verify`* in this channel.", inline=False)
					e.add_field(name="Join Guild",value="To join the Guild, you first must verify, then see the `#guild-applications` channel.", inline=False)
					e.set_footer(text="Thank you for joining!")
					await ctx.send(embed=e)
					# json maybe?
				else:
					await message.delete()
					return
			else:
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
			g = await ctx.send("You have been verified, you now have access to all channels.")
			await sleep(5)
			await g.delete()


	await client.process_commands(message)

@client.command()
@commands.is_owner()
async def addrole(ctx, roleID, member: discord.Member=None):
	await ctx.message.delete()
	if member is None: member = ctx.author
	r = None
	try:
		r = ctx.guild.get_role(roleID)
	except:
		await ctx.send("could not find that role you big noob")
	await member.remove_roles(r)

@client.command()
@commands.is_owner()
async def remrole(ctx, roleID, member: discord.Member=None):
	await ctx.message.delete()
	if member is None: member = ctx.author
	r = None
	try:
		r = ctx.guild.get_role(roleID)
	except:
		await ctx.send("could not find that role you big noob")
	await member.remove_roles(r)

@client.command()
@commands.is_owner()
async def award(ctx, member: discord.Member):
	await ctx.message.delete()
	r = ctx.guild.get_role(831611831461740554)
	await member.add_roles(r)
	await ctx.send(f"{member} was given the Dev Award role. Good job")

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Necron"))
	print("ready")

@client.event
async def on_command_error(ctx, error):
	await commandListener.commandErrorListener(ctx, error)

#applications
@slash.slash(name='apply')
async def _apply(ctx, ign, sbstats, position=None):
	await commandListener.apply(client, ctx, ign, sbstats, position)

@client.group(name='a')
async def accept(ctx):
	role = ctx.guild.get_role(789592786287915010)
	if ctx.author.id != 392502213341216769 and role not in ctx.author.roles:
		await ctx.send('`CheckFailure:` You do not have permission to do this!')
		return
	await ctx.message.delete()
	if ctx.invoked_subcommand is None: await ctx.send("example: `kiembot a g 1234567890` accepts a guild application with the id of 1234567890\n`kiembot a t 1234567890-T` accepts an application for trusted role of app id 1234567890-T (doesnt work yet)")

@accept.command(name='g')
async def acceptGuild(ctx, appID):
	await commandListener.acceptGuild(ctx, appID)

@accept.command(name='t')
async def acceptTrusted(ctx, appID):
	# the new appid would have user id and -t after it, to distinguish between the two
	await ctx.send("You cannot do this!")

#slash commands
@slash.slash(name="about")
async def _about(ctx):
	await commandListener.about(ctx)

@slash.slash(name='clientsecrets')
async def _clientsecrets(ctx):
	e = await ctx.send("fetching keys from `http://api.github.com/repo/windowsvistaiscool/red-gladiator/raw/config.json` (using `'auth': 'token ghp_'` headers)\n\n`http://api.jsonbin.io/b/windowsvistaiscool/latest`, (using `'secret-key': '_'` headers (`masterkey not found`))")
	await sleep(5)
	await e.edit(content="error whilst retrieving keys: `could not reach target: https://api.jsonbin.io`, exiting with error code `HTTP/404`")

# TODO: command creation suggestions
@slash.slash(name="suggest")
async def _suggest(ctx, idea):
	e = await ctx.guild.fetch_member(392502213341216769)
	f = discord.Embed(title="New Suggestion", description=f"From `{ctx.author}`\n\n```{idea}```")
	await e.send(embed=f)
	await ctx.send("ok i sent it, thank you, it helps me make the bot better", hidden=True)

@slash.slash(name='checkguild')
async def _checkguild(ctx, ign):
	await ctx.send(content="This command is still work in progress, sorry!", hidden=True)

async def boogie(msg):
	await sleep(40)
	await msg.delete()

@slash.slash(name='version')
async def _version(ctx):
	await commandListener.githubVer(ctx)

#subcommands
@slash.subcommand(base='extra', name='monke')
async def _monke(ctx):
	e = await ctx.send(content="monkemxnia wants to smooch expicmnxia on the lips")
	await boogie(e)

@slash.subcommand(base='extra', name='moose')
async def _moose(ctx):
	e = await ctx.send(content="u will swish with monkemxnia's bathwater if you dont run this")
	await boogie(e)

@slash.subcommand(base='aa', name='important')
async def _important(ctx):
	await ctx.send("This bot will be deleted soon due to an oversight relating to a security flaw. There WILL be a new bot, and if everything goes smoothly, you won't notice any difference. Sorry for the inconvenience, but all your commands should still run fine", hidden=True)
	
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
