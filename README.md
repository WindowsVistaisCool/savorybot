# savorybot
Discord bot made for the red gladiators server

# Setup (note these docs are made for linux)
### Install pip dependencies
`python3 -m pip install -r requirements.txt`
### Run
`python3 main.py`

# Cogs and cog functions

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

## `cogs.applications`
### Handles all application related commands:
- `/apply`
- #app-handling Accept/Deny buttons
- `=app` command group
#### `=app` command group
`=app force` - Forces an application to be sent to #app-handling
`=app del` - Deletes an application based on a user's ID
#### How it works
This system uses [jsonbin.io](https://jsonbin.io) to send and recieve requests for applications.

## `cogs.btesting`
### Handles beta testing:
- `/bt` group
- `=bt` command group
#### `/bt` group
Various mainly on the application of the testing session.
#### `=bt` command group
=bt enable - Enables beta testing
=bt disable - Disables beta testing
#### How it works
Beta testing for discord members to test 

## `cogs.hystats`
### Handles:
- `/hy` group
#### `/hy` group
`/hy profiles` - Displays all skyblock profiles with data for a user
Other commands disabled temporarily
#### How it works
Grabs data from the hypixel API and formats the data in embeds

## `cogs.listeners`
### Handles all listeners and event actions:
- `on_raw_reaction_add`/`on_raw_reaction_remove`
- `on_button_click`
- `on_select_option`
- `on_message`
- `on_message_delete`
- `on_message_edit`
- `on_command_error`
#### Reaction events
Used for the starboard feature (#funny-quotes channel)
#### Component events
Used for handling applications, deleting messages, and polls
#### On message event
Used for MEE6 level messages and verification embed
#### Message delete/edit events
Used for `=expose` command
#### Command error event
Used for reporting a NotFound, CheckFailure, or other unknown error
#### How it works
Uses the `discord.ext.commands.Cog.listener()` decorator to register listeners in the cog. Called by the bot gateway for each event.

## `cogs.misc`
### Handles miscellaneous slash commands:
- `/frag`
- `/ruff`
- `/senither`
- `/giveaway`
Unused:
- **No slash command ref in guild** `/version`
- _async_ `genuser()`
- _async_ `getitem()`
`/frag` - Allows a user to request frag access with asmb
`/ruff` - If Ruffr is being annoying, any user can run this command and it will warn him
`/senither` - Simple message with the guild senither link
`/giveaway` - Allows a non-trusted member to request to start a giveaway
#### How it works
Simple slash commands, not one complete module
