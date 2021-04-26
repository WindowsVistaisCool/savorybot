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


head = store('config.json', 'slashConfig', True)['auth']

# add tips later
def checktips():
	return store('config.json', 'slashConfig', True)['tips']

# internal
def checkURL():
  x = store('config.json', 'slashConfig', True)
  returns = []
  if x['appID'] is not None:
    returns.append(x['appID'])

  if x['guildID'] is not None:
    returns.append(x['guildID'])

  return returns

class sc:
	# Basic functions
	def get(all=False):
	  k = checkURL()
	  url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands"
	  f = requests.get(url, headers=head)
	  if all is False:
	      g = []
	      for com in f.json():
	          name = com['name']
	          id = com['id']
	          g.append({"name":name, "id":id})
	      return g
	  return f.json()

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

 	# Permissions
	def perm(commandID, roleIDTuple=None, *, includeSelf=True, permAllow=True, staff=False, user=None):
		k = checkURL()
		url = f"https://discord.com/api/v8/applications/{k[0]}/guilds/{k[1]}/commands/{commandID}/permissions"
		perms = []
		if includeSelf is True or (roleIDTuple is None and staff is False) and user is None:
			selfID = store('config.json', 'slashConfig', True)['selfID']
			selfData = {
				"id": selfID,
				"type": 2,
				"permission": True
			}
			perms.append(selfData)
		if roleIDTuple is not None:
			try:
				if staff is True:
					d = store('config.json', 'slashConfig', True)['staffID']
					roleIDTuple.append(d)
				for roleID in roleIDTuple:
					roleData = {
						"id": roleID,
						"type": 1,
						"permission": permAllow
					}
					perms.append(roleData)
			except:
				return
		if user is not None:
			try:
				uid = str(user)
			except:
				return
			userData = {
				"id": uid,
				"type": 2,
				"permission": permAllow
			}
			perms.append(userData)
		jData = {
			"permissions": perms
		}
		r = requests.put(url, headers=head, json=jData)
		return r
