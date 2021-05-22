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

#broken
def getOnline(name):
    key = store("config.json", "key", True)
	ruff = requests.get(f'https://api.hypixel.net/status?key={key}').json()
    sus = requests.get(f"https://api.hypixel.net/player?key={key}&name={name}").json()
	lout = ruff["session"]["online"]
	stuff = ruff["session"]
	time = "Error"

	# doesn't fully work
	if lout is True:
		return [True, stuff["gameType"], stuff["mode"]]
	else:
		time = datetime.fromtimestamp(int(sus["player"]["lastLogout"])/1000)
		return [False, time]

async def status(client, ctx, user):
	e = discord.Embed(title="Fetching data from api...", color=discord.Color.blurple())
	a = await ctx.send(embeds=[e])
	o = getOnline()
	color = 0x000000
	description = "Error"
	on = False
	if o[0] is True:
		color = discord.Color.green()
		description = f"{n} is currently ONLINE"
		on = True
	elif o[0] is False:
		color = discord.Color.red()
		description = f"{n} is currently OFFLINE (Since {o[1]})"
	e = discord.Embed(title=f"Status of {n}", color=color, description=description, timestamp=datetime.utcnow())
	if on is True:
		e.add_field(name="Game", value=o[1])
		e.add_field(name="Mode", value=o[2])
	await a.edit(embed=e)
