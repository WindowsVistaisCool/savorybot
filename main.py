import json
import random
import requests
import string
import commandListener
import slashrequest
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption
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
dcpnt = DiscordComponents(client)
slash = SlashCommand(client)
header = store('config.json', 'token', True)
tmode = store('config.json', 'testMode', True)

########################################################################
# Bot testing commands
@slash.subcommand(base='bt', name='info')
async def _bt_info(ctx):
    await ctx.send("You're here because you signed up to help me improve this bot! As of this first testing session, there are a few commands, and you will be pinged when a new one arrives. **DO NOT USE THESE COMMANDS OUTSIDE OF THE #bot-testing CHANNEL. YOU WILL RECIEVE A WARNING** If you recieve a message saying \"This interaction failed\", **please let me know as soon as possible**. Thank you for signing up and helping me iron out any bugs!", hidden=True)

@slash.subcommand(base='bt', name='interaction')
async def _bt_interaction(ctx, type):
    await commandListener.btesting.btInteraction(client, ctx, type)
    
########################################################################

# Events
@client.event
async def on_button_click(interaction):
    await commandListener.listener.onButtonClick(interaction)

@client.event
async def on_message(message):
    e = await commandListener.listener.onMessage(message, client)
    if e == 1: return
    await client.process_commands(message)

@client.event
async def on_raw_reaction_add(payload):
    await commandListener.listener.onRawReactionAdd(payload, client)

@client.event
async def on_raw_reaction_remove(payload):
    await commandListener.listener.onRawReactionRemove(payload, client)
@client.event
async def on_ready():
    await commandListener.listener.onReady(client)

@client.event
async def on_command_error(ctx, error):
    await commandListener.listener.onCommandError(ctx, error)

########################################################################

# Applications
@slash.slash(name='apply')
async def _apply(ctx, ign):
    await commandListener.apply(client, ctx, ign)

@client.group(name='app')
@commands.has_role("Staff")
async def accept(ctx):
    await ctx.message.delete()
    if ctx.invoked_subcommand is None: await ctx.send(f"(err: invalid command called) example: `{ctx.prefix}app accept 1234567890` accepts a guild application with the id of 1234567890\nrun this command to delete an application: `{ctx.prefix}app del 1234567890` which will allow the user to create another application\n use the buttons on the application message to deny")

@accept.command(name='accept')
async def acceptGuild(ctx, appID):
    await commandListener.acceptGuild(ctx, appID)

# @accept.command(name='deny')
# async def denyGuild(ctx, appID, *, reason):
    # await commandListener.denyGuild(ctx, appID, reason)

@accept.command(name='del')
async def delapp(ctx, appID):
    await commandListener.delApp(ctx, appID)

########################################################################

# HYSTATS
@slash.subcommand(base='hy', name='banstats')
async def _banstats(ctx):
    await commandListener.hystats.banstats(ctx)

@slash.subcommand(base='hy', name='counts')
async def _counts(ctx, gamemode='SKYBLOCK'):
    await commandListener.hystats.counts(ctx, gamemode)

@slash.subcommand(base='hy', name='status')
async def _status(ctx, username):
    await commandListener.hystats.status(client, ctx, username)

@slash.subcommand(base='hy', name='profiles')
async def _profiles(ctx, user, profile=None):
    await commandListener.hystats.profiles.profiles(client, ctx, user)

########################################################################

# Default member stuff
@slash.slash(name="about")
async def _about(ctx):
    await commandListener.about(ctx)

# add accept/deny stuff
@slash.slash(name='giveaway')
async def _giveaway(ctx, winners, time, prize):
    d = client.get_channel(834960422004064266)
    e = discord.Embed(title="New giveaway request",timestamp=datetime.utcnow())
    e.add_field(name="Host", value=f"{ctx.author.mention}", inline=False)
    e.add_field(name="Winners", value=f"```{winners}```", inline=False)
    e.add_field(name="Time", value=f"```{time}```", inline=False)
    e.add_field(name="Prize", value=prize, inline=False)
    await d.send("<@&840038424332337202>", embed=e, components=[Button(label="Deny",disabled=True,style=4,id="giveaway_deny")])
    await ctx.send("Your request has been sent", hidden=True)

