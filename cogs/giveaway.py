import discord
from discord.ext import commands
from discord_slash import cog_ext as scmd
from cogs import checks

class Giveaway(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

def setup(bot):
  bot.add_cog(Giveaway(bot)
