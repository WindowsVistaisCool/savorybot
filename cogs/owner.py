import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from datetime import datetime
from asyncio import sleep

# Eval command imports
import sys
import requests
import io
import cogs
from aioconsole import aexec

store = cogs.util.store
checks = cogs.checks

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        out, err = io.StringIO(), io.StringIO()
        silence = False
        if code.startswith('-s'):
            silence = True
            code = code[3:]
            await ctx.message.delete()
        code = code[:-3]
        code = code[5:]
        args = {
            "discord": discord,
            "Button": Button,
            "Select": Select,
            "SelectOption": SelectOption,
            "ctx": ctx,
            "self": self,
            "cogs": cogs,
            "sleep": sleep,
            "requests": requests,
            "client": self.bot,
            "datetime": datetime
        }
        sys.stdout = out
        sys.stderr = err
        await aexec(code, args) # main exec process
        results = out.getvalue()
        errors = err.getvalue()
        if not silence:
            await ctx.send(f"```py\n{results}```{('```Errors: ' + errors + '```') if errors != '' else ''}")

    @commands.group()
    @commands.is_owner()
    async def role(self, ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand == None: return

    @role.command(name='a')
    async def role_a(self, ctx, roleid, member:discord.Member=None):
        try:
            if member == None:
                await ctx.author.add_roles(ctx.guild.get_role(int(roleid)))
            else:
                await member.add_roles(ctx.guild.get_role(int(roleid)))
        except: return

    @role.command(name='d')
    async def role_d(self, ctx, roleid, member:discord.Member=None):
        try:
            if member == None:
                await ctx.author.remove_roles(ctx.guild.get_role(int(roleid)))
            else:
                await member.remove_roles(ctx.guild.get_role(int(roleid)))
        except: return

    @commands.group(aliases=['bl'])
    # Only using is_owner because duration is not functional at the moment
    # @commands.check(checks.owner_staff)
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand == None: return
    
    @blacklist.command(name='set', aliases=['s', 'a', 'add'])
    async def bl_set(self, ctx, member, command, dur='1h'):
        await ctx.message.delete()
        seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            duration = int(dur[:-1]) * seconds_per_unit[dur[-1]]
        except:
            await ctx.send("invalid duration proivded")
            return
        e = store('blacklist.json', None, True)
        for i in e:
            if member == i:
                e[member]["blacklistedCommands"].append(command)
                break
        else:
            e[member] = {"duration": duration, "blacklistedCommands": [command]}
        store('blacklist.json', e)
        
    @blacklist.command(name='rem', aliases=['d', 'r', 'del', 'remove', 'delete'])
    async def bl_rem(self, ctx, member, command):
        await ctx.message.delete()
        e = store('blacklist.json', None, True)
        mem = None
        for blacklisted in e:
            if blacklisted == member:
                mem = e[blacklisted]
                break
        e[member] = mem['blacklistedCommands'].remove(command)
        if e[member] == None:
            e.pop(member)
        store('blacklist.json', e)

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
    async def kickuser(self, ctx, member: discord.Member, reason):
        await ctx.message.delete()
        await member.kick(reason=reason)

    @commands.command()
    @commands.check(checks.owner_staff)
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

def setup(bot):
    bot.add_cog(Owner(bot))
