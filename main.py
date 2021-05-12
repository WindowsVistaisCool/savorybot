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

client = commands.Bot(command_prefix=store('config.json', 'pfx', True))
client.remove_command('help')
slash = SlashCommand(client)
header = store('config.json', 'token', True)		

@client.event
async def on_message(message):
	# move to commandlistener
	ctx = await client.get_context(message)
	if message.channel.id == 789303598957199441:
		if message.content != "verify" and message.author.id != 713461668667195553:
			if message.author.id == 392502213341216769:
				if message.content == 'embed':
					# convert to reaction
					await message.delete()
					e = discord.Embed(title="Verification", color=discord.Color.blurple())
					e.add_field(name="Verify", value="To verify, type *`verify`* in this channel.", inline=False)
					e.add_field(name="Join Guild",value="To join the Guild, you first must verify, then see the `#guild-applications` channel.", inline=False)
					e.set_footer(text="Thank you for joining!")
					await ctx.send(embed=e)
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
			return
	
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
async def _apply(ctx, ign, skycrypt, position=None):
	await commandListener.apply(client, ctx, ign, skycrypt, position)

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

	
#slash commands
@slash.slash(name="about")
async def _about(ctx):
	await commandListener.about(ctx)

@slash.slash(name='pinglist')
async def _pinglist(ctx, action, str):
	await commandListener.pinglist(ctx, action, str)

# TODO: command creation suggestions
@slash.slash(name="suggest")
async def _suggest(ctx, type, request):
	if type == 'b':
		e = await ctx.guild.fetch_member(392502213341216769)
		f = discord.Embed(title="New Suggestion", description=f"{request}")
		f.set_author(name=ctx.author)
		await e.send(embed=f)
		await ctx.send("Thank you for your suggestion! It really helps me make the bot better.", hidden=True)
	elif type == 'g':
		c = client.get_channel(818132089492733972)
		e = discord.Embed(title=f"Suggestion from {ctx.member.nick}", description=request, timestamp=datetime.utcnow())
		await c.send(embed=e)
		await ctx.send("The request has been sent, thank you!", hidden=True)
	else:
		await ctx.send("EOL: 404 not found param 'type'")

@slash.slash(name='docs')
async def _docs(ctx):
	await ctx.send("https://reddocs.gitbook.io",hidden=True)

@slash.slash(name='genusername')
async def _genusername(ctx, setnick=False):
	rank = ['Non', 'Non', 'Non', 'Non', 'Non', 'VIP', 'VIP', 'VIP', 'VIP', 'VIP+', 'VIP+', 'VIP+', 'MVP', 'MVP', 'MVP+', 'MVP+', 'MVP+', 'MVP+', 'MVP++']
	randnames = ['Ender', 'Pro', 'Itz', 'YT', 'Chill', 'Mom', 'Playz', 'Games', 'Fortnite', 'Prokid', 'Monkey', 'Gamer', 'GirlGamer', 'Lowping', 'Ihave', 'Getgud', 'Istupid', '123', 'Minecraft', 'LMAO', 'non']
	f = random.choice(rank)
	if f != 'Non':
		f = f"[{f}] "
	else:
		f = ''
	def callName():
		return f + ''.join(random.choice(randnames) for i in range(random.randint(1, 8)))
	username = callName()
	while True:
		if len(username)-len(f) > 31:
			username = callName()
		else:
			break
	if setnick is False:
		await ctx.send(f"`{username}`", hidden=True)
		return
	try:
		await ctx.author.edit(nick=username)
	except:
		await ctx.send("Could not do this (you may be a higher rank than the bot)", hidden=True)
		return
	await ctx.send(f"Your new nickname is: `{username}`", hidden=True)

# clean up THIS mess
async def boogie(msg):
	await sleep(40)
	await msg.delete()

# do this later
@slash.slash(name='version')
async def _version(ctx):
	await commandListener.githubVer(ctx)

#subcommands
@slash.subcommand(base='z', name='sussy')
async def _apple(ctx):
	e = await ctx.send("when imposter sus")
	await boogie(e)

@slash.subcommand(base='z', name='dadrip')
async def _dadrip(ctx):
	e = await ctx.send('https://windowsvistaiscool.github.io/i/d.jpeg')
	await boogie(e)

@client.command()
@commands.is_owner()
async def s(ctx, *, message='poopie farts'):
	await ctx.message.delete()
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
