import discord
import slashrequest
from discord.ext import commands
from discord_slash import cog_ext as scmd
from discord_components import Button, Select, SelectOption

class bTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # enable/disable
    @commands.group()
    @commands.is_owner()
    async def bt(ctx):
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid sub")

    @bt.command(name='enable')
    async def bt_enable(ctx, roleid):
        slashrequest.sc.post(store('config.json', 'bt', True))
        e = slashrequest.sc.get('bt')['id']
        slashrequest.sc.perm(e, [roleid], [True])
        await ctx.send("Added bot testing commands")

    @bt.command(name='disable')
    async def bt_disable(ctx):
        slashrequest.sc.rem('bt')
        await ctx.send("Removed bot testing commands")

    @scmd.cog_subcommand(base='bt', name='info')
    async def _bt_info(ctx):
        await ctx.send("You're here because you signed up to help me improve this bot! As of this first testing session, there are a few commands, and you will be pinged when a new one arrives. **DO NOT USE THESE COMMANDS OUTSIDE OF THE #bot-testing CHANNEL. YOU WILL RECIEVE A WARNING** If you recieve a message saying \"This interaction failed\", **please let me know as soon as possible**. Thank you for signing up and helping me iron out any bugs!", hidden=True)
    
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
            await m.edit(content=f"Expired menu - {ctx.author.name} selected {interaction.component[0].label}",components=[])
            await interaction.respond(content="You selected an item!")

def load(bot):
    bot.add_cog(bTesting(bot))
