import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from cogs.util import store

class Trusted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # add ping last message from member
    @commands.command()
    @commands.has_role("Trusted")
    async def pin(self, ctx, message=None):
        await ctx.message.delete()
        try:
            if message != None:
                e = await ctx.channel.fetch_message(int(message)) 
            else:
                e = None
                async for msg in ctx.channel.history(limit=1):
                    e = msg
            await e.pin()
        except:
            await ctx.send("failure (invalid message id?/already pinned?)", delete_after=3)

    @commands.command()
    @commands.has_role("Trusted")
    async def unpin(self, ctx, message=None):
        await ctx.message.delete()
        if message != None:
            try:
                e = await ctx.channel.fetch_message(int(message))
                await e.unpin()
            except:
                await ctx.send("Could not find pin!")
                return
        try:
            m = None
            async for ms in ctx.channel.history(limit=200):
                if ms.pinned:
                    m = ms
                    break
            await m.unpin()
            await ctx.send("Unpinned message!")
        except:
            await ctx.send("Error retrieving pin (pins cannot be unpinned via this command if it is more than 200 messages ago")
            
def load(bot):
    bot.add_cog(Trusted(bot))
