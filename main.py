import json
import random
import requests
import hystats
import string
import commandListener
import discord
from discord.ext import commands
from commandListener import store as jbin
from discord_slash import SlashCommand, utils
from datetime import datetime
from asyncio import sleep

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
	e = await commandListener.msg(message, client)
	if e == 1: return
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
async def _apply(ctx, ign, skycrypt):
	await commandListener.apply(client, ctx, ign, skycrypt)

@client.group(name='a')
async def accept(ctx):
	role = ctx.guild.get_role(789592786287915010)
	if ctx.author.id != 392502213341216769 and role not in ctx.author.roles:
		await ctx.send('`CheckFailure:` You do not have permission to do this!')
		return
	await ctx.message.delete()
	if ctx.invoked_subcommand is None: await ctx.send(f"(bad sub err [null]) example: `{ctx.prefix}a g 1234567890` accepts a guild application with the id of 1234567890")

@accept.command(name='g')
async def acceptGuild(ctx, appID):
	await commandListener.acceptGuild(ctx, appID)

@client.command()
async def delapp(ctx, appID):
	await commandListener.delApp(ctx, appID)
	
#slash commands
@slash.slash(name="about")
async def _about(ctx):
	await commandListener.about(ctx)

# @slash.slash(name='pinglist')
# async def _pinglist(ctx, action, str):
# 	await commandListener.pinglist(ctx, action, str)

# TODO: command creation suggestions
@slash.slash(name="suggest")
async def _suggest(ctx, type, request):
	await commandListener.suggest(client, ctx, type, request)

@slash.slash(name='docs')
async def _docs(ctx):
	await ctx.send("https://reddocs.gitbook.io",hidden=True)

@slash.slash(name='genusername')
async def _genusername(ctx, setnick=False):
	await commandListener.genuser(ctx, setNick)

# clean up THIS mess
async def boogie(msg):
	await sleep(40)
	await msg.delete()

@slash.slash(name='banstats')
async def _banstats(ctx):
	f = requests.get('https://api.hypixel.net/punishmentstats?key=1663194c-20d2-4255-b85b-82fa68236d4e').json()
	if f['success'] is False:
		await ctx.send('There was an error, please report this! (The command may be on cooldown!)', hidden=True)
		return
	e = discord.Embed(title="Punishment statistics",color=discord.Color.red(), timestamp=datetime.utcnow())
	e.add_field(name='Watchdog total', value=f"`{f['watchdog_total']}`", inline=False)
	e.add_field(name='Watchdog daily', value=f"`{f['watchdog_rollingDaily']}`", inline=False)
	e.add_field(name='Staff total', value=f"`{f['staff_total']}`", inline=False)
	e.add_field(name='Staff daily', value=f"`{f['staff_rollingDaily']}`", inline=False)
	f = await ctx.send(embeds=[e])
	await boogie(f)

@slash.slash(name='counts')
async def _counts(ctx, type='SKYBLOCK'):
	gmname = "undefined"
	if type == 'SKYBLOCK':
		gmname = 'Skyblock'
	# elif type == 'BEDWARS':
		# gmname = 'Bedwars'
	# elif type == 'SKYWARS':
		# gmname = 'Skywars'
	# elif type == 'mini':
		# gmname = 'Arcade/Build Battle/Legacy Games/TNT Games'
	elif type == 'etc':
		gmname = 'SMP/Replay/Housing/Pit/Tournament/Prototype'
	count = requests.get('https://api.hypixel.net/counts?key=1663194c-20d2-4255-b85b-82fa68236d4e').json()
	if count['success'] is False:
		await ctx.send("Error getting player counts, please report this!", hidden=True)
		return
	e = discord.Embed(title=f"Player counts for {gmname}", description=f"**Network-wide player count**\n```yaml\n{count['playerCount']}```", color=discord.Color.blurple(), timestamp=datetime.utcnow())
	e.set_footer(text='Counts recieved')
	# Set counts
	if type == 'SKYBLOCK':
		base = count["games"][type]
		modes = base["modes"]
		e.add_field(name='Total skyblock count (skyblock-wide)', value=f'```fix\n{base["players"]}```', inline=False)
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

	d = await ctx.send(embed=e)
	await boogie(d)

@slash.slash(name='giveaway')
async def _giveaway(ctx, winners, time, prize):
	d = client.get_channel(834960422004064266)
	e = discord.Embed(title="New giveaway request",timestamp=datetime.utcnow())
	e.add_field(name="Host", value=f"{ctx.author.mention}", inline=False)
	e.add_field(name="Winners", value=f"```{winners}```", inline=False)
	e.add_field(name="Time", value=f"```{time}```", inline=False)
	e.add_field(name="Prize", value=prize, inline=False)
	await d.send("<@&840038424332337202>", embed=e)
	await ctx.send("Your request has been sent", hidden=True)

#broken
@slash.slash(name='status')
async def _status(ctx, user):
	await hystats.status(client, ctx, user)
	#https://wiki.vg/Mojang_API

# fix this
@client.command()
@commands.is_owner()
async def s(ctx, *, message='poopie farts'):
	await ctx.message.delete()
	if 'usr' in message:
		message = message.replace(' usr', '')
		message = f"<@!{message}>"
	await ctx.send(message)

@client.command()
@commands.is_owner()
async def d(ctx, meID):
	await ctx.message.delete()
	e = await ctx.channel.fetch_message(int(meID))
	await e.delete()

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
