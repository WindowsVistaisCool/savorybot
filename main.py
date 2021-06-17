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

embeds = {}
client = commands.Bot(command_prefix=store('config.json', 'pfx', True))
client.remove_command('help')
slash = SlashCommand(client)
header = store('config.json', 'token', True)        

def getcolor(clr):
    if clr == "blurple":
        return discord.Color.blurple()
    elif clr == "red":
        return discord.Color.red()
    elif clr == "blue":
        return discord.Color.blue()
    else:
        return discord.Color.light_gray()

async def advancedEmbed(ctx, title, color='blurple', timestamp=False, description=None, authorname=None, authoricon=None, authorlink=None, fields=[]):
    def emtest(thing, test):
        if test is False or test is None:
            return discord.Embed.Empty
        else:
            return thing
    e = discord.Embed(title=title, color=getcolor(color), timestamp=emtest(datetime.utcnow(), timestamp), description=emtest(description, description))
    if fields != []:
        for field in fields:
            e.add_field(name=field['name'], value=field['value'], inline=field['inline'])
    if authorname is not None:
        e.set_author(name=authorname, url=emtest(authorlink, authorlink), icon_url=emtest(authoricon, authoricon))
    await ctx.send(embed=e)

@client.event
async def on_message(message):
    e = await commandListener.msg(message, client)
    if e == 1: return
    await client.process_commands(message)

@client.event
async def on_raw_reaction_add(payload):
    await commandListener.listenerOnRawReactionAdd(payload, client)

@client.event
async def on_ready():
    x = store('config.json', 'atype', True)
    f = store('config.json', 'testMode', True)
    def type():
        d = store('config.json', 'activity', True)
        if f:
            return discord.Game(name='DEV MODE') 
        elif x == 'l':
            return discord.Activity(type=discord.ActivityType.listening, name=d)
        elif x == 'w':
            return discord.Activity(type=discord.ActivityType.watching, name=d)
        elif x == 'c':
            return discord.Activity(type=discord.ActivityType.competing, name=d)
        elif x == 's':
            return discord.Streaming(name=d, url=store('config.json', 'surl', True))
        else:
            return discord.Game(name=d)
    def stat():
        l = store('config.json', 'status', True)
        f = store('config.json', 'testMode', True)
        if l == 'dnd' or f:
            return discord.Status.dnd
        elif l == 'online':
            return discord.Status.online
        elif l == 'afk':
            return discord.Status.idle
        else:
            return discord.Status.invisible
    if x != 'n':
        await client.change_presence(status=stat(), activity=type())
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
    if ctx.invoked_subcommand is None: await ctx.send(f"(bad sub err) example: `{ctx.prefix}a g 1234567890` accepts a guild application with the id of 1234567890")

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
#     await commandListener.pinglist(ctx, action, str)

# TODO: command creation suggestions
@slash.slash(name="suggest")
async def _suggest(ctx, type, request):
    await commandListener.suggest(client, ctx, type, request)

@slash.slash(name='docs')
async def _docs(ctx):
    await ctx.send("https://reddocs.gitbook.io",hidden=True)

# @slash.slash(name='genusername')
# async def _genusername(ctx, setnick=False):
    # await commandListener.genuser(ctx, setNick)

@client.command()
@commands.has_role("Trusted")
async def poll(ctx, *, msg):
    await ctx.message.delete()
    e = discord.Embed(title=msg, color=discord.Color.blurple(), timestamp=datetime.utcnow())
    e.set_footer(text="Poll started")
    msg = await ctx.send(embed=e)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@slash.subcommand(base='hy', name='banstats')
async def _banstats(ctx):
    m = await ctx.send("Fetching data from API...")
    f = requests.get('https://api.hypixel.net/punishmentstats?key=1663194c-20d2-4255-b85b-82fa68236d4e').json()
    if f['success'] is False:
        await m.edit(content=f'There was an error, please report this! ({f["cause"]})')
        return
    e = discord.Embed(title="Punishment statistics",color=discord.Color.red(), timestamp=datetime.utcnow())
    e.add_field(name='Watchdog total', value=f"`{f['watchdog_total']}`", inline=False)
    e.add_field(name='Watchdog today', value=f"`{f['watchdog_rollingDaily']}`", inline=False)
    e.add_field(name='Staff total', value=f"`{f['staff_total']}`", inline=False)
    e.add_field(name='Staff today', value=f"`{f['staff_rollingDaily']}`", inline=False)
    f = await m.edit(content="", embed=e, delete_after=40)

@slash.subcommand(base='hy', name='counts')
async def _counts(ctx, type='SKYBLOCK'):
    m = await ctx.send("Fetching data from API...")
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
        count = requests.get('https://api.hypixel.net/counts?key=1663194c-20d2-4255-b85b-82fa68236d4e').json()
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

@slash.subcommand(base='hy', name='status')
async def _status(ctx, username):
    await hystats.status(client, ctx, username)

@slash.subcommand(base='hy', name='profiles')
async def _profiles(ctx, user):
    await hystats.profiles(ctx, user)

# fix this
@client.command()
@commands.is_owner()
async def s(ctx, *, message='poopie farts'):
    await ctx.message.delete()
    if 'p!' in message:
        message = message.replace('p!', '<@!')
    await ctx.send(message)

@client.command()
@commands.is_owner()
async def n(ctx, *, nickname=None):
    d = await ctx.guild.fetch_member(client.user.id)
    await d.edit(nick=nickname)
    await ctx.message.delete()

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

