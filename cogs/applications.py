import discord
import json
import requests
from datetime import datetime
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from cogs import checks
from cogs.hystats import hyutil

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
            return x
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

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def forceapply(self, ctx, memberid, ign="Seggs"):
        pass

    @scmd.cog_slash(name='apply')
    async def apply(self, ctx, ign):
        await ctx.defer(hidden=True)
        if store('config.json', 'testMode', True):
            await ctx.send("Sorry! The bot is in test mode and this command cannot be ran at this time. Please try again later", hidden=True)
            return
        appType = None
        e = store('apps.json', 'guildApps', True, app=True)
        if str(ctx.author.id) in e:
            await ctx.send(content=f"You have already submitted an application, the application may have been denied or unanswered. Ask a mod for more help. (Submitted at `{e[str(ctx.author.id)]}`)", hidden=True)
            return
        l = store('apps.json', 'deniedGuildApps', True, app=True)
        if str(ctx.author.id) in l:
            await ctx.send("Sorry, your application has already been denied. Talk to a staff member if you need to re-apply.", hidden=True)
            return
        b = store('apps.json', 'acceptedGuildApps', True, app=True)
        if str(ctx.author.id) in b:
            await ctx.send(content="Your application has already been accepted, you may not apply for this position again",hidden=True)
            return
        igeen = hyutil.toUUID(ign)
        if igeen == False:
            await ctx.send("Your application IGN is invalid, please resubmit it.", hidden=True)
            return
        skycrypt = f"https://sky.shiiyu.moe/stats/{igeen}"
        appType = "guildApps"
        r = ctx.guild.get_role(831614870256353330)
        await ctx.author.add_roles(r)
        await ctx.send(content="Thank you for submitting your application! Our mod team will review it soon.", hidden=True)
        c = self.bot.get_channel(831579949415530527)
        e = discord.Embed(title="New Application", timestamp=datetime.utcnow(), color=discord.Color.green())
        e.set_footer(text="Application submitted")
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(name="Application ID", value=f"{ctx.author.id}", inline=False)
        e.add_field(name="User", value=f"{ctx.author.mention}")
        e.add_field(name="IGN", value=hyutil.toName(igeen), inline=False)
        e.add_field(name="Skyblock Stats", value=f"{skycrypt}", inline=False)
        store('apps.json', appType, val=str(datetime.utcnow()), app=True, appKey=str(ctx.author.id))
        a = await c.send("||<@789593786287915010>||", embed=e, components=[[Button(label="Accept App",id=f"{ctx.author.id}-a",style=3), Button(label="Deny App",id=f"{ctx.author.id}-d",style=4)]])

    @commands.group()
    @commands.check(checks.owner_staff)
    async def app(self, ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand is None: await ctx.send("Where did all the commands go? You can now accept/deny applications with the buttons on the application! If you made a mistake, you can use `=app del 1234567890` to delete the application with ID 1234567890! This will check pending, accepted, and denied guild apps and delete it correspondingly.")

    @app.command(name='del')
    async def delApp(self, ctx, appID):
        if store('config.json', 'testMode', True):
            await ctx.send("Sorry! The bot is in test mode and this command cannot be ran at this time. Please try again later")
            return
        f = await ctx.send("Fetching data from api...")
        e = store('apps.json', 'guildApps', True, app=True)
        a = store('apps.json', 'acceptedGuildApps', True, app=True)
        d = store('apps.json', 'deniedGuildApps', True, app=True)
        typee = 1
        if appID not in e:
            await f.edit(content="Could not find that application! Searching...")
            typee = 2
            if appID not in a:
                await f.edit(content="Could not find that application! Searching...")
                typee = 3
                if appID not in d:
                    await f.edit(content="Could not find that application!")
                    return
        await f.edit(content='Found application, deleting...')
        if typee == 1:
            store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
        elif typee == 2:
            store('apps.json', 'acceptedGuildApps', app=True, appKey=appID, pop=True)
        elif typee == 3:
            store('apps.json', 'deniedGuildApps', app=True, appKey=appID, pop=True)
        else:
            await f.edit(content="Lookup failed")
            return
        await f.edit(content='Deleted. (You must remove roles)')

    @app.command(name='force')
    async def forceApp(self, ctx, memberid=None, ign="Placeholder"):
        if memberid is None: memberid = ctx.author.id
        appType = None
        e = store('apps.json', 'guildApps', True, app=True)
        if str(memberid) in e:
            await ctx.send(content=f"You have already submitted an application, the application may have been denied or unanswered. Ask a mod for more help. (Submitted at `{e[str(memberid)]}`)")
            return
        l = store('apps.json', 'deniedGuildApps', True, app=True)
        if str(memberid) in l:
            await ctx.send("Sorry, your application has already been denied. Talk to a staff member if you need to re-apply.")
            return
        b = store('apps.json', 'acceptedGuildApps', True, app=True)
        if str(memberid) in b:
            await ctx.send(content="Your application has already been accepted, you may not apply for this position again")
            return
        igeen = hyutil.toUUID(ign)
        if igeen == False:
            await ctx.send("Your application IGN is invalid, please resubmit it.")
            return
        skycrypt = f"https://sky.shiiyu.moe/stats/{igeen}"
        appType = "guildApps"
        member = await ctx.guild.fetch_member(int(memberid))
        r = ctx.guild.get_role(831614870256353330)
        await member.add_roles(r)
        c = self.bot.get_channel(831579949415530527)
        e = discord.Embed(title="New Application", timestamp=datetime.utcnow(), color=discord.Color.green())
        e.set_footer(text="Application submitted")
        e.set_author(name=member, icon_url=member.avatar_url)
        e.add_field(name="Application ID", value=f"{memberid}", inline=False)
        e.add_field(name="User", value=f"{member.mention}")
        e.add_field(name="IGN", value=hyutil.toName(igeen), inline=False)
        e.add_field(name="Skyblock Stats", value=f"{skycrypt}", inline=False)
        store('apps.json', appType, val=str(datetime.utcnow()), app=True, appKey=str(memberid))
        a = await c.send("||Test Application||", embed=e, components=[[Button(label="Accept App",id=f"{memberid}-a",style=3), Button(label="Deny App",id=f"{memberid}-d",style=4)]])

def setup(bot):
    bot.add_cog(Applications(bot))
