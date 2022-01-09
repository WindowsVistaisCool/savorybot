import requests
import string
import random
import json
import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from datetime import datetime
from cogs.util import store
from cogs.hystats import hyutil
from asyncio import sleep

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.annoy = 0

    @scmd.cog_slash(name='frag')
    async def _frag(self, ctx, ign, reason):
        try:
            igeen = hyutil.toUUID(ign)
        except:
            await ctx.send("Invalid IGN provided", hidden=True)
            return
        c = self.bot.get_channel(866363490675326996)
        m = await c.fetch_message(929573516691517530)
        j = json.loads(m.content)
        for user in j:
            if user['id'] == ctx.author.id:
                await ctx.send("You have already applied for frag access!", hidden=True)
                return
        j.append({"id": ctx.author.id, "name": ctx.author.name, "ign": ign, "reason": reason})
        await m.edit(json.dumps(j))
        await ctx.send("You have successfully requested frag access", hidden=True)

    @scmd.cog_slash(name='ruff')
    async def _ruff(self, ctx, show=False):
        if not show:
            self.annoy += 1
            await ctx.send("Oh no! Ruffmann is an idiot I guess", hidden=True)
        else:
            await ctx.send("Hmm, that seems like a lot of times!", hidden=True)
        await ctx.channel.send(f"Ruffmann has been annoying to guild members {self.annoy} tim{'e' if self.annoy == 1 else 'es'} in the past 24 hours", components=[Button(label='Delete', style=4)])

    @scmd.cog_slash(name='version')
    async def _version(self, ctx, version_type="latest"):
        v = store('config.json', 'versions', True)
        def convert_date(date):
            d = date.split('-')
            m = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Nobember', 'December']
            if d[1].suffix == "1" and d[1].prefix != "1": daySuffix = 'st'
            elif d[1].suffix == "2": daySuffix = 'nd'
            elif d[1].suffix == "3": daySuffix = 'rd'
            else: daySuffix = 'th'
            return [m[int(d[0]) - 1], d[1] + daySuffix, "20" + d[2]]
            
        if version_type == 'latest' and v['latest'] == 'stable': version_type = 'stable'
        date = convert_date(v['date'])
        e = discord.Embed(title=f'Current version: {version_type}', color=discord.Color.green(), description=f"Date: {date[0]} {date[1]}, {date[2]}", timestamp=datetime.utcnow())
        e.set_footer("Version data retrieved")
        if version_type == 'dev':
            await ctx.send(embed=e)
            return
        e.add_field(name='Version Number', value=v['num'], inline=False)
        e.add_field(name='Full Version Name', value=v['full'], inline=False)
        e.add_field(name='Codename', value=v['codename'], inline=False)
        await ctx.send(embed=e)
    
    @scmd.cog_slash(name='senither')
    async def senither(self, ctx):
        await ctx.send("https://hypixel-leaderboard.senither.com/", hidden=True)

    # add accept/deny stuff
    @scmd.cog_slash(name='giveaway')
    async def giveaway(self, ctx, winners, time, prize):
        try:
            e = store('blacklist.json', str(ctx.author.id), True)
            print(e)
            for command in e['blacklistedCommands']:
                if command == 'giveaway':
                    await ctx.send("Sorry! You have been blacklisted from using this command.")
                    return
        except Exception as e: pass
        d = self.bot.get_channel(834960422004064266)
        e = discord.Embed(title="New giveaway request",timestamp=datetime.utcnow())
        e.add_field(name="Host", value=f"{ctx.author.mention}", inline=False)
        e.add_field(name="Winners", value=f"```{winners}```", inline=False)
        e.add_field(name="Time", value=f"```{time}```", inline=False)
        e.add_field(name="Prize", value=prize, inline=False)
        await d.send("<@&840038424332337202>", embed=e, components=[Button(label="Deny",disabled=True,style=4,id="giveaway_deny")])
        await ctx.send("Your request has been sent", hidden=True)

    async def genuser(self, ctx, setNick):
        rank = ['Non', 'Non', 'Non', 'Non', 'Non', 'VIP', 'VIP', 'VIP', 'VIP', 'VIP+', 'VIP+', 'VIP+', 'MVP', 'MVP', 'MVP+', 'MVP+', 'MVP+', 'MVP+', 'MVP++']
        randnames = ['Ender', 'Pro', 'Itz', 'YT', 'Chill', 'Mom', 'Playz', 'Games', 'Fortnite', 'Prokid', 'Monkey', 'Gamer', 'GirlGamer', 'Lowping', 'Ihave', 'Getgud', 'Istupid', '123', 'Minecraft', 'LMAO', 'non']
        f = random.choice(rank)
        if f != 'Non':
            f = f"[{f}] "
        else:
            f = ''
        def callName():
            return f + ''.join(random.choice(randnames) for i in range(random.randint(1, 8)))
        username = callName()
        while True:
            if len(username)-len(f) > 31:
                username = callName()
            else:
                break
        if setnick is False:
            await ctx.send(f"`{username}`", hidden=True)
            return
        try:
            await ctx.author.edit(nick=username)
        except:
            await ctx.send("Could not do this (you may be a higher rank than the bot)", hidden=True)
            return
        await ctx.send(f"Your new nickname is: `{username}`", hidden=True)

    async def getitem(self, ctx, item, time, *, username=None, rocks=False):
        # add item list or something
        def genuser():
            rank = ['Non', 'Non', 'Non', 'Non', 'Non', 'VIP', 'VIP', 'VIP', 'VIP', 'VIP+', 'VIP+', 'VIP+', 'MVP', 'MVP', 'MVP+', 'MVP+', 'MVP+', 'MVP+', 'MVP++']
            randnames = ['Ender', 'Pro', 'Itz', 'YT', 'Chill', 'Mom', 'Playz', 'Games', 'Fortnite', 'Prokid', 'Monkey', 'Gamer', 'GirlGamer', 'Lowping', 'Ihave', 'Getgud', 'Istupid', '123', 'Minecraft', 'LMAO', 'non']
            username = ''.join(random.choice(randnames) for i in range(random.randint(1, 8)))
            return username
        def getname():
            if username is None:
                e = genuser()
                return e
            else:
                return username
        locations = ['Graveyard', 'Castle', 'Wizard Tower', 'Barn', 'Dark Auction', 'Auction House', 'Lumber Merchant', 'Plumber Joe\'s House', 'Community Center', 'Jacob\'s House', 'Catacombs Entrance', 'Coal Mines', 'Bank', 'Builder\'s House', 'Maddox the Slayer', 'Tia the Fairy']
        location = random.choice(locations)
        e = discord.Embed(title="Dropped item(s) were found!", color=discord.Color.green(), description=f"Hurry to pick it up at the `{location}` in `Hub {random.randint(1, 40)}` before it dissapears!", timestamp=datetime.utcnow())
        if rocks is True:
            for x in range(8):
                e.add_field(name=f"`{item}` ({x + 1})", value=f"Dropped by `{getname()}`", inline=False)
        else:
            e.add_field(name=f"`{item}`", value=f"Dropped by `{getname()}`")
        e.set_footer(text=f"{time} seconds!")
        d = await ctx.send(embeds=[e])
        await sleep(time)
        g = discord.Embed(title="The item disappeared!", color=discord.Color.red())
        e.set_footer(text="Rip item")
        await d.edit(embed=g)
        await sleep(10)
        await d.delete()

