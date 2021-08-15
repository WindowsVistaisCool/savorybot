import cogs
import json
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
        if message.author.id != 713461668667195553:
            if message.author.id == 392502213341216769:
                if message.content == 'embed':
                    await message.delete()
                    e = discord.Embed(title="Verification", color=discord.Color.blurple())
                    e.add_field(name="Verify", value="To verify, click the button below. If you do not see the button or get a `This interaction failed` message, please update your discord app or talk to `ruffmann#2668`.", inline=False)
                    e.add_field(name="Join Guild",value="To join the Guild, you first must verify, then see the `#guild-applications` channel.", inline=False)
                    e.set_footer(text="Thank you for joining!")
                    d = await ctx.send(embed=e, components=[Button(label='Verify', style=1)])
                    store('config.json', 'verifyV2', val=f'{d.id}')
        if message.channel.id == 788886124159828012:
            if message.content.startswith('.n ') or message.content.startswith('.d ') or 'sbs guild' in message.content or message.content.startswith('.sk ') or message.content.startswith('.s '):
                await message.reply(content='Please use this command in the bot commands channel!')

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
            await ctx.send(embed=e, delete_after=10)

def load(bot):
    bot.add_cog(Listeners(bot))
