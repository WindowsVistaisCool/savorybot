import requests
import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from datetime import datetime
from asyncio import sleep
from cogs.util import store, bugReport

class hyutil:
    def handleRequest(status_code, err=True):
        # add success codes too
        if err == True:
            # Client errors
            if status_code == 400:
                return '**400** Bad Request'
            elif status_code == 401:
                return '**401** Invalid Authorization'
            elif status_code == 403:
                return '**403** Forbidden'
            elif status_code == 404:
                return '**404** Not found'
            elif status_code == 408:
                return '**408** Request timed out'
            elif status_code == 413:
                return '**413** Payload too large'
            elif status_code == 418:
                return '**418** I\'m a teapot! I can\'t brew coffee!'
            elif status_code == 429:
                return '**429** Too many requests (or API name looked up recently)!'
            # Server errors
            elif status_code == 500:
                return '***500*** Internal Server Error'
            elif status_code == 502:
                return '***502*** Bad gateway'
            elif status_code == 503:
                return '***503*** Service down'
            elif status_code == 504:
                return '***504*** Gateway timeout'
            # Cloudflare
            elif status_code == 520:
                return '**520** Server returned unkown error'
            elif status_code == 521 or status_code == 523:
                return f'**{status_code}** Origin is unreachable'
            elif status_code == 522:
                return '**522** Connection timed out'
            else:
                return
        else:
            return

    def testAPIKey(key):
        responsejson = key.json()
        if responsejson['success'] == False:
            return [False, responsejson['cause']]
        else:
            return [True, None]

    def getOnline(name):
        key = store("config.json", "key", True)
        uuid = hyutil.toUUID(name)
        if uuid == False:
            return ['err', 'Could not find that username!']
        ruf = requests.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid}')
        sus = requests.get(f"https://api.hypixel.net/player?key={key}&name={name}")
        res = sus
        # print(res.json())
        if res.status_code == 429:
            return ['err', hyutil.handleRequest(res.status_code)]
        ruff = ruf.json()
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
            try:
                time = datetime.fromtimestamp(int(sus["player"]["lastLogout"])/1000)
                return [False, time, res]
            except:
                return [False, "Invalid Timestamp", res]

    # add modes later
    def sbmode(g):
        return g

    def toUUID(name):
        d = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
        if d.status_code == 204:
            return False
        return d.json()["id"]

    def toName(uuid):
        # add other features later
        d = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")
        if d.status_code == 204:
            return False
        return d.json()[-1]['name']

class HyStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @scmd.cog_subcommand(base='hy', name='profiles')
    async def profiles(self, ctx, user):
        name = user
        # placeholder so slash interaction doesn't fail
        await ctx.send("Retrieving data...",delete_after=3)
        uuid = hyutil.toUUID(name)
        if uuid is False:
            await ctx.channel.send(embed=discord.Embed(title="API Error",description="Could not find that username!",color=discord.Color.red())) #, components=[Button(label="Remove",style=4)])
            return
        d = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={store('config.json', 'key', True)}&uuid={uuid}")
        if d.status_code == 429 or d.status_code == 521:
            await ctx.channel.send(embed=discord.Embed(title="API Error", description=hyutil.handleRequest(d.status_code), color=discord.Color.red())) #, components=[Button(label="Remove",style=4)])
            return
        testAPI = hyutil.testAPIKey(d)
        if testAPI[0] == False:
            await ctx.channel.send(embed=discord.Embed(title="Unknown API error", description=testAPI[1], color=discord.Color.red()))
            await bugReport(self.bot, f'`/hy profiles user:{user}` Unknown API error', testAPI[1])
            return
        f = d.json()
        if f['profiles'] is None:
            await ctx.channel.send(embed=discord.Embed(title="API Error", description="That user has not played skyblock!", color=discord.Color.red())) #, components=[Button(label="Remove",style=4)])
            return
        def get_coop(pf):
            coopm = []
            isCoop = False
            isCoop2 = False
            for name, member in pf['members'].items():
                if "coop_invitation" in member:
                    if member["coop_invitation"]["confirmed"] == False:
                        coopm.append({"name":hyutil.toName(name), "title":"Invited Coop Member"})
                        continue
                    isCoop = True
                    coopm.append({"name":hyutil.toName(name), "title":"Coop Member"})
                else:
                    if isCoop2: isCoop = True
                    coopm.append({"name":hyutil.toName(name), "title":"Coop Owner",})
                    isCoop2 = True
            if isCoop == False:
                coopm[0]["title"] = "Solo Profile"
            coop = ""
            first = True
            for member in coopm:
                try:
                    if first:
                        coop = f"**{member['name']}** ({member['title']})"
                        first = False
                        continue
                    coop = f"{coop}, **{member['name']}** ({member['title']})"
                except:
                    coop = "Error"
                    break
            return coop
        plen = len(f['profiles'])
        if plen == 1: pfls = "1 profile was"
        else: pfls = f"{plen} profiles were"
        labels = []
        e = discord.Embed(title=f"Profiles for user {hyutil.toName(uuid)}", description=f"{pfls} detected for {hyutil.toName(uuid)}\n\nGet more information about a profile by selecting the name below!\n\nNOTE: Kicked coop members show up as normal, as there is no function to see if they are kicked.", color=discord.Color.green())
        for pf in f['profiles']:
            # `ID`: {pf['profile_id']}
            msg = f"`Coop members`: {get_coop(pf)}\n`First Join`: <t:{str(pf['members'][uuid]['first_join'])[:-3]}:D>\n`Last Seen`: <t:{str(pf['members'][uuid]['last_save'])[:-3]}:R>"
            title = pf['cute_name']
            labels.append(SelectOption(label=title, value=title.lower()))
            try:
                if pf['game_mode'] == 'ironman':
                    title = title + " **(Ironman)**"
            except:
                pass
            e.add_field(name=title, value=msg, inline=False)
        # temp return here becuase selects aren't slash friendly
        await ctx.channel.send(embed=e)
        return
        try:
            de = await ctx.channel.send(embed=e, components=[Select(placeholder="Select profile",options=labels, id='nolistener')])
        except Exception as e:
            await ctx.channel.send(f"An error occurred while executing this command! ({e})")
            return
        while True:
            try:
                interaction = await self.bot.wait_for("select_option", timeout=90.0)
                if interaction.user.id != ctx.author.id: continue
                break
            except:
                try:
                    await de.edit(components=[])
                except:
                    pass
                return
        await interaction.respond(type=6)
        id = interaction.values[0]
        await ctx.send(id)
        await de.edit(content="Loading data...", embeds=[], components=[])
        pf = ''
        for pfl in f['profiles']:
            try:
                if pfl['cute_name'].lower() == id:
                    pf = pfl
                    break
            except Exception as e:
                print(e)
                continue
        if pf == '':
            await ctx.channel.send(embed=discord.Embed(title="API Error",description="Could not find that profile! (Internal error, not your fault)",color=discord.Color.red()), components=[Button(label="Remove",style=4)])
            return
        def try_pass(val, bold=True, sub=None, coop=False):
            try:
                if bold and not sub:
                    return f"**{pf['members'][uuid][val]}**"
                elif sub:
                    return f"{pf['members'][uuid][val][sub]}"
                elif coop:
                    return f"{pf[val][sub]}"
                return f"{pf['members'][uuid][val]}"
            except:
                return "Error getting value (Incomplete?)"
        def convert_dec(inp):
            try:
                # used to convert floats to human readable numbers
                return f"{'{:,.2f}'.format(float(inp.partition('.')[0]))[:-3]}"
            except:
                return f"Failure getting value"
        e = discord.Embed(title=f"{hyutil.toName(uuid)} on {pf['cute_name']}", color=discord.Color.green())
        e.add_field(name='Coop Members', value=get_coop(pf), inline=False)
        e.add_field(name='Creation/Last seen', value=f"`First Join`: <t:{str(pf['members'][uuid]['first_join'])[:-3]}:D>\n`Last Seen`: <t:{str(pf['members'][uuid]['last_save'])[:-3]}:R>", inline=False)
        e.add_field(name='Basic info', value=f"`Skill Average`: Coming soon\n`Highest Critical Damage`: **{convert_dec(try_pass('stats', bold=False, sub='highest_critical_damage'))}**\n`Purse`: **{convert_dec(try_pass('coin_purse', False))}**\n`Bank Balance`: **{convert_dec(try_pass('banking', False, 'balance', True))}**\n`Fairy Souls`: **{try_pass('fairy_souls_collected',bold=False)} / 227**\n`Deaths`: {try_pass('death_count')}", inline=False)
        await de.edit(content='', embed=e, components=[[Button(label="Exit", id=f"{ctx.author.id}"), Button(label="Delete",style=4, id=f"{ctx.author.id}")]])

    @scmd.cog_subcommand(base='hy', name='status')
    async def status(self, ctx, username):
        user = username
        e = discord.Embed(title="Fetching data from api...", color=discord.Color.blurple())
        a = await ctx.send(embeds=[e])
        o = hyutil.getOnline(user)
        color = 0x000000
        description = "Error"
        on = False
        if o[0] is True:
            color = discord.Color.green()
            description = f"{user} is currently **ONLINE**"
            on = True
        elif o[0] is False:
            color = discord.Color.red()
            description = f"{user} is currently **OFFLINE**"
        elif o[0] == 'err':
            e = discord.Embed(title="API Error", color=discord.Color.red(), description=o[1])
            await a.edit(embed=e)
            return
        def timeC():
            if o[0] == True:
                return datetime.utcnow()
            else:
                return o[1]
        def fC():
            if o[0]:
                return "Lookup at"
            else:
                return "Offline since"
        try:
            e = discord.Embed(title=f"Status of {user}", color=color, description=description, timestamp=timeC())
        except:
            e = discord.Embed(title=f"Status of {user} (invalid timestamp passed)", color=color, description=description)
        e.set_footer(text=fC())
        if on is True:
            e.add_field(name="Game", value=o[1])
            game = o[2]
            if o[1] == 'SKYBLOCK':
                game = util.sbmode(o[2])
            e.add_field(name="Mode", value=game)
        await a.edit(embed=e)

    @scmd.cog_subcommand(base='hy', name='counts')
    async def counts(self, ctx, gamemode='SKYBLOCK'):
        type = gamemode
        await ctx.defer()
        gmname = "(not yet implemented)"
        if type == 'SKYBLOCK':
            gmname = 'Skyblock'
        elif type == 'BEDWARS':
            gmname = 'Bedwars'
        elif type == 'SKYWARS':
            gmname = 'Skywars'
        elif type == 'ARCADE':
            gmname = "Arcade Games"
        elif type == "TNT":
            gmname = "TNT Games"
        elif type == "BUILD":
            gmname = "Build Battle"
        elif type == 'LEGACY':
            gmname = 'Legacy Games'
        elif type == 'etc':
            gmname = 'SMP/Replay/Housing/Pit/Tournament/Prototype'
        counts = requests.get(f'https://api.hypixel.net/counts?key={store("config.json", "key", True)}')
        if counts.status_code == 521:
            await ctx.send(embed=discord.Embed(title="API Error", description=handleRequest(counts.status_code), color=discord.Color.red()))
            return
        count = counts.json()
        testAPI = hyutil.testAPIKey(counts)
        if testAPI[0] == False:
            await ctx.send(embed=discord.Embed(title="Unknown API Error", description=testAPI[1], color=discord.Color.red()))
            await bugReport(self.bot, f'`/hy counts gamemode:{gamemode}`', testAPI[1])
            return
        e = discord.Embed(title=f"Player counts for {gmname}", description=f"**Network-wide player count**\n```yaml\n{count['playerCount']}```", color=discord.Color.blurple(), timestamp=datetime.utcnow())
        e.set_footer(text='Counts recieved')
        def af(name, value=None, inline=True, *, total=None):
            if total != None:
                e.add_field(name=name, value=f'```fix\n{total["players"]}```', inline=False)
                return
            e.add_field(name=name, value=f'`{value}`', inline=inline)
        def modeLoop(rawName, fancyName, modes, inLine=None):
            for x in range(len(rawName)):
                try:
                    thing = fancyName[x-1]
                    if thing == None: thing = rawName[x-1]
                    af(thing, modes[rawName[x-1]])
                except: continue
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
            e.add_field(name='Crystal Hollows', value='`0`')
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
            modeLoop(rawModes, fancyModes, modes)
        elif type == 'SKYWARS':
            base = count['games'][type]
            modes = base["modes"]
            e.add_field(name='Total Skywars count', value=f'```fix\n{base["players"]}```', inline=False)
            e.add_field(name='Solo Normal', value=f'`{modes["solo_normal"]}`')
            e.add_field(name='Teams Normal', value=f'`{modes["teams_normal"]}`')
            e.add_field(name='More games coming later', value='NOT SOON')
        elif type == 'ARCADE':
            base = count['games'][type]
            modes = base['modes']
            af('Total Arcade Games count', total=base)
            rawName = ['PARTY', 'HOLE_IN_THE_WALL', 'DEFENDER', 'MINI_WALLS', 'SIMON_SAYS', 'ZOMBIES_BAD_BLOOD', 'HIDE_AND_SEEK_PARTY_POOPER', 'DAYONE', 'DRAW_THEIR_THING', 'ZOMBIES_ALIEN_ARCADIUM', 'ONEINTHEQUIVER', 'SOCCER', 'PVP_CTW', 'THROW_OUT', 'ENDER', 'STARWARS', 'DRAGONWARS2', 'ZOMBIES_DEAD_END', 'FARM_HUNT', 'HIDE_AND_SEEK_PROP_HUNT']
            fancyName = ['Party Games', 'Hole in the Wall', None, 'Mini Walls', 'Simon Says', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
            # inLine = []
            modeLoop(rawName, fancyName, modes)
        elif type == 'TNT':
            base = count['games']['TNTGAMES']
            modes = base['modes']
            af('Total TNT Games count', total=base)
            rawName = ['TNTAG', 'TNTRUN', 'BOWSPLEEF', 'PVPRUN', 'CAPTURE']
            fancyName = ['TNT Tag', 'TNT Run', 'Bow Spleef', 'PvP Run', None]
            modeLoop(rawName, fancyName, modes)
        elif type == 'BUILD':
            base = count['games']['BUILD_BATTLE']
            modes = base['modes']
            af('Total Build Battle count', total=base)
            rawName = ['BUILD_BATTLE_SOLO_NORMAL_LATEST', 'BUILD_BATTLE_SOLO_NORMAL', 'BUILD_BATTLE_GUESS_THE_BUILD', 'BUILD_BATTLE_SOLO_PRO', 'BUILD_BATTLE_TEAMS_NORMAL']
            fancyName = ['Solo Normal Latest', 'Solo Normal', 'Guess the Build', 'Solo Pro', 'Teams Normal']
            modeLoop(rawName, fancyName, modes)
        elif type == 'LEGACY':
            base = count['games'][type]
            modes = base['modes']
            af('Total Legacy Games count', total=base)
            rawName = ['WALLS', 'ARENA', 'QUAKECRAFT', 'PAINTBALL', 'VAMPIREZ', 'GINGERBREAD']
            fancyName = ['Walls', 'Arena', 'Quakecraft', 'Paintball', 'Vampirez', None]
            modeLoop(rawName, fancyName, modes)
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
        await ctx.send(embed=e, delete_after=40)

def setup(bot):
    bot.add_cog(HyStats(bot))
