import json
import random
import string
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

async def getitem(ctx, item, time, *, username=None, rocks=False):
	# add item list or something
	def genuser():
		rank = ['Non', 'Non', 'Non', 'Non', 'Non', 'VIP', 'VIP', 'VIP', 'VIP', 'VIP+', 'VIP+', 'VIP+', 'MVP', 'MVP', 'MVP+', 'MVP+', 'MVP+', 'MVP+', 'MVP++']
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
	d = await ctx.send(embeds=[e])
	await sleep(time)
	g = discord.Embed(title="The item disappeared!", color=discord.Color.red())
	e.set_footer(text="Rip item")
	await d.edit(embed=g)
	await sleep(10)
	await d.delete()

@client.event
async def on_message(message):
	ctx = await client.get_context(message)
	if message.channel.id == 789303598957199441:
		if message.content != "verify" and message.author.id != 829885999270068276:
			# await message.delete()
			# return
			pass
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
			
	await client.process_commands(message)

@client.command()
@commands.is_owner()
async def award(ctx, member: discord.Member):
	r = ctx.guild.get_role(831611831461740554)
	await member.add_roles(r)
	await ctx.send(f"{member} was given the Dev Award role. Good job")

@client.command()
@commands.is_owner()
async def c(ctx):
	await ctx.message.delete()
	e = discord.Embed(title="Verification", color=discord.Color.blurple())
	e.add_field(name="Verify", value="To verify, type *`verify`* (lowercase) in this channel.", inline=False)
	e.add_field(name="Join Guild",value="To join the Guild, you first must verify, then head over to the `#guild-applications` channel.", inline=False)
	await ctx.send(embed=e)

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Skyblock noises"))
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
		e = discord.Embed(title="An exception occurred", description=f"{error}")
		await ctx.send(embed=e)

#applications
@slash.slash(name='apply')
async def _apply(ctx, ign, sbstats, position=None):
	appType = None
	if position == 'disman' or position == 'veteran' or position == 'trusted':
		# enable-disable feature
		await ctx.send(content="This position is not open for applications, sorry!", hidden=True)
		return
	elif position == None:
		e = store('apps.json', 'guildApps', True)
		if str(ctx.author.id) in e:
			await ctx.send(content=f"You have already submitted an application, the application may have been denied or unanswered. Ask a mod for more help. (Submitted at {e[str(ctx.author.id)]})", hidden=True)
			return
		b = store('apps.json', 'acceptedGuildApps', True)
		if str(ctx.author.id) in b:
			await ctx.send(content="Your application has already been accepted, you may not apply for this position again",hidden=True)
			return
	d = sbstats.find("https://sky.shiiyu.moe/stats/")
	if d == -1:
		await ctx.send(content="Your SkyCrypt URL is invalid! Please use this format: `https://sky.shiiyu.moe/stats/Goon/Apple`", hidden=True)
		return
	if position == None: appType = "guildApps"
	r = ctx.guild.get_role(831614870256353330)
	await ctx.author.add_roles(r)
	await ctx.send(content="Thank you for submitting your application! Our mod team will review it soon.", hidden=True)
	c = client.get_channel(831579949415530527)
	e = discord.Embed(title="New Application", timestamp=datetime.utcnow(), color=discord.Color.blurple())
	e.set_footer(text="Application submitted")
	e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
	e.add_field(name="Application ID", value=f"{ctx.author.id}", inline=False)
	e.add_field(name="IGN", value=ign, inline=False)
	e.add_field(name="Skyblock Stats", value=f"[Click Here]({sbstats})", inline=False)
	a = await c.send(embed=e)
	store('apps.json', appType, val=str(datetime.utcnow()), app=True, appKey=str(ctx.author.id))

@client.group(name='a')
@commands.has_role('Staff')
async def accept(ctx):
	await ctx.message.delete()
	if ctx.invoked_subcommand is None: await ctx.send("example: `goonbot a g 1234567890` accepts a guild application with the id of 1234567890\n`goonbot a t 1234567890` accepts an application for trusted role of app id 1234567890 (doesnt work yet)")
	
@accept.command(name='g')
async def acceptGuild(ctx, appID):
	e = store('apps.json', 'guildApps', True)
	if appID not in e:
		await ctx.send("Could not find that application!")
		return
	r = ctx.guild.get_role(789590790669205536)
	b = ctx.guild.get_role(831614870256353330)
	try:
		m = await ctx.guild.fetch_member(int(appID))
		await m.add_roles(r)
		await m.remove_roles(b)
	except:
		await ctx.send("Member lookup failed, deleting application")
		store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
		return
	store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
	store('apps.json', 'acceptedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=appID)
	await ctx.send("Application accepted")

#slash commands
@slash.slash(name="about")
async def _about(ctx, sub=None):
	e = discord.Embed(title="Red Gladiators Guild Info", color=discord.Color.blurple())
	e.add_field(name="Features",value="**-** Active Skyblock Guild\n\n**-** Dungeons\n\n**-** Skyblock advice\n\n**-** Trusted members\n\n**-** Good community")
	d = await ctx.send(embeds=[e])
	await sleep(20)
	await d.delete()

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

@client.command()
@commands.is_owner()
async def voice(ctx):
	bird = await ctx.guild.fetch_member(392502213341216769)
	chn = bird.voice.channel
	await chn.connect()
# 	source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('doobag.mp3'))
# 	ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

@client.command()
@commands.is_owner()
async def dc(ctx):
	await ctx.voice_client.disconnect()

#disabled
@slash.slash(name='getnecronstick')
async def _getnecronstick(ctx):
	d = ['t', 't', 't', 't', 't', 'f']
	b = random.choice(d)
	if b == 'f':
		e = discord.Embed(title="No item(s) were found!", color=discord.Color.red())
		await ctx.send(embeds=[e])
		return
	await getitem(ctx, 'Necron\'s handle', 30)

#disabled
@slash.slash(name='getrocks')
async def _getrocks(ctx):
	await getitem(ctx, 'Jolly Pink Rock', 60, rocks=True)

@client.command()
@commands.is_owner()
async def stop(ctx):
	e = await ctx.send("stopping bot cuz u gay")
	await sleep(2)
	await e.delete()
	await client.close()

@client.command()
@commands.is_owner()
async def purge(ctx, message):
	await ctx.message.delete()
	await ctx.channel.purge(limit=int(message))

try:
	client.run(header)
except:
	print("token failure")
