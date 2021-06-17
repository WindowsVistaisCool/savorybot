import json
import requests
import discord
from discord.ext import commands
from asyncio import sleep as asleep
from datetime import datetime

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

def toUUID(name):
    d = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    if d.status_code == 204:
        return False
    return d.json()["id"]

# sbprofiles
async def profiles(ctx, name):
    a = await ctx.send("Getting data...")
    uuid = toUUID(name)
    if uuid is False:
        await a.edit(content="Could not find that username!")
        return
    d = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={store('config.json', 'key', True)}&uuid={uuid}")
    if d.status_code == 429:
        await a.edit(content="API Error (name looked up recently). Try again later")
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
	ruff = requests.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid}').json()
	sus = requests.get(f"https://api.hypixel.net/player?key={key}&name={name}")
	res = sus
	# print(res.json())
	if res.status_code == 429:
		return ['err', 'This name has recently been looked up (check older messages or wait a minute)']
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
