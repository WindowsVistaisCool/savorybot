import discord
from datetime import datetime
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption
from cogs.util import store

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @scmd.cog_subcommand(base='poll', name='create')
    async def create(self, ctx, msg, polltype=None, listoptions=None, hideanswers=False):
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
            store('polls.json', f"{m.id}", val={"title": msg, "type": "button","yes": 0, "no": 0, "users": []})
            await m.edit(content="", embed=e, components=[[Button(label="Vote Yes",style=3,id=f"{m.id}POLLYES"), Button(label="Vote No",style=4,id=f"{m.id}POLLNO")]])
        elif polltype == 'list':
            await ctx.send("Created poll", hidden=True)
            opts = listoptions.split(';')
            if len(opts) >= 15:
                await ctx.send("You cannot have this many options!", hidden=True)
                return
            m = await ctx.channel.send("Building...")
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
                    selectopts.append(SelectOption(label=opt, value=f"SelectPoll-{m.id}-T-{count}"))
                else:
                    e.add_field(name=opt, value="0", inline=False)
                    selectopts.append(SelectOption(label=opt, value=f"SelectPoll-{m.id}-F-{count}"))
                count += 1
            store('polls.json', f"{m.id}", val={"title": msg,"type": "list", "fields": fields, "fieldpos": fieldpos, "users": []})
            await m.edit(content="", embed=e, components=[Select(placeholder="Choose a response...",options=selectopts)])

    @scmd.cog_subcommand(base='poll', name='conclude')
    async def conclude(self, ctx, pollid):
        x = store('polls.json', None, True)
        if pollid not in x:
            await ctx.send("Could not find that poll!",hidden=True)
            return
        await ctx.send("Concluded poll", hidden=True)
        msg = await ctx.channel.fetch_message(int(pollid))
        e = msg.embeds[0]
        e.clear_fields()
        e.add_field(name="POLL ENDED", value="Thank you, participants!", inline=False)
        res = ""
        if x[pollid]['type'] == 'button':
            res = res + f"**Yes**: {x[pollid]['yes']}\n**No**: {x[pollid]['no']}"
        else:
            for opt in x[pollid]['fields']:
                res = res + f"**{opt}**: {x[pollid]['fields'][opt]}\n"
        e.add_field(name="Results", value=res, inline=False)
        usrs = ""
        for user in x[pollid]['users']:
            usrs = usrs + f"<@!{user}>\n"
        if usrs == "": usrs = "(None)"
        e.add_field(name="Participants",value=usrs, inline=False)
        x.pop(pollid)
        store('polls.json', x)
        await msg.edit(embed=e, components=[])

def load(bot):
    bot.add_cog(Polls(bot))
