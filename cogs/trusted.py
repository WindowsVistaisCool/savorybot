import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from datetime import datetime
from cogs.util import store, bugReport
from cogs import checks

class Trusted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['e'])
    @commands.check(checks.owner_trusted)
    async def expose(self, ctx):
        if await checks.blacklist(ctx, 'expose'): return
        try:
            d = store('expose.json', None, True)
            x = d[str(ctx.channel.id)]
        except:
            await ctx.send("Nothing found to expose!")
            return
        embed = discord.Embed(title='EDIT SNIPE' if x['type'] == 'edit' else discord.Embed.Empty, color=discord.Color.red(), timestamp=datetime.utcnow(), description=x['content'])
        try:
            embed.set_author(name=x['author'], icon_url=x['author_icon'])
        except: pass
        embed.set_footer(text='Exposed at')
        if x['files'] != []:
            embed.set_image(url=x['files'][0])
        if x['ghostping']:
            gField = ""
            for ghostMention in x['ghostping']:
                gField = gField + f'<@!{ghostMention}> '
            embed.add_field(name="**GHOST PING/REPLY!** Users affected:",value=gField)
        await ctx.send(embed=embed)
        d.pop(str(ctx.channel.id))
        store('expose.json', d)

    # add ping last message from member
    @commands.command()
    @commands.check(checks.owner_trusted)
    async def pin(self, ctx, message=None):
        try:
            e = store('blacklist.json', str(ctx.author.id), True)
            print(e)
            for command in e['blacklistedCommands']:
                if command == 'pin':
                    await ctx.send("Sorry! You have been blacklisted from using this command.")
                    return
        except Exception as e: pass
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
    @commands.check(checks.owner_trusted)
    async def unpin(self, ctx, message=None):
        try:
            e = store('blacklist.json', str(ctx.author.id), True)
            print(e)
            for command in e['blacklistedCommands']:
                if command == 'pin':
                    await ctx.send("Sorry! You have been blacklisted from using this command.")
                    return
        except Exception as e: pass
        await ctx.message.delete()
        if message != None:
            try:
                e = await ctx.channel.fetch_message(int(message))
                await e.unpin()
                await ctx.send("Unpinned message!")
                return
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

def setup(bot):
    bot.add_cog(Trusted(bot))