def setup(bot):
    bot.add_cog(Misc(bot))

# Unused commands

# async def _getnecronstick(ctx):
    # d = ['t', 't', 't', 't', 't', 'f']
    # b = random.choice(d)
    # if b == 'f':
        # e = discord.Embed(title="No item(s) were found!", color=discord.Color.red())
        # await ctx.send(embeds=[e])
        # return
    # await commandListener.getitem(ctx, 'Necron\'s handle', 30)

# async def _getrocks(ctx):
    # await commandListener.getitem(ctx, 'Jolly Pink Rock', 60, rocks=True)

# async def acceptGuild(ctx, appID):
    # if store('config.json', 'testMode', True):
        # await ctx.send("Sorry! The bot is in test mode and this command cannot be ran at this time. Please try again later")
        # return
    # f = await ctx.send("Fetching data from api...")
    # e = store('apps.json', 'guildApps', True, app=True)
    # if appID not in e:
        # await f.edit(content="Could not find that application!")
        # return
    # r = ctx.guild.get_role(789590790669205536)
    # b = ctx.guild.get_role(831614870256353330)
    # try:
        # m = await ctx.guild.fetch_member(int(appID))
        # await m.add_roles(r)
        # await m.remove_roles(b)
    # except:
        # await ctx.send("Member lookup failed, deleting application; ask applicant to apply again.")
        # store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
        # return
    # await f.edit(content="Sending data to API...")
    # store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
    # store('apps.json', 'acceptedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=appID)
    # e = await ctx.guild.fetch_member(appID)
    # try:
        # await e.send("Your application for `Red Gladiators` has been accepted! Head over to the server to check it out!")
    # except:
        # await f.edit(content='Application accepted but could not send messages to user')
        # return
    # await f.edit(content="Application accepted")

