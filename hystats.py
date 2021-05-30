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

#broken
def getOnline(name):
	key = store("config.json", "key", True)
	uuid = toUUID(name)
	if uuid == False:
		return ['err', 'Could not find that username!']
	ruff = requests.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid}').json()
	sus = requests.get(f"https://api.hypixel.net/player?key={key}&name={name}")
	print(sus)
	res = sus
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
		time = datetime.fromtimestamp(int(sus["player"]["lastLogout"])/1000)
		return [False, time, res]

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
