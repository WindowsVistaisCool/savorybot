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

async def get_ready(bot):
    load_cogs(bot)
    await ready_status(bot, store('config.json', None, True))
    print("Ready")

def load_cogs(bot):
    cogs.applications.load(bot)
    cogs.btesting.load(bot)
    cogs.hystats.load(bot)
    cogs.listeners.load(bot)
    cogs.misc.load(bot)
    cogs.owner.load(bot)
    cogs.polls.load(bot)
    cogs.trusted.load(bot)

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