@client.group()
@commands.is_owner()
async def e(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Please provide a valid subcommand")

@e.command()
async def help(ctx, command=None):
    if command is None:
        e = discord.Embed(title="Embed creator help", color=discord.Color.blurple(), timestamp=datetime.utcnow())
        e.add_field(name="Creating an embed", value="To create an embed, you first need need to run `./embed create <title>`. More info with `./embed help create'.", inline=False)
        e.add_field(name="Customization", value="To customize your embed, you can run `./embed help color`, `./embed help timestamp`, `./embed help author`, or `./embed help description`.")
        await ctx.send(embed=e)
        return
    elif command == 'create':
        e = discord.Embed(title="Specific embed command help", color=discord.Color.blurple())
        e.add_field(name="Syntax:", value="`./embed create <title>`")
    elif command == 'color':
        e = discord.Embed(title="Specific embed command help", color=discord.Color.blurple())
        e.add_field(name="Syntax:", value="`./embed color <color>`")
        e.add_field(name="Acceptable Color Fields:", value="dark_purple\nblurple")

    await ctx.send(embed=e)

@e.command()
async def create(ctx, *, title=None):
    if not ctx.author.id in embeds:
        embeds[ctx.author.id] = {}
    if title is None:
        await ctx.send("Please provide a title!")
        return
    embeds[ctx.author.id]['title'] = title
    embeds[ctx.author.id]['color'] = 'null'
    embeds[ctx.author.id]['description'] = 'null'
    embeds[ctx.author.id]['fields'] = []
    embeds[ctx.author.id]['timestamp'] = 'False'
    embeds[ctx.author.id]['authorlink'] = 'null'
    embeds[ctx.author.id]['authoricon'] = 'null'
    embeds[ctx.author.id]['authorname'] = 'null'
    await ctx.message.delete()
    msg = await ctx.send("Created embed")
    await sleep(1)
    await msg.delete()

@e.command()
async def field(ctx, name='Amoogus', value='Yay!', inline=False):
    if not ctx.author.id in embeds:
        await ctx.send("Please create an embed first with the ./embed create command.")
        return
    if inline == 'true':
        inline = True
    f = {"name": name, "value": value, "inline": inline}
    embeds[ctx.author.id]['fields'].append(f.copy())
    await ctx.message.delete()
    msg = await ctx.send("Added field")
    await sleep(1)
    await msg.delete()

@e.command()
async def color(ctx, color='blurple'):
    if not ctx.author.id in embeds:
        await ctx.send("Please create an embed first with the ./embed create command.")
        return
    embeds[ctx.author.id]['color'] = color
    await ctx.message.delete()
    msg = await ctx.send("Color set")
    await sleep(1)
    await msg.delete()

@e.command()
async def description(ctx, *, desc='Nice and short description!'):
    if not ctx.author.id in embeds:
        await ctx.send("Please create an embed first with the ./embed create command.")
        return
    embeds[ctx.author.id]['description'] = desc
    await ctx.message.delete()
    msg = await ctx.send("Embed description set")
    await sleep(1)
    await msg.delete()

@e.command()
async def timestamp(ctx, times='False'):
    if not ctx.author.id in embeds:
        await ctx.send("Please create an embed first with the ./embed create command.")
        return
    if times == 'False':
        pass
    elif times == 'True':
        pass
    else:
        await ctx.send("Please use \"False\" or \"True\".")
        return
    embeds[ctx.author.id]['timestamp'] = times
    await ctx.message.delete()
    msg = await ctx.send("Timestamp set")
    await sleep(1)
    await msg.delete()

@e.command()
async def author(ctx, link=None, icontype='self', *, name='self'):
    if not ctx.author.id in embeds:
        await ctx.send("Please create an embed first with the ./embed create command.")
        return
    authorlink = None
    authorname = None
    if link != None:
        authorlink = link
    if name == 'self':
        authorname = ctx.author.name
    else:
        authorname = name
    if icontype == 'self':
        icontype = ctx.author.avatar_url
    embeds[ctx.author.id]['authorlink'] = authorlink
    embeds[ctx.author.id]['authoricon'] = icontype
    embeds[ctx.author.id]['authorname'] = authorname
    await ctx.message.delete()
    msg = await ctx.send("Author set")
    await sleep(1)
    await msg.delete()

@e.command()
async def build(ctx):
    # also maybe change null str to Nonetype
    if not ctx.author.id in embeds:
        await ctx.send("Please create an embed with the ./embed create command.")
        return
    description = None
    if embeds[ctx.author.id]['description'] != 'null':
        description = embeds[ctx.author.id]['description']
    timestamp = False
    if embeds[ctx.author.id]['timestamp'] != 'False':
        timestamp = True
    authorname = None
    authoricon = None
    authorlink = None
    if embeds[ctx.author.id]['authorname'] != 'null':
        authorname = embeds[ctx.author.id]['authorname']
        if embeds[ctx.author.id]['authorlink'] != 'null':
            authorlink = embeds[ctx.author.id]['authorlink']
        if embeds[ctx.author.id]['authoricon'] != 'null':
            authoricon = embeds[ctx.author.id]['authoricon']
    title = embeds[ctx.author.id]['title']
    color = embeds[ctx.author.id]['color']
    await advancedEmbed(ctx, title, color, timestamp, description, authorname, authoricon, authorlink, embeds[ctx.author.id]['fields'])
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def purge(ctx, message):
    await ctx.message.delete()
    await ctx.channel.purge(limit=int(message))

client.run(header)
