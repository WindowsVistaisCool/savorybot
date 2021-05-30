import json
import requests
import random
import string
import discord
from discord.ext import commands
from datetime import datetime
from asyncio import sleep

def store(file, key=None, read=False, val=None, *, app=False, appKey=None, pop=False, specKey=None, specBin=None, n=False):
	# needs to be updated to api v3
	ke = specKey
	bi = specBin
	if specKey is None:
		ke = "$2b$10$H7xSlAq9QTHZmA3sgSfCK.kAMAk98k5uxSG1GlAPUj/rv5Yl2jZYu"
	if specBin is None:
		bi = "6084ce3c5210f622be390873"
	rheaders = {
		'secret-key': ke
	}
	uheaders = {
		'Content-Type': 'application/json',
		'secret-key': ke
	}
	rurl = f"https://api.jsonbin.io/b/{bi}/latest"
	url = f"https://api.jsonbin.io/b/{bi}"
	def get_read():
			x = requests.get(rurl, headers=rheaders, json=None).json()
			return x
	x = None
	if app or n:
		x = get_read()
		# print(x)
	else:
		with open(file, 'r') as v:
			x = json.load(v)
	if x is None: return
	if read is not False:
		if key is None:
			return
		else:
			return x[key]
	elif pop is True:
		if app is True:
			x[key].pop(appKey)
			e = requests.put(url, json=x, headers=uheaders)
			# print(e.text)
			return
		elif n is True:
			x.pop(key)
			e = requests.put(url, json=x, headers=uheaders)
			return e
		else:
			return
	else:
		if val is None:
			with open(file, 'w') as v:
				json.dump(key, v, indent=4)
			return
		if app is True:
			x[key][appKey] = val
			# print(x)
			e = requests.put(url, json=x, headers=uheaders)
			# print(e.text)
			# print(get_read())
			return
		elif n is True:
			x[key] = val
			e = requests.put(url, json=x, headers=uheaders)
			return e 
		else:
			x[key] = val
			with open(file, 'w') as v:
				json.dump(x, v, indent=4)

async def listenerOnRawReactionAdd(payload, client):
	x = store('config.json', 'verify', True)
	if payload.message_id == int(x):
		if payload.emoji.name == "✅":
			guild = client.get_guild(payload.guild_id)
			role = guild.get_role(788914323485491232)
			mrole = guild.get_role(788890991028469792)
			await payload.member.add_roles(role)
			await payload.member.remove_roles(mrole)

async def msg(message, client):
    ctx = await client.get_context(message)
    if message.author.id != 713461668667195553:
        if message.author.id == 392502213341216769:
            if message.content == 'embed':
                await message.delete()
                e = discord.Embed(title="Verification", color=discord.Color.blurple())
                e.add_field(name="Verify", value="To verify, react to this message with :white_check_mark:.", inline=False)
                e.add_field(name="Join Guild",value="To join the Guild, you first must verify, then see the `#guild-applications` channel.", inline=False)
                e.set_footer(text="Thank you for joining!")
                msg = await ctx.send(embed=e)
                await msg.add_reaction('✅')
                store('config.json', 'verify', False, str(msg.id))
    # if "@someone" in message.content and message.author.bot == False:
        # g = await message.guild.fetch_members(limit=150).flatten()
        # e = []
        # d = None
        # m = None
        # while True:
            # for member in g:
                # e.append(str(member.id))            
            # d = random.choice(e)
            # m = await message.guild.fetch_member(int(d))
            # if m.bot is False: break
        # await message.channel.send(f"{message.author.mention}, you pinged {m.mention}!")

async def getitem(ctx, item, time, *, username=None, rocks=False):
	# add item list or something
	def genuser():
		rank = ['Non', 'Non', 'Non', 'Non', 'Non', 'VIP', 'VIP', 'VIP', 'VIP', 'VIP+', 'VIP+', 'VIP+', 'MVP', 'MVP', 'MVP+', 'MVP+', 'MVP+', 'MVP+', 'MVP++']
		randnames = ['Ender', 'Pro', 'Itz', 'YT', 'Chill', 'Mom', 'Playz', 'Games', 'Fortnite', 'Prokid', 'Monkey', 'Gamer', 'GirlGamer', 'Lowping', 'Ihave', 'Getgud', 'Istupid', '123', 'Minecraft', 'LMAO', 'non']
		username = ''.join(random.choice(randnames) for i in range(random.randint(1, 8)))
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

async def commandErrorListener(ctx, error):
	if isinstance(error, commands.CheckFailure):
		e = discord.Embed(title="You do not have permission to do this!", color=discord.Color.red())
		await ctx.send(embed=e)
	elif isinstance(error, commands.CommandNotFound):
		e = discord.Embed(title="Command not found!", color=discord.Color.red())
		await ctx.send(embed=e)
	else:
		e = discord.Embed(title="An exception occurred", description=f"{error}")
		await ctx.send(embed=e)

