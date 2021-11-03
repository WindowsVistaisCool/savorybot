# savorybot
Discord bot made for the red gladiators server

# Setup (note these docs are made for linux)
### Install pip dependencies
`python3 -m pip install -r requirements.txt`
### Run
`python3 main.py`

# Cogs and cog functions

## All cogs
#### Functional cogs (commands)
```
cogs.applications
cogs.btesting
cogs.hystats
cogs.listeners
cogs.misc
cogs.owner
cogs.polls
cogs.trusted
```
#### Utility cogs (not really cogs, just functions unrelated to commands)
```
cogs.checks
cogs.util
```

## Cog descriptions/commands
### `cogs.applications`
Handles all application related commands:
- `/apply`
- #app-handling Accept/Deny buttons
- =app command group
#### =app command group
=app force - Forces an application to be sent to #app-handling
=app del - Deletes an application based on a user's ID
#### How it works
This system uses [jsonbin.io](https://jsonbin.io) to send and recieve requests for applications. (more info coming soon)
