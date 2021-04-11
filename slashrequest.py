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
		x[key] = val
		with open(file, 'w') as v:
			json.dump(x, v, indent=4)

# internal
def checkURL():
  x = store('config,json', 'slashID', True)
  returns = []
  if x['appID'] is not None:
    returns.append(x['appID'])
  
  if x['guildID'] is not None:
    returns.append(x['appID'])
   
  return returns

def setURL(appID, guildID):
  try:
    x = store('config.json', None, True)
    x['slashID']['appID'] = appID
    x['slashID']['guildID'] = guildID
    with open('config.json', 'r') as v:
      json.dump(x, v, indent=4)
    return True
  except:
    return False

def get(header):
  k = checkURL()
  url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands"
  head = f"Bot {header}"
  headers = {
    "Authorization": head
  }
  f = requests.get(url, headers=headers)
  return f
  
def post(header, jsonData):
  k = checkURL()
  url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands"
  head = f"Bot {header}"
  headers = {
    "Authorization": head
  }
  e = requests.post(url, headers=headers, json=jsonData)
  return e

def delete(header, slashAppID):
  k = checkURL()
  url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands"
  head = f"Bot {header}"
  headers = {
    "Authorization": head
  }
  r = requests.delete(url + f"/{slashAppID}", headers=headers)
  return r
