import requests
import json
import discord
from discord.ext import commands
from discord_slash import SlashCommand, utils

def store(file, key=None, read=False, val=None):
	with open(file, 'r') as v:
		x = json.load(v)
	if read is not False:
		if key is None:
			return x
		else:
			return x[key]
	else:
		if val is None:
			with open(file, 'w') as v:
				json.dump(key, v, indent=4)
			return
		x[key] = val
		with open(file, 'w') as v:
			json.dump(x, v, indent=4)

			
head = {"Authorization": f"Bot {store('config.json', 'token', True)}"}

# internal
def checkURL():
  x = store('config.json', 'slashID', True)
  returns = []
  if x['appID'] is not None:
    returns.append(x['appID'])
  
  if x['guildID'] is not None:
    returns.append(x['guildID'])
   
  return returns

def get():
  k = checkURL()
  url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands"
  f = requests.get(url, headers=head)
  return f.text
  
def post(jsonData):
  k = checkURL()
  url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands"
  e = requests.post(url, headers=head, json=jsonData)
  return e

def rem(slashAppID):
  k = checkURL()
  url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands"
  r = requests.delete(url + f"/{slashAppID}", headers=head)
  return r
