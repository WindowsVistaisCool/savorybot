import json
import discord
from discord.ext import commands
from main import store

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

async def commmandErrorListener(ctx, error):
	if isinstance(error, commands.CheckFailure):
		e = discord.Embed(title="You do not have permission to do this!", color=discord.Color.red())
		await ctx.send(embed=e)
	elif isinstance(error, commands.CommandNotFound):
		e = discord.Embed(title="Command not found!", color=discord.Color.red())
		await ctx.send(embed=e)
	else:
		e = discord.Embed(title="An exception occurred", description=f"{error}")
		await ctx.send(embed=e)

async def apply(client, ctx, ign, sbstats, position=None):
	appType = None
	if position == 'disman' or position == 'veteran':
		# enable-disable feature
		await ctx.send(content="This position isnot open for applications, sorry!", hidden=True)
		return
	elif position == 'trusted':
		await ctx.send(content="You can apply for this position, but you have to DM a staff member to do so.", hidden=True)
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
		await ctx.send("Member lookup failed, deleting application; ask applicant to apply again.")
		store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
		return
	store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
	store('apps.json', 'acceptedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=appID)
	await ctx.send("Application accepted")

async def about(ctx):
	await ctx.send(content='If you are a guild member and want to add something, please dm <@!392502213341216769>!', hidden=True)
	e = discord.Embed(title="Red Gladiators Guild Info", color=discord.Color.blurple())
	e.add_field(name="Features",value="**-** Active Skyblock Guild\n\n**-** Dungeons\n\n**-** Skyblock advice\n\n**-** Trusted members\n\n**-** Good community")
	d = await ctx.send(embeds=[e])
	await sleep(20)
	await d.delete()
