import cogs
import json
import re
import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from cogs.applications import store
from datetime import datetime

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        y = store('rroles.json', None, True)
        if payload.emoji.id == 815831189696413698:
            blacklistChannel = self.bot.get_channel(880550264564748368)
            blacklist = await blacklistChannel.history(limit=100).flatten()
            for blacklistitem in blacklist:
                if str(payload.channel_id) == blacklistitem: return
            check = self.bot.get_channel(880550772021010433)
            checkHistory = await check.history(limit=500).flatten()
            # needs to be squished, 10 starboards per messsage or something like that
            for message in checkHistory:
                if str(payload.message_id) == message.content: return
            cat = self.bot.get_channel(880550245841403904)
            ch = None
            for channel in cat.channels:
                if channel.name == str(payload.message_id):
                    ch = channel
                    break
            if ch == None:
                c = await cat.create_text_channel(str(payload.message_id), reason="New starboard")
                await c.send(f"{payload.user_id}")
                return
            history = await ch.history(limit=1).flatten()
            newhistory = f"{history[0].content}-{payload.user_id}"
            await history[0].edit(content=newhistory)
            members = newhistory.split('-')
            if len(members) >= 3:
                starboard = self.bot.get_channel(871491040224378940)
                messageChannel = self.bot.get_channel(payload.channel_id)
                message = await messageChannel.fetch_message(payload.message_id)
                embed = discord.Embed(description=message.content, color=discord.Color.blue())
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                if len(message.attachments) != 0:
                    embed.set_image(url=message.attachments[0].url)
                await starboard.send(embed=embed)
                await ch.delete(reason="Starboard has 3 reactions")
                await check.send(f"{payload.message_id}")
                return

        if str(payload.message_id) in y['rroles']:
            for msg in y['rroles']:
                if str(payload.message_id) == msg:
                    if payload.emoji.name == "✅":
                        guild = self.bot.get_guild(payload.guild_id)
                        role = guild.get_role(int(y['rrolesrole'][msg]))
                        await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        x = store('rroles.json', None, True)
        if str(payload.message_id) in x['rroles']:
            for msg in x['rroles']:
                if str(payload.message_id) == msg:
                    if payload.emoji.name == "✅":
                        guild = self.bot.get_guild(payload.guild_id)
                        member = await guild.fetch_member(payload.user_id)
                        role = guild.get_role(int(x['rrolesrole'][msg]))
                        await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        try:
                label = interaction.component.label
                ide = interaction.component.id
        except:
            print("error setting id")
            ide = None
        if label == "Verify" or ide == "verify":
            role = interaction.message.guild.get_role(788914323485491232)
            mrole = interaction.message.guild.get_role(788890991028469792)
            member = await interaction.message.guild.fetch_member(interaction.user.id)
            await member.add_roles(role)
            await member.remove_roles(mrole)
            await interaction.respond(type=6)
        elif label == "Accept App":
            ide = ide.replace('-a', '')
            await interaction.respond(type=6)
            ctx = interaction.message.guild.get_channel(831579949415530527)
            f = await ctx.send("Fetching data from api...")
            e = store('apps.json', 'guildApps', True, app=True)
            if ide not in e:
                await f.edit(content="Could not find that application!")
                return
            r = ctx.guild.get_role(789590790669205536)
            b = ctx.guild.get_role(831614870256353330)
            try:
                m = await ctx.guild.fetch_member(int(ide))
                await m.add_roles(r)
                await m.remove_roles(b)
            except:
                await ctx.send("Member lookup failed, deleting application; ask applicant to apply again.")
                await interaction.message.delete()
                store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
                return
            await f.edit(content="Sending data to API...")
            store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
            store('apps.json', 'acceptedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=ide)
            e = await ctx.guild.fetch_member(ide)
            try:
                await e.send(f"Your application for `Red Gladiators` has been accepted by `{interaction.user}`! Head over to the server to check it out!")
            except:
                await f.edit(content='Application accepted but user has private messages turned off')
                await interaction.message.edit(components=[])
                return
            await f.edit(content="Application accepted")
            await interaction.message.edit(components=[])
        elif label == "Deny App":
            ide = ide.replace('-d', '')
            ctx = interaction.message.guild.get_channel(831579949415530527)
            await interaction.respond(type=6)
            f = await ctx.send("Fetching data from api...")
            e = store('apps.json', 'guildApps', True, app=True)
            if ide not in e:
                await f.edit(content='Could not find that application!')
                return
            b = ctx.guild.get_role(831614870256353330)
            try:
                m = await ctx.guild.fetch_member(int(ide))
                await m.remove_roles(b)
            except:
                await f.edit("Member lookup failed, deleting application; ask applicant to apply again.")
                await interaction.message.delete()
                store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
                return
            await f.edit(content='Sending data to API...')
            store('apps.json', 'guildApps', app=True, appKey=ide, pop=True)
            store('apps.json', 'deniedGuildApps', val=f"{datetime.utcnow()}", app=True, appKey=ide)
            e = await ctx.guild.fetch_member(ide)
            try:
                await e.send(f"Your application to `Red Gladiators` has been denied by `{interaction.user}`. You cannot apply again. Talk to a staff member if you have any issues.")
            except:
                await f.edit(content="Application denied successfully but user has private messages turned off")
                await interaction.message.edit(components=[])
                return
            await f.edit(content="Application denied")
            # add feature to get embed and change it into
            await interaction.message.edit(components=[])
        elif label == "Vote Yes":
            ide = ide.replace('POLLYES', '')
            cat = self.bot.get_channel(876182017400766544)
            c = None
            for channel in cat.channels:
                if channel.name == ide:
                    c = channel
                    break
            if c == None:
                await interaction.respond(content="Sorry, the poll ID was not found! Try again later or contact trngl.")
                return
            messages = await c.history(limit=4).flatten()
            x = json.loads(messages[1].content)
            users = []
            if messages[0].content != "No user data":
                users = messages[0].content.split('-')
            try:
                if str(interaction.user.id) in users:
                    await interaction.respond(content="You have already responded to this poll!")
                    return
                x['yes'] = int(x['yes'])
                x['yes'] += 1
                e = interaction.message.embeds[0]
                e.set_field_at(0, name='Yes', value=x['yes'])
                await interaction.message.edit(embed=e)
                if messages[0].content != "No user data":
                    await messages[0].edit(content=f"{messages[0].content}-{interaction.user.id}")
                else:
                    await messages[0].edit(content=f"{interaction.user.id}")
                await messages[1].edit(content=f"{json.dumps(x)}")
                await interaction.respond(type=6)
            except:
                await interaction.respond(content="There was an error executing this!")
        elif label == "Vote No":
            ide = ide.replace('POLLNO', '')
            cat = self.bot.get_channel(876182017400766544)
            c = None
            for channel in cat.channels:
                if channel.name == ide:
                    c = channel
                    break
            if c == None:
                await interaction.respond(content="Sorry, the poll ID was not found! Try again later or contact trngl.")
                return
            messages = await c.history(limit=4).flatten()
            x = json.loads(messages[1].content)
            users = []
            if messages[0].content != "No user data":
                users = messages[0].content.split('-')
            try:
                if str(interaction.user.id) in users:
                    await interaction.respond(content="You have already responded to this poll!")
                    return
                x['no'] = int(x['no'])
                x['no'] += 1
                e = interaction.message.embeds[0]
                e.set_field_at(1, name='No', value=x['no'])
                await interaction.message.edit(embed=e)
                if messages[0].content != "No user data":
                    await messages[0].edit(content=f"{messages[0].content}-{interaction.user.id}")
                else:
                    await messages[0].edit(content=f"{interaction.user.id}")
                await messages[1].edit(content=f"{json.dumps(x)}")
                await interaction.respond(type=6)
            except:
                await interaction.respond(content="There was an error executing this!")
        elif label == "Remove" or ide == "remove":
            await interaction.message.delete()
        try:
            if ide == "deverify":
                role = interaction.message.guild.get_role(788914323485491232)
                mrole = interaction.message.guild.get_role(788890991028469792)
                member = await interaction.message.guild.fetch_member(interaction.user.id)
                await member.add_roles(mrole)
                await member.remove_roles(role)
                await interaction.respond(type=7, content=f"LMFAOOOOOO L L L L {member.name} JUST GOT CLWOON'd ON L L L L L L L GET L KID")
        except:
            pass
        try:
            userid = ide.split('-')[0]
        except:
            userid = ide
        if str(interaction.user.id) != userid: return
        if label == 'Exit' or ide == "exit":
            await interaction.message.edit(components=[])
        elif label == 'Delete' or ide == "delete":
            await interaction.message.delete()

    @commands.Cog.listener()
    async def on_select_option(self, interaction):
        try:
            label = interaction.component[0].to_dict()['label']
            val = interaction.component[0].to_dict()['value']
        except:
            print("error setting id")
            val = None
        if val.startswith("SelectPoll"):
            val = val.split('-')
            mid = val[1]
            cat = self.bot.get_channel(876182017400766544)
            c = None
            for channel in cat.channels:
                if channel.name == mid:
                    c = channel
                    break
            if c == None:
                await interaction.respond(content="Sorry, the poll ID was not found! Try again later or contact trngl.")
                return
            messages = await c.history(limit=4).flatten()
            x = json.loads(messages[1].content)
            users = []
            if messages[0].content != "No user data":
                users = messages[0].content.split('-')
            try:
                if str(interaction.user.id) in users:
                    await interaction.respond(content="You have already responed to this poll!")
                    return
                if messages[0].content != "No user data":
                    await messages[0].edit(content=f"{messages[0].content}-{interaction.user.id}")
                else:
                    await messages[0].edit(content=f"{interaction.user.id}")
                x['fields'][label] = int(x['fields'][label])
                x['fields'][label] += 1
                await messages[1].edit(content=f"{json.dumps(x)}")
                if val[2] != 'T':
                    e = interaction.message.embeds[0]
                    e.set_field_at(x['fieldpos'][label], name=label, value=x['fields'][label], inline=False)
                    await interaction.message.edit(embed=e)
                await interaction.respond(type=6)
            except:
                await interaction.respond(content="There was an error executing this!")

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        if message.author.bot: return
        if message.author.id != 713461668667195553:
            if message.author.id == 406629388059410434:
                if message.content == 'embed':
                    await message.delete()
                    e = discord.Embed(title="Verification", color=discord.Color.blurple())
                    e.add_field(name="Verify", value="To verify, click the button below. If you get a `This interaction failed` message, please talk to <@!406629388059410434>.", inline=False)
                    e.add_field(name="Read the rules", value="Make sure to read our <#788887107544285244>!")
                    e.add_field(name="Join the guild!",value="To join the Guild, you first must verify, then check out the <#822915132153135144> channel.", inline=False)
                    e.add_field(name='Need support?', value="If you ever need support, you can create a ticket in <#866426260573650966>.", inline=False)
                    e.set_footer(text="Thank you for joining!")
                    d = await ctx.send(embed=e, components=[Button(label='Verify', style=1)])
                    store('config.json', 'verifyV2', val=f'{d.id}')
        if message.channel.id == 788889735157907487:
            if message.author.id == 392502213341216769 or message.author.id == 159985870458322944:
                splitted = message.content.split(' ')
                if int(splitted[7][:-1])%10 != 0:
                    return
                userid = re.sub("[^0-9]", "", splitted[1])
                user = await message.guild.fetch_member(int(userid))
                roleid = {"40!": 865832933028528158, "30!": 865832837948244009, "20!": 864125893660508161, "10!": 841066567151910932}
                role = message.guild.get_role(roleid[splitted[7]])
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        d = store('expose.json', None, True)
        files = []
        if message.attachments != []:
            for file in message.attachments:
                files.append(file.url)
        d[str(message.channel.id)] = {
            "content": message.content,
            "author": f"{message.author}",
            "author_icon": f"{message.author.avatar_url}",
            "files": files
        }
        store('expose.json', d)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            e = discord.Embed(title="You do not have permission to do this!", color=discord.Color.red())
            await ctx.send(embed=e, delete_after=3)
        elif isinstance(error, commands.CommandNotFound):
            e = discord.Embed(title="Command not found!", color=discord.Color.red())
            await ctx.send(embed=e, delete_after=3)
        else:
            e = discord.Embed(title="An exception occurred", description=f"{error}")
            await cogs.util.bugReport(self.bot, f'`Command Error` {ctx.message.content}', f"{error}")
            await ctx.send(embed=e, delete_after=10)

def setup(bot):
    bot.add_cog(Listeners(bot))
