import discord
import requests
from discord.ext import commands

key = "key=811f49f0-096a-418b-87e5-25ce9ca9b8c2"
uuid = {"m": "e8350b1a-fb6b-4bb8-ab2b-c2a9e1744ac9", "t": "e6316d9a-39e8-47ca-8a19-cbd06149773b"}
hy = "https://api.hypixel.net"

class t:
  def gdata():
    return requests.get(f"{hy}/skyblock?{key}")