# async def denyGuild(ctx, appID, reason):
    # f = await ctx.send("Fetching data from api...")
    # e = store('apps.json', 'guildApps', True, app=True)
    # if appID not in e:
        # await f.edit(content='Could not find that application!')
        # return
    # b = ctx.guild.get_role(831614870256353330)
    # try:
        # m = await ctx.guild.fetch_member(int(appID))
        # await m.remove_roles(b)
    # except:
        # await f.edit("Member lookup failed, deleting application; ask applicant to apply again.")
        # store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
        # return
    # await f.edit(content='Sending data to API...')
    # store('apps.json', 'guildApps', app=True, appKey=appID, pop=True)
    # store('apps.json', 'deniedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=appID)
    # e = await ctx.guild.fetch_member(appID)
    # try:
        # await e.send(f"Your application to `Red Gladiators` has been denied (by {ctx.author}). You cannot apply again. Talk to a staff member if you have any issues. Reason: {reason}")
    # except:
        # await f.edit(content="Data sent successfully but user has private messages turned off")
        # return
    # await f.edit(content="Application denied")

# async def pinglist(ctx, action, str):
#     if action != 'list' and str is None:
#         await ctx.send("You cannot leave that field blank for that operation!",hidden=True)
#         return
#     x = store('apps.json', None, True, n=True, specBin="6093310865b36740b92ef100")
#     d = x[str(ctx.author.id)]
#     if action == 'list':
#         if str(ctx.author.id) not in x:
#             await ctx.send("You do not have any words stored! Add them with `/pinglist add {word}`",hidden=True)
#             return
#         s = []
#         s.append(f"`{d['1']}`")
#         if '2' not in d:
#             s.append("Unset")
#         else:
#             s.append(f"`{d['2']}`")

#         await ctx.send(f"Your ping words are:\n{s[0]}\n{s[1]}",hidden=True)

#     # trusted role could have more?
#     elif action == 'add':
#         if '2' in d:
#             await ctx.send("You may not have more than 2 ping words! Use `/pinglist remove {index}`",hidden=True)
#             return
#         di = {}
#         if '1' not in d:
#             di['1'] = str
#             store('blah.json', str(ctx.author.id), val=di, n=True, specBin="6093310865b36740b92ef100")
#             await ctx.send(f"Added 1st word to index (`{str}`)",hidden=True)
#             return
#         else:
#             di['1'] = d['1']
#             di['2'] = str
#             store('blah.json', str(ctx.author.id), val=di, n=True, specBin="6093310865b36740b92ef100")
#             await ctx.send(f"Added 2nd word to index (`{str}`)",hidden=True)
#             return

