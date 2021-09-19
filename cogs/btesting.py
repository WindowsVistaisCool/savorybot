import discord
import json
import random
import slashrequest
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from cogs.util import store
from itertools import accumulate

class bTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # enable/disable
    @commands.group()
    @commands.is_owner()
    async def bt(self, ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid sub")

    @bt.command(name='enable')
    async def bt_enable(self, ctx, roleid):
        slashrequest.sc.post(store('config.json', 'bt', True))
        e = slashrequest.sc.get('bt')['id']
        slashrequest.sc.perm(e, [roleid], [True])
        await ctx.send("Added bot testing commands")

    @bt.command(name='disable')
    async def bt_disable(self, ctx):
        slashrequest.sc.rem('bt')
        await ctx.send("Removed bot testing commands")

    @scmd.cog_subcommand(base='bt', name='info')
    async def _bt_info(self, ctx):
        await ctx.send("You're here because you signed up to help me improve this bot! **DO NOT USE THESE COMMANDS OUTSIDE OF THE #bot-testing CHANNEL. YOU WILL RECIEVE A WARNING!** If you recieve a message saying \"This interaction failed\", *please let me know as soon as possible*! Thank you for signing up and helping me test new features!", hidden=True)

    # testing commands
    @scmd.cog_subcommand(base='bt', name='interaction')
    async def btInteraction(self, ctx, type):
        await ctx.defer()
        c = self.bot.get_channel(ctx.channel.id)
        if type == 'b':
            m = await c.send(f"These are test buttons! ({ctx.author})", components=[Button(label="Test")])
            while True:
                interaction = await self.bot.wait_for("button_click", check=lambda i: i.component.label.startswith("Test"))
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
                interaction = await self.bot.wait_for("select_option")
                if interaction.user.id != ctx.author.id:
                    mem = await ctx.guild.fetch_member(interaction.user.id)
                    await ctx.send(f"{mem.mention}, this isn't your menu!")
                    continue
                break
            await m.edit(content=f"Expired menu - {ctx.author.name} selected {interaction.values[0]}",components=[])
            await interaction.respond(content="You selected an item!")

    @scmd.cog_subcommand(base='bt', name='roll')
    async def btRoll(self, ctx):
        c = self.bot.get_channel(889169342997069825)
        messages = await c.history(limit=4).flatten()
        x = json.loads(messages[0].content)
        us = []
        west = []
        eu = []
        for key, val in x.items():
            if val['timezone'] == 'us-east':
                us.append(int(key))
                continue
            elif val['timezone'] == 'us-west':
                west.append(int(key))
                continue
            elif val['timezone'] == 'eu':
                eu.append(int(key))
        n = len(x)
        g = 3
        size = n // g
        rem = n % g
        separators = list(accumulate([0] + [size+1] * rem + [size] * (g - rem)))

        # Make raw data
        items = list(range(n))
        random.shuffle(items)

        # Iterate and print
        for i, s in enumerate(zip(separators, separators[1:])):
            group = items[slice(*s)]
            await ctx.send(f'Group {i+1}: {group} (size {len(group)})')
    
    @scmd.cog_subcommand(base='bt', name='queueevent')
    async def btQueueEvent(self, ctx, networth, timezone):
        if timezone == "other":
            await ctx.send("Please talk to daKiem to enter you in this event.", hidden=True)
            return
        c = self.bot.get_channel(889169342997069825)
        messages = await c.history(limit=4).flatten()
        x = json.loads(messages[0].content)
        x[str(ctx.author.id)] = {"timezone": timezone, "networth": networth}
        await messages[0].edit(content=json.dumps(x))
        await ctx.send("You have been queued!")

def setup(bot):
    bot.add_cog(bTesting(bot))
