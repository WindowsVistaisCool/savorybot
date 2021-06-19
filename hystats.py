import json
import requests
import discord
from discord.ext import commands
from asyncio import sleep as asleep
from datetime import datetime
from os import system

# asyncio api timeout needed
def store(file, key=None, read=False, val=None):
	with open(file, 'r') as v:
		x = json.load(v)
	if read is not False:
		if key is None:
			return x
		else:
			return x[key]
	else:
		if val is None:
			with open(file, 'w') as v:
				json.dump(key, v, indent=4)
			return
		x[key] = val
		with open(file, 'w') as v:
			json.dump(x, v, indent=4)

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
            return '**418** I\'m a teapot! I don\'t brew coffee!'
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
    uuid = toUUID(name)
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
        for member in pf['members']:
            if member.has_key("coop_invitation"):
                continue
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
	uuid = toUUID(name)
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
			return [False, time, res]
		except:
			return [False, "Invalid Timestamp", res]

# add modes later
def sbmode(g):
    return g

async def status(client, ctx, user):
	e = discord.Embed(title="Fetching data from api...", color=discord.Color.blurple())
	a = await ctx.send(embeds=[e])
	o = getOnline(user)
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