async def apply(client, ctx, ign, skycrypt):
	if store('config.json', 'testMode', True):
		await ctx.send("Sorry! The bot is in test mode and this command cannot be ran at this time. Please try again later", hidden=True)
		return
	appType = None
	e = store('apps.json', 'guildApps', True, app=True)
	if str(ctx.author.id) in e:
		await ctx.send(content=f"You have already submitted an application, the application may have been denied or unanswered. Ask a mod for more help. (Submitted at `{e[str(ctx.author.id)]})``", hidden=True)
		return
	b = store('apps.json', 'acceptedGuildApps', True, app=True)
	if str(ctx.author.id) in b:
		await ctx.send(content="Your application has already been accepted, you may not apply for this position again",hidden=True)
		return
	d = skycrypt.find("https://sky.shiiyu.moe/stats/")
	if d == -1:
		await ctx.send(content="Your SkyCrypt URL is invalid! Please use this format: `https://sky.shiiyu.moe/stats/Savory/Apple`", hidden=True)
		return
	appType = "guildApps"
	r = ctx.guild.get_role(831614870256353330)
	await ctx.author.add_roles(r)
	await ctx.send(content="Thank you for submitting your application! Our mod team will review it soon.", hidden=True)
	c = client.get_channel(831579949415530527)
	e = discord.Embed(title="New Application", timestamp=datetime.utcnow(), color=discord.Color.green())
	e.set_footer(text="Application submitted")
	e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
	e.add_field(name="Application ID", value=f"{ctx.author.id}", inline=False)
	e.add_field(name="User", value=f"{ctx.author.mention}")
	e.add_field(name="IGN", value=ign, inline=False)
	e.add_field(name="Skyblock Stats", value=f"{skycrypt}", inline=False)
	a = await c.send("||<@&789593786287915010>||", embed=e)
	store('apps.json', appType, val=str(datetime.utcnow()), app=True, appKey=str(ctx.author.id))

async def acceptGuild(ctx, appID):
	if store('config.json', 'testMode', True):
		await ctx.send("Sorry! The bot is in test mode and this command cannot be ran at this time. Please try again later")
		return
	f = await ctx.send("Fetching data from api...")
	e = store('apps.json', 'guildApps', True, app=True)
	if appID not in e:
		await f.edit(content="Could not find that application!")
		return
	r = ctx.guild.get_role(789590790669205536)
	b = ctx.guild.get_role(831614870256353330)
	try:
		m = await ctx.guild.fetch_member(int(appID))
		await m.add_roles(r)
		await m.remove_roles(b)
	except:
		await ctx.send("Member lookup failed, deleting application; ask applicant to apply again.")
		store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
		return
	await f.edit(content="Sending data to API...")
	store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
	store('apps.json', 'acceptedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=appID)
	await f.edit(content="Application accepted")

async def delApp(ctx, appID):
	if store('config.json', 'testMode', True):
		await ctx.send("Sorry! The bot is in test mode and this command cannot be ran at this time. Please try again later")
		return
	f = await ctx.send("Fetching data from api...")
	e = store('apps.json', 'guildApps', True, app=True)
	if appID not in e:
		await f.edit(content="Could not find that application!")
		return
	await f.edit(content='Found application, deleting...')
	store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
	await f.edit(content='Deleted. (You must remove roles)')

async def about(ctx):
	await ctx.send(content='If you are a guild member and want to add something, please dm <@!392502213341216769>!', hidden=True)
	e = discord.Embed(title="Red Gladiators Guild Info", color=discord.Color.blurple())
	e.add_field(name="Features",value="**-** Active Skyblock Guild\n\n**-** Dungeons\n\n**-** Skyblock advice\n\n**-** Trusted members\n\n**-** Good community")
	d = await ctx.send(embeds=[e])
	await sleep(20)
	await d.delete()

async def genuser(ctx, setNick):
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

async def suggest(client, ctx, type, request):
	if type == 'b':
		e = await ctx.guild.fetch_member(392502213341216769)
		f = discord.Embed(title="New Suggestion", description=f"{request}")
		f.set_author(name=ctx.author)
		await e.send(embed=f)
		await ctx.send("Thank you for your suggestion! It really helps me make the bot better.", hidden=True)
	elif type == 'g':
		c = client.get_channel(818132089492733972)
		d = ctx.author.nick
		if d is None:
			d = ctx.author.name
		e = discord.Embed(title=f"Suggestion from {d}", description=request, timestamp=datetime.utcnow())
		await c.send(embed=e)
		await ctx.send("The request has been sent, thank you!", hidden=True)

# async def pinglist(ctx, action, str):
# 	if action != 'list' and str is None:
# 		await ctx.send("You cannot leave that field blank for that operation!",hidden=True)
# 		return
# 	x = store('apps.json', None, True, n=True, specBin="6093310865b36740b92ef100")
# 	d = x[str(ctx.author.id)]
# 	if action == 'list':
# 		if str(ctx.author.id) not in x:
# 			await ctx.send("You do not have any words stored! Add them with `/pinglist add {word}`",hidden=True)
# 			return
# 		s = []
# 		s.append(f"`{d['1']}`")
# 		if '2' not in d:
# 			s.append("Unset")
# 		else:
# 			s.append(f"`{d['2']}`")
		
# 		await ctx.send(f"Your ping words are:\n{s[0]}\n{s[1]}",hidden=True)
				 
# 	# trusted role could have more?
# 	elif action == 'add':
# 		if '2' in d:
# 			await ctx.send("You may not have more than 2 ping words! Use `/pinglist remove {index}`",hidden=True)
# 			return
# 		di = {}
# 		if '1' not in d:
# 			di['1'] = str
# 			store('blah.json', str(ctx.author.id), val=di, n=True, specBin="6093310865b36740b92ef100")
# 			await ctx.send(f"Added 1st word to index (`{str}`)",hidden=True)
# 			return
# 		else:
# 			di['1'] = d['1']
# 			di['2'] = str
# 			store('blah.json', str(ctx.author.id), val=di, n=True, specBin="6093310865b36740b92ef100")
# 			await ctx.send(f"Added 2nd word to index (`{str}`)",hidden=True)
# 			return

async def githubVer(ctx):
	await ctx.send(content="Sorry, but this command is not functional at the moment!",hidden=True)
