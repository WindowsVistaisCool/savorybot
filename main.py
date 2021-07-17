import json
import random
import requests
import string
import commandListener
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

# Bot testing commands
@slash.subcommand(base='bt', name='info')
async def _bt_info(ctx):
    await ctx.send("You're here because you signed up to help me improve this bot! As of this first testing session, there are a few commands, and you will be pinged when a new one arrives. **DO NOT USE THESE COMMANDS OUTSIDE OF THE #bot-testing CHANNEL. YOU WILL RECIEVE A WARNING** If you recieve a message saying \"This interaction failed\", **please let me know as soon as possible**. Thank you for signing up and helping me iron out any bugs!", hidden=True)

@slash.subcommand(base='bt', name='interaction')
async def _bt_interaction(ctx, type):
    await ctx.defer()
    c = client.get_channel(ctx.channel.id)
    if type == 'b':
        m = await c.send(f"These are test buttons! ({ctx.author})", components=[Button(label="Test")])
        while True:
            interaction = await client.wait_for("button_click", check=lambda i: i.component.label.startswith("Test"))
            if interaction.user.id != ctx.author.id:
                mem = await ctx.guild.fetch_member(interaction.user.id)
                await ctx.send(f"{mem.mention}, this isn't your button!")
                continue
            break
        await m.edit(content=f"{ctx.author.name} clicked a button!", components=[])
        await interaction.respond(content="You clicked a button!")
    else:
        m = await c.send(f"This is an example dropdown menu! ({ctx.author})", components=[Select(placeholder="Select an option...", options=[SelectOption(label="Apple",value="apple"),SelectOption(label="Pear",value="pear"),SelectOption(label="Cucumber",value="cucumber")])])
        while True:
            interaction = await client.wait_for("select_option")
            if interaction.user.id != ctx.author.id:
                mem = await ctx.guild.fetch_member(interaction.user.id)
                await ctx.send(f"{mem.mention}, this isn't your menu!")
                continue
            break
        await m.edit(content=f"Expired menu - {ctx.author.name} selected {interaction.component[0].label}",components=[])
        await interaction.respond(context="You selected an item!")

@slash.subcommand(base='bt', name='hyprofiles')
async def _bt_hyprofiles(ctx, user):
    await commandListener.btesting.profiles(client, ctx, user)

# Events
@client.event
async def on_button_click(interaction):
    try:
        if interaction.component.label == "Delete":
            await interaction.message.delete()
        if str(interaction.user.id) != interaction.message.embeds[0].to_dict()['footer']['text'].replace('ID: ',''): return
        if interaction.component.label == 'Exit (Keep msg)':
            await interaction.message.edit(components=[])
        elif interaction.component.label == 'Delete (Delete msg)':
            await interaction.message.delete()
    except:
        pass

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

# Commands 

########################################################################
# Applications
@slash.slash(name='apply')
async def _apply(ctx, ign, skycrypt):
    await commandListener.apply(client, ctx, ign, skycrypt)

@client.group(name='app')
async def accept(ctx):
    role = ctx.guild.get_role(789592786287915010)
    if ctx.author.id != 392502213341216769 and role not in ctx.author.roles:
        await ctx.send('`CheckFailure:` You do not have permission to do this!')
        return
    await ctx.message.delete()
    if ctx.invoked_subcommand is None: await ctx.send(f"(err: invalid command called) example: `{ctx.prefix}app accept 1234567890` accepts a guild application with the id of 1234567890\nto deny an application, run this: `{ctx.prefix}app deny 124567890` which denies that user from creating applications again\nrun this command to pardon them: `{ctx.prefix}app pardon 1234567890` which will allow them to create applications again")

@accept.command(name='accept')
async def acceptGuild(ctx, appID):
    await commandListener.acceptGuild(ctx, appID)

@accept.command(name='deny')
async def denyGuild(ctx, appID, *, reason):
    await commandListener.denyGuild(ctx, appID, reason)

@client.command()
async def delapp(ctx, appID):
    await commandListener.delApp(ctx, appID)
########################################################################

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
    await commandListener.hystats.profiles(ctx, user, profile)
########################################################################

# Default member stuff
@slash.slash(name="about")
async def _about(ctx):
    await commandListener.about(ctx)

@slash.slash(name="suggest")
async def _suggest(ctx, type, request):
    await commandListener.suggest(client, ctx, type, request)

# add accept/deny stuff
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
