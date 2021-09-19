import discord
import json
from datetime import datetime
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from cogs.util import store
from asyncio import sleep

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @scmd.cog_subcommand(base='poll', name='create')
    async def create(self, ctx, msg, polltype=None, listoptions=None, hideanswers=False):
        cat = self.bot.get_channel(886767483342696490)
        hide = hideanswers
        if polltype == 'list' and listoptions is None:
            await ctx.send("You must fill out the `listoptions` parameters when using the `list` type!",hidden=True)
            return
        if polltype == 'default' or polltype == None:
            await ctx.send("Created poll", hidden=True)
            e = discord.Embed(title=msg, color=discord.Color.blurple(), timestamp=datetime.utcnow())
            e.set_footer(text="Poll started")
            msg = await ctx.channel.send(embed=e)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        elif polltype == 'buttons':
            await ctx.send("Created poll", hidden=True)
            e = discord.Embed(title=msg, color=discord.Color.blurple(), timestamp=datetime.utcnow())
            e.add_field(name="Yes", value="0")
            e.add_field(name="No", value="0")
            m = await ctx.channel.send("Building...")
            e.set_footer(text=f"ID: {m.id}")
            c = await cat.create_text_channel(f"{m.id}", reason="Auto-created by a poll command (button)")
            data = json.dumps({"title": msg, "type": "button","yes": 0, "no": 0})
            await c.send(data)
            await sleep(1.5)
            await c.send("No user data")
            await m.edit(content="", embed=e, components=[[Button(label="Vote Yes",style=3,custom_id=f"{m.id}POLLYES"), Button(label="Vote No",style=4,custom_id=f"{m.id}POLLNO")]])
        elif polltype == 'list':
            await ctx.send("Created poll", hidden=True)
            opts = listoptions.split(';')
            for option in opts:
                if len(option) >= 25:
                    await ctx.send("One or more of your options has greater than 25 characters!", hidden=True)
                    return
            if len(opts) >= 15:
                await ctx.send("You cannot have this many options!", hidden=True)
                return
            m = await ctx.channel.send("Building...")
            c = await cat.create_text_channel(f"{m.id}", reason="Auto-created by a poll command (select)")
            selectopts = []
            fields = {}
            fieldpos = {}
            e = discord.Embed(title=msg,color=discord.Color.blurple(), timestamp=datetime.utcnow())
            e.set_footer(text=f"ID: {m.id}")
            count = 0
            for opt in opts:
                fields[opt] = 0
                fieldpos[opt] = count
                if hide:
                    selectopts.append(SelectOption(label=opt, value=f"SelectPoll-{m.id}-T-{count}-{opt}"))
                else:
                    e.add_field(name=opt, value="0", inline=False)
                    selectopts.append(SelectOption(label=opt, value=f"SelectPoll-{m.id}-F-{count}-{opt}"))
                count += 1
            data = json.dumps({"title": msg,"type": "list", "fields": fields, "fieldpos": fieldpos})
            await c.send(data)
            await sleep(1.5)
            await c.send("No user data")
            await m.edit(content="", embed=e, components=[Select(placeholder="Choose a response...",options=selectopts)])

    @scmd.cog_subcommand(base='poll', name='conclude')
    async def conclude(self, ctx, pollid):
        cat = self.bot.get_channel(886767483342696490)
        c = None
        for channel in cat.channels:
            if pollid == channel.name:
                c = channel
                break
        if c == None:
            await ctx.send("Could not find that poll!",hidden=True)
            return
        await ctx.send("Concluded poll", hidden=True)
        dat = await c.history(limit=4).flatten()
        x = json.loads(dat[1].content)
        sers = []
        if dat[0].content != "No user data":
            sers = dat[0].content.split('-')
        msg = await ctx.channel.fetch_message(int(pollid))
        e = msg.embeds[0]
        e.clear_fields()
        e.add_field(name="POLL ENDED", value="Thank you, participants!", inline=False)
        res = ""
        if x['type'] == 'button':
            res = res + f"**Yes**: {x['yes']}\n**No**: {x['no']}"
        else:
            for opt in x['fields']:
                res = res + f"**{opt}**: {x['fields'][opt]}\n"
        e.add_field(name="Results", value=res, inline=False)
        usrs = ""
        for user in sers:
            usrs = usrs + f"<@!{user}>\n"
        if usrs == "": usrs = "(None)"
        e.add_field(name="Participants",value=usrs, inline=False)
        await msg.edit(embed=e, components=[])
        await c.delete(reason="Poll concluded")

def setup(bot):
    bot.add_cog(Polls(bot))
