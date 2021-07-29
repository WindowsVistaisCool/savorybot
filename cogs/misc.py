import requests
import string
import random
import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from datetime import datetime
from cogs.util import store
from asyncio import sleep

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @scmd.cog_slash(name='about')
    async def about(self, ctx):
        e = discord.Embed(title="Red Gladiators Guild Info", color=discord.Color.blurple())
        e.add_field(name="Features",value="**-** Active Skyblock Guild\n\n**-** Dungeons\n\n**-** Skyblock advice\n\n**-** Trusted members\n\n**-** Good community")
        await ctx.send(embed=e, hidden=True)

    @scmd.cog_slash(name='bugreport')
    async def bugreport(self, ctx):
        await ctx.send("Coming soon", hidden=True)
    
    # add accept/deny stuff
    @scmd.cog_slash(name='giveaway')
    async def giveaway(self, ctx, winners, time, prize):
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

def load(bot):
    bot.add_cog(Misc(bot))