########################################################################
# Trusted Commands
@client.command()
@commands.has_role("Trusted")
async def poll(ctx, *, msg):
    await ctx.message.delete()
    e = discord.Embed(title=msg, color=discord.Color.blurple(), timestamp=datetime.utcnow())
    e.set_footer(text="Poll started")
    msg = await ctx.send(embed=e)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@client.command()
@commands.has_role("Trusted")
async def pin(ctx, message=None):
    await ctx.message.delete()
    try:
        if message != None:
            e = await ctx.channel.fetch_message(int(message)) 
        else:
            e = None
            async for msg in ctx.channel.history(limit=1):
                e = msg
        await e.pin()
    except:
        await ctx.send("failure (invalid message id?/already pinned?)", delete_after=3)

@client.command()
@commands.has_role("Trusted")
async def unpin(ctx, message=None):
    await ctx.message.delete()
    if message != None:
        try:
            e = await ctx.channel.fetch_message(int(message))
            await e.unpin()
        except:
            await ctx.send("Could not find pin!")
            return
    try:
        m = None
        async for ms in ctx.channel.history(limit=200):
            if ms.pinned:
                m = ms
                break
        await m.unpin()
        await ctx.send("Unpinned message!")
    except:
        await ctx.send("Error retrieving pin (pins cannot be unpinned via this command if it is more than 200 messages ago")

# Officer commands
# Manager commands

# Owner-only commands
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


@client.command()
@commands.is_owner()
async def purge(ctx, message):
    await ctx.message.delete()
    await ctx.channel.purge(limit=int(message))

@client.command()
@commands.is_owner()
async def clown(ctx):
    await ctx.message.delete()
    await ctx.send("lmfao click the button below to get clowned on", components=[Button(emoji=client.get_emoji(815818057359687691), id="deverify")])

@client.command()
@commands.is_owner()
async def genbutton(ctx, label="Click me", id=None, message="Generated button"):
    await ctx.message.delete()
    if id:
        await ctx.send(message, components=[Button(label=label, id=id)])
    else:
        await ctx.send(message, components=[Button(label=label, id=id)])


# btesting
@client.group()
@commands.is_owner()
async def bt(ctx):
    await ctx.message.delete()
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid sub")

@bt.command(name='enable')
async def bt_enable(ctx, roleid):
    slashrequest.sc.post(store('config.json', 'bt', True))
    e = slashrequest.sc.get('bt')['id']
    slashrequest.sc.perm(e, [roleid], [True])
    await ctx.send("Added bot testing commands")

@bt.command(name='disable')
async def bt_disable(ctx):
    slashrequest.sc.rem('bt')
    await ctx.send("Removed bot testing commands")

# Reaction roles (owner-only)
@client.command()
@commands.is_owner()
async def rrsend(ctx, roleid, *, embmsg):
	await ctx.message.delete()
	e = discord.Embed(title=embmsg, color=discord.Color.blurple())
	msg = await ctx.send(embed=e)
	x = store('rroles.json', None, True)
	x['rroles'][str(msg.id)] = embmsg
	x['rrolesrole'][str(msg.id)] = roleid
	store('rroles.json', x)
	await msg.add_reaction("✅")
	await ctx.send("Reaction role added", delete_after=1)

@client.command()
@commands.is_owner()
async def rrdel(ctx, messageid):
	await ctx.message.delete()
	x = store('rroles.json', None, True)
	x["rroles"].pop(messageid)
	x["rrolesrole"].pop(messageid)
	store('rroles.json', x)
	await ctx.send("Reaction role removed", delete_after=1)
    
########################################################################

# Unused
async def _getnecronstick(ctx):
    d = ['t', 't', 't', 't', 't', 'f']
    b = random.choice(d)
    if b == 'f':
        e = discord.Embed(title="No item(s) were found!", color=discord.Color.red())
        await ctx.send(embeds=[e])
        return
    await commandListener.getitem(ctx, 'Necron\'s handle', 30)

async def _getrocks(ctx):
    await commandListener.getitem(ctx, 'Jolly Pink Rock', 60, rocks=True)

if __name__ == '__main__':
    client.run(header)
