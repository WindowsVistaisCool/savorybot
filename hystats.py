class util:
    def handleRequest(status_code, err=True):
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
                return '**429** Too many requests!'
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

    def getOnline(name):
        key = store("config.json", "key", True)
        uuid = util.toUUID(name)
        if uuid == False:
            return ['err', 'Could not find that username!']
        ruf = requests.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid}')
        sus = requests.get(f"https://api.hypixel.net/player?key={key}&name={name}")
        res = sus
        # print(res.json())
        if res.status_code == 429 or res.status_code == 521:
            return ['err', util.handleRequest(res.status_code)]
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

# sbprofiles
class profiles:
    async def profiles(client, ct, name):
        # placeholder so slash interaction doesn't fail
        await ct.send("Getting data...",delete_after=3)
        ctx = client.get_channel(ct.channel.id)
        uuid = util.toUUID(name)
        if uuid is False:
            await ctx.send(embed=discord.Embed(title="API Error",description="Could not find that username!",color=discord.Color.red()), components=[Button(label="Remove",style=4)])
            return
        d = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={store('config.json', 'key', True)}&uuid={uuid}")
        if d.status_code == 429 or d.status_code == 521:
            await ctx.send(embed=discord.Embed(title="API Error", description=util.handleRequest(d.status_code), color=discord.Color.red()), components=[Button(label="Remove",style=4)])
            return
        f = d.json()
        if f['profiles'] is None:
            await ctx.send(embed=discord.Embed(title="API Error", description="That user has not played skyblock!", color=discord.Color.red()), components=[Button(label="Remove",style=4)])
            return
        def get_coop(pf):
            coopm = []
            isCoop = False
            isCoop2 = False
            for name, member in pf['members'].items():
                if "coop_invitation" in member:
                    if member["coop_invitation"]["confirmed"] == False:
                        coopm.append({"name":util.toName(name), "title":"Invited Coop Member"})
                        continue
                    isCoop = True
                    coopm.append({"name":util.toName(name), "title":"Coop Member"})
                else:
                    if isCoop2: isCoop = True
                    coopm.append({"name":util.toName(name), "title":"Coop Owner",})
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
        e = discord.Embed(title=f"Profiles for user {util.toName(uuid)}", description=f"{pfls} detected for {util.toName(uuid)}\n\nGet more information about a profile by selecting the name below!\n\nNOTE: Kicked coop members show up as normal, as there is no function to see if they are kicked.", color=discord.Color.green())
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
        de = await ctx.send(embed=e, components=[Select(placeholder="Select profile",options=labels)])
        while True:
            try:
                interaction = await client.wait_for("select_option", timeout=90.0)
                if interaction.user.id != ct.author.id: continue
                break
            except:
                try:
                    await de.edit(components=[])
                except:
                    pass
                return
        await interaction.respond(type=6)
        await de.edit(content="Loading data...", embeds=[], components=[])
        id = interaction.component[0].label
        pf = ''
        for pfl in f['profiles']:
            try:
                if pfl['cute_name'] == id:
                    pf = pfl
                    break
            except:
                continue
        if pf == '':
            await ctx.send(embed=discord.Embed(title="API Error",description="Could not find that profile! (Internal error, not your fault)",color=discord.Color.red()), components=[Button(label="Remove",style=4)])
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
        # store('req.json', pf)
        e = discord.Embed(title=f"{util.toName(uuid)} on {pf['cute_name']}", color=discord.Color.green())
        e.add_field(name='Coop Members', value=get_coop(pf), inline=False)
        e.add_field(name='Creation/Last seen', value=f"`First Join`: <t:{str(pf['members'][uuid]['first_join'])[:-3]}:D>\n`Last Seen`: <t:{str(pf['members'][uuid]['last_save'])[:-3]}:R>", inline=False)
        e.add_field(name='Basic info', value=f"`Skill Average`: Coming soon\n`Highest Critical Damage`: **{convert_dec(try_pass('stats', bold=False, sub='highest_critical_damage'))}**\n`Purse`: **{convert_dec(try_pass('coin_purse', False))}**\n`Bank Balance`: **{convert_dec(try_pass('banking', False, 'balance', True))}**\n`Fairy Souls`: **{try_pass('fairy_souls_collected',bold=False)} / 227**\n`Deaths`: {try_pass('death_count')}", inline=False)
        await de.edit(content='', embed=e, components=[[Button(label="Exit", id=f"{ct.author.id}-H"), Button(label="Delete",style=4, id=f"{ct.author.id}-D")]])


# add modes later
def sbmode(g):
    return g

async def status(client, ctx, user):
    e = discord.Embed(title="Fetching data from api...", color=discord.Color.blurple())
    a = await ctx.send(embeds=[e])
    o = util.getOnline(user)
    color = 0x000000
    description = "Error"
    on = False
    if o[0] is True:
        color = discord.Color.green()
        description = f"{user} is currently ONLINE"
        on = True
    elif o[0] is False:
        color = discord.Color.red()
        description = f"{user} is currently OFFLINE"
    elif o[0] == 'err':
        e = discord.Embed(title="API Error", color=discord.Color.red(), description=o[1])
        await a.edit(embed=e)
        return
    def timeC():
        if o[0]:
            return datetime.utcnow()
        else:
            return o[1]
    def fC():
        if o[0]:
            return "Lookup at"
        else:
            return "[UTC] Offline since"
    e = discord.Embed(title=f"Status of {user}", color=color, description=description, timestamp=timeC())
    e.set_footer(text=fC())
    if on is True:
        e.add_field(name="Game", value=o[1])
        game = o[2]
        if o[1] == 'SKYBLOCK':
            game = sbmode(o[2])
        e.add_field(name="Mode", value=game)
    await a.edit(embed=e)
