import cogs
import discord
import json

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

async def bugReport(client, command, data):
    c = client.get_channel(889165938983845930)
    await c.send(f"***BUG REPORT*** ||<@!406629388059410434>||\n**Command:** {command}\n**Cause:** {data}")

################################################################################

async def get_ready(bot):
    config = store('config.json', None, True)
    load_cogs(bot, config)
    await ready_status(bot, config)
    print("Ready")

def load_cogs(bot, config):
    for cog in config['cogs']:
        bot.load_extension(cog)

async def ready_status(client, x):
    f = x['testMode']
    def type():
        d = x['activity']
        if f:
            return discord.Game(name='Test mode (commands don\'t work)')
        elif x['atype'] == 'l':
            return discord.Activity(type=discord.ActivityType.listening, name=d)
        elif x['atype'] == 'w':
            return discord.Activity(type=discord.ActivityType.watching, name=d)
        elif x['atype'] == 'c':
            return discord.Activity(type=discord.ActivityType.competing, name=d)
        elif x['atype'] == 's':
            return discord.Streaming(name=d, url=x['surl'])
        else:
            return discord.Game(name=d)
    def stat():
        l = x['status']
        if l == 'dnd' or f:
            return discord.Status.dnd
        elif l == 'online':
            return discord.Status.online
        elif l == 'idle':
            return discord.Status.idle
        else:
            return discord.Status.invisible
    if x['atype'] != 'n' or f:
        await client.change_presence(status=stat(), activity=type())