# async def legacy(ctx, name, id):
#             await ctx.defer()
#             uuid = hystats.util.toUUID(name)
#             if uuid is False:
#                 await ctx.send(embed=discord.Embed(title="API Error",description="Could not find that username!",color=discord.Color.red()))
#                 return
#             d = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={store('config.json', 'key', True)}&uuid={uuid}")
#             if d.status_code == 429 or d.status_code == 521:
#                 await ctx.send(embed=discord.Embed(title="API Error", description=hystats.util.handleRequest(d.status_code), color=discord.Color.red()))
#                 return
#             f = d.json()
#             if f['profiles'] is None:
#                 await ctx.send(embed=discord.Embed(title="API Error", description="That user has not played skyblock!", color=discord.red()))
#                 return
#             def get_coop(pf):
#                 coopm = []
#                 isCoop = False
#                 isCoop2 = False
#                 for name, member in pf['members'].items():
#                     if "coop_invitation" in member:
#                         if member["coop_invitation"]["confirmed"] == False:
#                             coopm.append({"name":hystats.util.toName(name), "title":"Invited Coop Member"})
#                             continue
#                         isCoop = True
#                         coopm.append({"name":hystats.util.toName(name), "title":"Coop Member"})
#                     else:
#                         if isCoop2: isCoop = True
#                         coopm.append({"name":hystats.util.toName(name), "title":"Coop Owner",})
#                         isCoop2 = True
#                 if isCoop == False:
#                     coopm[0]["title"] = "Solo Profile"
#                 coop = ""
#                 first = True
#                 for member in coopm:
#                     try:
#                         if first:
#                             coop = f"**{member['name']}** ({member['title']})"
#                             first = False
#                             continue
#                         coop = f"{coop}, **{member['name']}** ({member['title']})"
#                     except:
#                         coop = "Error"
#                         break
#                 return coop
#             if id != None:
#                 pf = ''
#                 for pfl in f['profiles']:
#                     try:
#                         if pfl['cute_name'].lower() == id or pfl['cute_name'] == id:
#                             pf = pfl
#                             break
#                     except:
#                         continue
#                 if pf == '':
#                     await ctx.send(embed=discord.Embed(title="API Error",description="Could not find that profile!",color=discord.Color.red()))
#                     return
#                 def try_pass(val, bold=True, sub=None, coop=False):
#                     try:
#                         if bold and not sub:
#                             return f"**{pf['members'][uuid][val]}**"
#                         elif sub:
#                             return f"{pf['members'][uuid][val][sub]}"
#                         elif coop:
#                             return f"{pf[val][sub]}"
#                         return f"{pf['members'][uuid][val]}"
#                     except:
#                         return "Error getting value (Incomplete?)"
#                 def convert_dec(inp):
#                     try:
#                         return f"{'{:,.2f}'.format(float(inp.partition('.')[0]))[:-3]}"
#                     except Exception as e:
#                         return f"Failure converting str-int to float (Unstarted quest/task/stat?) [{e}]"
#                 store('req.json', pf)
#                 e = discord.Embed(title=f"{hystats.util.toName(uuid)} on {pf['cute_name']}", color=discord.Color.green())
#                 e.add_field(name='Coop Members', value=get_coop(pf), inline=False)
#                 e.add_field(name='Creation/Last seen', value=f"`First Join`: <t:{str(pf['members'][uuid]['first_join'])[:-3]}:D>\n`Last Seen`: <t:{str(pf['members'][uuid]['last_save'])[:-3]}:R>", inline=False)
#                 e.add_field(name='Basic info', value=f"`Skill Average`: Coming soon\n`Highest Critical Damage`: **{convert_dec(try_pass('stats', bold=False, sub='highest_critical_damage'))}**\n`Purse`: **{convert_dec(try_pass('coin_purse', False))}**\n`Bank Balance`: **{convert_dec(try_pass('banking', False, 'balance', True))}**\n`Fairy Souls`: **{try_pass('fairy_souls_collected',bold=False)} / 227**\n`Deaths`: {try_pass('death_count')}", inline=False)
#                 await ctx.send(embed=e, delete_after=60)
#                 return
#             plen = len(f['profiles'])
#             if plen == 1: pfls = "1 profile was"
#             else: pfls = f"{plen} profiles were"
#             e = discord.Embed(title=f"Profiles for user {hystats.util.toName(uuid)}", description=f"{pfls} detected for {hystats.util.gettoName(uuid)}\n\nGet more information about a profile by providing the name in the command!\n\nNOTE: Kicked coop members show up as normal, as there is no function to see if they are kicked.", color=discord.Color.green())
#             for pf in f['profiles']:
#                 # `ID`: {pf['profile_id']}
#                 msg = f"`Coop members`: {get_coop(pf)}\n`First Join`: <t:{str(pf['members'][uuid]['first_join'])[:-3]}:D>\n`Last Seen`: <t:{str(pf['members'][uuid]['last_save'])[:-3]}:R>"
#                 title = pf['cute_name']
#                 try:
#                     if pf['game_mode'] == 'ironman':
#                         title = title + " **(Ironman)**"
#                 except:
#                     pass
#                 e.add_field(name=title, value=msg, inline=False)
#             await ctx.send(embed=e)
