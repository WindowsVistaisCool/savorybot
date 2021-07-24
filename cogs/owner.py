import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from datetime import datetime
from cogs.util import store
from asyncio import sleep

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.is_owner()
    async def n(self, ctx, *, nickname=None):
        d = await ctx.guild.fetch_member(self.bot.user.id)
        await d.edit(nick=nickname)
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def d(self, ctx, meID):
        await ctx.message.delete()
        e = await ctx.channel.fetch_message(int(meID))
        await e.delete()


    @commands.command()
    @commands.is_owner()
    async def purge(self, ctx, message):
        await ctx.message.delete()
        await ctx.channel.purge(limit=int(message))

    @commands.command()
    @commands.is_owner()
    async def clown(self, ctx):
        await ctx.message.delete()
        await ctx.send("lmfao click the button below to get clowned on", components=[Button(emoji=self.bot.get_emoji(815818057359687691), id="deverify")])

    @commands.command()
    @commands.is_owner()
    async def genbutton(self, ctx, label="Click me", id=None, message="friendly button"):
        await ctx.message.delete()
        await ctx.send(message, components=[Button(label=label, id=id)])

    # Reaction roles
    @commands.command()
    @commands.is_owner()
    async def rrsend(self, ctx, roleid, *, embmsg):
        await ctx.message.delete()
        e = discord.Embed(title=embmsg, color=discord.Color.blurple())
        msg = await ctx.send(embed=e)
        x = store('rroles.json', None, True)
        x['rroles'][str(msg.id)] = embmsg
        x['rrolesrole'][str(msg.id)] = roleid
        store('rroles.json', x)
        await msg.add_reaction("✅")
        await ctx.send("Reaction role added", delete_after=1)

    @commands.command()
    @commands.is_owner()
    async def rrdel(self, ctx, messageid):
        await ctx.message.delete()
        x = store('rroles.json', None, True)
        x["rroles"].pop(messageid)
        x["rrolesrole"].pop(messageid)
        store('rroles.json', x)
        await ctx.send("Reaction role removed", delete_after=1)

def load(bot):
    bot.add_cog(Owner(bot))
