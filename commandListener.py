import json
import requests
import random
import string
import discord
from discord.ext import commands
from datetime import datetime
from asyncio import sleep

def store(file, key=None, read=False, val=None, *, app=False, appKey=None, pop=False, specKey=None, specBin=None, n=False):
	ke = specKey
	bi = specBin
	if specKey is None:
		ke = "$2b$10$H7xSlAq9QTHZmA3sgSfCK.kAMAk98k5uxSG1GlAPUj/rv5Yl2jZYu"
	if specBin is None:
		bi = "6084ce3c5210f622be390873"
	rheaders = {
		'X-Master-Key': ke
	}
	uheaders = {
		'Content-Type': 'application/json',
		'X-Master-Key': ke
	}
	rurl = f"https://api.jsonbin.io/v3/b/{bi}/latest"
	url = f"https://api.jsonbin.io/v3/b/{bi}"
	def get_read():
			x = requests.get(rurl, headers=rheaders, json=None).json()
			return x
	x = None
	if app or n:
		x = get_read()['record']
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


class hystats:
    def handleRequest(status_code, err=True):
        if err == True:
            # Client errors
            if status_code == 400:
                return '**400** Bad Request'
            elif status_code == 401:
                return '**401** Invalid Authorization'
            elif status_code == 403:
                return '**403** Forbidden'
            elif status_code == 404:
                return '**404** Not found'
            elif status_code == 408:
                return '**408** Request timed out'
            elif status_code == 413:
                return '**413** Payload too large'
            elif status_code == 418:
                return '**418** I\'m a teapot! I can\'t brew coffee!'
            elif status_code == 429:
                return '**429** Too many requests!'
            # Server errors
            elif status_code == 500:
                return '***500*** Internal Server Error'
            elif status_code == 502:
                return '***502*** Bad gateway'
            elif status_code == 503:
                return '***503*** Service down'
            elif status_code == 504:
                return '***504*** Gateway timeout'
            # Cloudflare
            elif status_code == 520:
                return '**520** Server returned unkown error'
            elif status_code == 521 or status_code == 523:
                return f'**{status_code}** Origin is unreachable'
            elif status_code == 522:
                return '**522** Connection timed out'
            else:
                return
        else:
            return

    def toUUID(name):
        d = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
        if d.status_code == 204:
            return False
        return d.json()["id"]

    # sbprofiles
    async def profiles(ctx, name):
        a = await ctx.send(embed=discord.Embed(title='Fetching data from api...', color=discord.Color.blurple()))
        uuid = hystats.toUUID(name)
        if uuid is False:
            await a.edit(content="Could not find that username!")
            return
        d = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={store('config.json', 'key', True)}&uuid={uuid}")
        if d.status_code == 429:
            await a.edit(embed=discord.Embed(title="API Error", description=handleRequest(d.status_code), color=discord.Color.red()))
            return
        # hypixel down for maintainence
        if d.status_code == 521:
            await a.edit(embed=discord.Embed(title="API Error", description=handleRequest(d.status_code), color=discord.Color.red()))
            return
        f = d.json()
        store('req.json', f)
        if f['profiles'] is None:
            await a.edit(content="That user has not played skyblock!")
            return
        plen = len(f['profiles'])
        if plen == 1:
            pfls = "1 profile was"
        else:
            pfls = f"{plen} profiles were"
        e = discord.Embed(title=f"Profiles for user {name}", description=f"{pfls} detected for {name}", color=discord.Color.green())
        for pf in f['profiles']:
            coopm = []
    #         for member in pf['members']:
    #             if member.has_key("coop_invitation"):
    #                 continue
            coop = "Coming soon"
                    
            msg = f"`ID`: {pf['profile_id']}\n`Coop members`:{coop}"
            title = pf['cute_name']
            try:
                if pf['game_mode'] == 'ironman':
                    title = title + " **(Ironman)**"
            except:
                pass
            e.add_field(name=title, value=msg, inline=False)
        await a.edit(content=None, embed=e)

    #broken
    def getOnline(name):
        key = store("config.json", "key", True)
        uuid = hystats.toUUID(name)
        if uuid == False:
            return ['err', 'Could not find that username!']
        ruf = requests.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid}')
        sus = requests.get(f"https://api.hypixel.net/player?key={key}&name={name}")
        res = sus
        # print(res.json())
        if res.status_code == 429 or res.status_code == 521:
            return ['err', handleRequest(res.status_code)]
        ruff = ruf.json()
        sus = sus.json()
        if sus["success"] is False:
            print(sus)
        lout = ruff["session"]["online"]
        stuff = ruff["session"]
        time = "Error"

        # doesn't fully work
        if lout is True:
            return [True, stuff["gameType"], stuff["mode"], res]
        else:
            try:
                time = datetime.fromtimestamp(int(sus["player"]["lastLogout"])/1000)
                print(time)
                return [False, time, res]
            except:
                return [False, "Invalid Timestamp", res]

    # add modes later
    def sbmode(g):
        return g

    async def status(client, ctx, user):
        e = discord.Embed(title="Fetching data from api...", color=discord.Color.blurple())
        a = await ctx.send(embeds=[e])
        o = hystats.getOnline(user)
        color = 0x000000
        description = "Error"
        on = False
        if o[0] is True:
            color = discord.Color.green()
            description = f"{user} is currently ONLINE"
            on = True
        elif o[0] is False:
            color = discord.Color.red()
            description = f"{user} is currently OFFLINE"
        elif o[0] == 'err':
            e = discord.Embed(title="API Error", color=discord.Color.red(), description=o[1])
            await a.edit(embed=e)
            return
        def timeC():
            if o[0]:
                return datetime.utcnow()
            else:
                return o[1]
        def fC():
            if o[0]:
                return "Lookup at"
            else:
                return "[UTC] Offline since"
        e = discord.Embed(title=f"Status of {user}", color=color, description=description, timestamp=timeC())
        e.set_footer(text=fC())
        if on is True:
            e.add_field(name="Game", value=o[1])
            game = o[2]
            if o[1] == 'SKYBLOCK':
                game = sbmode(o[2])
            e.add_field(name="Mode", value=game)
        await a.edit(embed=e)

    async def banstats(ctx):
        await ctx.defer(hidden=True)
        f = requests.get('https://api.hypixel.net/punishmentstats?key=1663194c-20d2-4255-b85b-82fa68236d4e')
        if f.status_code == 521:
            await ctx.send(embed=discord.Embed(title="API Error", description=handleRequest(f.status_code), color=discord.Color.red()))
            return
        f = f.json()
        if f['success'] is False:
            await ctx.send(content=f'There was an error, please report this! ({f["cause"]})', hidden=True)
            return
        e = discord.Embed(title="Punishment statistics",color=discord.Color.red(), timestamp=datetime.utcnow())
        e.add_field(name='Watchdog total', value=f"`{f['watchdog_total']}`", inline=False)
        e.add_field(name='Watchdog today', value=f"`{f['watchdog_rollingDaily']}`", inline=False)
        e.add_field(name='Staff total', value=f"`{f['staff_total']}`", inline=False)
        e.add_field(name='Staff today', value=f"`{f['staff_rollingDaily']}`", inline=False)
        await ctx.send(embed=e, hidden=True)

    async def counts(ctx, type='SKYBLOCK'):
        m = await ctx.send(embed=discord.Embed(title="Fetching data from API...", color=discord.Color.blurple()))
        gmname = "(not yet implemented)"
        if type == 'SKYBLOCK':
            gmname = 'Skyblock'
        elif type == 'BEDWARS':
            gmname = 'Bedwars'
        elif type == 'SKYWARS':
            gmname = 'Skywars'
        # elif type == 'mini':
            # gmname = 'Arcade/Build Battle/Legacy Games/TNT Games'
        elif type == 'etc':
            gmname = 'SMP/Replay/Housing/Pit/Tournament/Prototype'
        try:
            counts = requests.get('https://api.hypixel.net/counts?key=1663194c-20d2-4255-b85b-82fa68236d4e')
            if counts.status_code == 521:
                await m.edit(embed=discord.Embed(title="API Error", description=handleRequest(counts.status_code), color=discord.Color.red()))
                return
            count = counts.json()
            store('req.json', count)
            if count['success'] is False:
                await m.edit(content=f"Error getting player counts, please report this! ({count['cause']})")
                return
            e = discord.Embed(title=f"Player counts for {gmname}", description=f"**Network-wide player count**\n```yaml\n{count['playerCount']}```", color=discord.Color.blurple(), timestamp=datetime.utcnow())
            e.set_footer(text='Counts recieved')
            # Set counts
            if type == 'SKYBLOCK':
                base = count["games"][type]
                modes = base["modes"]
                e.add_field(name='Total Skyblock count (skyblock-wide)', value=f'```fix\n{base["players"]}```', inline=False)
                e.add_field(name='Private Island', value=f'`{modes["dynamic"]}`')
                e.add_field(name='Main Hub', value=f'`{modes["hub"]}`')
                e.add_field(name='Dungeon Hub', value=f'`{modes["dungeon_hub"]}`')
                e.add_field(name='Dungeon', value=f'`{modes["dungeon"]}`')
                e.add_field(name='Farming Islands', value=f'`{modes["farming_1"]}`', inline=False)
                e.add_field(name='Gold Mines', value=f'`{modes["mining_1"]}`')
                e.add_field(name='Deep Caverns', value=f'`{modes["mining_2"]}`')
                e.add_field(name='Dwarven Mines', value=f'`{modes["mining_3"]}`')
                e.add_field(name='The Park', value=f'`{modes["foraging_1"]}`', inline=False)
                e.add_field(name='Spider\'s Den', value=f'`{modes["combat_1"]}`')
                e.add_field(name='Blazing Fortress', value=f'`{modes["combat_2"]}`')
                e.add_field(name='The End', value=f'`{modes["combat_3"]}`')
            elif type == 'BEDWARS':
                base = count["games"][type]
                modes = base["modes"]
                e.add_field(name='Total Bedwars count', value=f'```fix\n{base["players"]}```', inline=False)
                e.add_field(name='Solos', value=f'`{modes["BEDWARS_EIGHT_ONE"]}`')
                e.add_field(name='Doubles', value=f'`{modes["BEDWARS_EIGHT_TWO"]}`')
                e.add_field(name='Triples', value=f'`{modes["BEDWARS_FOUR_THREE"]}`')
                e.add_field(name='Quads', value=f'`{modes["BEDWARS_FOUR_FOUR"]}`')
                e.add_field(name='4v4', value=f'`{modes["BEDWARS_TWO_FOUR"]}`')
                e.add_field(name='Practice', value=f'`{modes["BEDWARS_PRACTICE"]}`')
                # add castle
                rawModes = ["BEDWARS_FOUR_FOUR_RUSH", "BEDWARS_EIGHT_TWO_VOIDLESS", "BEDWARS_FOUR_FOUR_VOIDLESS", "BEDWARS_EIGHT_TWO_ARMED", "BEDWARS_FOUR_FOUR_ARMED", "BEDWARS_EIGHT_TWO_ULTIMATE", "BEDWARS_FOUR_FOUR_ULTIMATE", "BEDWARS_EIGHT_TWO_LUCKY", "BEDWARS_FOUR_FOUR_LUCKY", "BEDWARS_EIGHT_TWO_RUSH"]
                fancyModes = ['Quads Rush', 'Doubles Voidless', 'Quads Voidless', 'Doubles Armed', 'Quads Armed', 'Doubles Ultimates', 'Quads Ultimates', 'Doubles Lucky Block', 'Quads Lucky Block', 'Doubles Rush']
                for x in range(len(rawModes)):
                    try:
                        e.add_field(name=fancyModes[x-1], value=f'`{modes[rawModes[x-1]]}`')
                    except:
                        continue
            elif type == 'SKYWARS':
                base = count['games'][type]
                modes = base["modes"]
                e.add_field(name='Total Skywars count', value=f'```fix\n{base["players"]}```', inline=False)
                e.add_field(name='Solo Normal', value=f'`{modes["solo_normal"]}`')
                e.add_field(name='Teams Normal', value=f'`{modes["teams_normal"]}`')
                e.add_field(name='More games coming later', value='NOT SOON')
            elif type == 'etc':
                base = count["games"]
                e.add_field(name='Main Lobby', value=f'`{base["MAIN_LOBBY"]["players"]}`')
                e.add_field(name='Limbo', value=f'`{base["LIMBO"]["players"]}`')
                e.add_field(name='Idle', value=f'`{base["IDLE"]["players"]}`')
                tmnt = base["TOURNAMENT_LOBBY"]["players"]
                if tmnt == 0: tmnt = "No current ongoing tournament"
                e.add_field(name='Tournament Lobby', value=f'`{tmnt}`')
                e.add_field(name='SMP', value=f'`{base["SMP"]["players"]}`')
                e.add_field(name='The Pit', value=f'`{base["PIT"]["players"]}`')
                e.add_field(name='Replay', value=f'`{base["REPLAY"]["players"]}`')
                e.add_field(name='Housing', value=f'`{base["HOUSING"]["players"]}`')
                ptp = base["PROTOTYPE"]
                e.add_field(name='Prototype (lobby & games)', value=f'`{ptp["players"]}`')
                e.add_field(name='TOWERWARS', value=f'Tower wars (solo): `{ptp["modes"]["TOWERWARS_SOLO"]}`\nTower wars (doubles): `{ptp["modes"]["TOWERWARS_TEAM_OF_TWO"]}`')

            await m.edit(content="", embed=e, delete_after=40)
        except Exception as e:
            await m.edit(content=("Failure: ",e), delete_after=40)

async def listenerOnRawReactionAdd(payload, client):
	if payload.user_id == 392502213341216769:
		m = client.get_channel(payload.channel_id)
		d = await m.fetch_message(payload.message_id)
		await d.remove_reaction(payload.emoji, client.user)
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
    if message.channel.id == 788886124159828012:
        if '.n' in message.content or '.d' in message.content or '.skills' in message.content or 'sbs guild' in message.content:
            await message.reply(content='Please use this command in the bot commands channel!')
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
		await ctx.send(content=f"You have already submitted an application, the application may have been denied or unanswered. Ask a mod for more help. (Submitted at `{e[str(ctx.author.id)]}`)", hidden=True)
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
	e = await ctx.guild.fetch_member(appID)
	try:
		await e.send("Your application for `Red Gladiators` has been accepted! Head over to the server to check it out!")
	except:
		await f.edit(content='Application accepted but could not send messages to user')
		return
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
	e = discord.Embed(title="Red Gladiators Guild Info", color=discord.Color.blurple())
	e.add_field(name="Features",value="**-** Active Skyblock Guild\n\n**-** Dungeons\n\n**-** Skyblock advice\n\n**-** Trusted members\n\n**-** Good community")
	await ctx.send(embed=e, hidden=True)

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
