# savorybot
Discord bot made for the red gladiators server

# Setup (note these docs are made for linux)
### Install pip dependencies
`python3 -m pip install -r requirements.txt`
### Run
`python3 main.py`

# Contents
- ### [Cogs and cog functions](#cogs-and-cog-functions-1)
  - #### [`cogs.applications`](#cogsapplications-1)
  - #### [`cogs.btesting`](#cogsbtesting-1)
  - #### [`cogs.hystats`](#cogshystats-1)
  - #### [`cogs.listeners`](#cogslisteners-1)
  - #### [`cogs.misc`](#cogsmisc-1)
  - #### [`cogs.owner`](#cogsowner-1)
  - #### [`cogs.polls`](#cogspolls-1)
  - #### `cogs.trusted`
  - #### `cogs.checks`
  - #### `cogs.util`

# Cogs and cog functions
Arguments listed in `<>` are required, while arguments listed in `[]` are not.
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
#### Cog init: `self.bot = bot`
##### Extra imports: `json`, `requests`, `cogs.hystats.hyutil`
### Handles all application related commands:
- `/apply`
- #app-handling Accept/Deny buttons
- `=app` command group
- _internal_ `store()`
#### `=app` command group
_Permission:_ Officer+<br>
`=app force <Member ID> <IGN="placeholder">` - Forces an application to be sent to #app-handling
`=app del <appID (user's discord ID)>` - Deletes an application based on a user's ID
- _internal_ `store()` - Modified version of `cogs.util.store` to R/W from `jsonbin.io` APIs
#### How it works
This system uses [jsonbin.io](https://jsonbin.io) to send and recieve requests for applications.

## `cogs.btesting`
#### Cog init: `self.bot = bot`
##### Extra imports: `random`, `itertools.accumulate`, `slashrequest`, (others based on testing session)
### Handles beta testing:
- `/bt` group
- `=bt` command group
#### `/bt` group
_Permission:_ Owner and BT role (selected by `=bt enable`)
- `/info` - Shows brief description of what BT is
- Other commands will vary based on the application of the testing session.
#### `=bt` command group
_Permission:_ Owner only
`=bt enable <roleID (role with BT permissions)>` - Enables beta testing
`=bt disable` - Disables beta testing
#### How it works
Beta testing for discord members to test 

## `cogs.hystats`
#### Cog init: `self.bot = bot`
##### Extra imports: `requests`
### Handles:
- `hyutil` class
- `/hy` group
#### `hyutil` class
Note: This class is imported by other cogs
- _internal_ `handlerequest(status_code, err=True)` - Returns a string based on HTTP request and switches between err and success (not implemented yet)
- _internal_ `testAPIKey(key)` - Checks the status code of the JSON payload and return True/False with err cause
- _internal_ `getOnline(name)` - Returns online status, with current gamemode or last logout
- _internal_ `sbmode(g)` - Currently unused, returns `g`
- _internal_ `toUUID(name)` - Calls mojang API to return a UUID with a player's IGN
- _internal_ `toName(uuid)` - Calls mojang API to return a name with a player's UUID
#### `/hy` group
_Permission:_ Guild Member+<br>
`/hy profiles <IGN - Minecraft in-game name>` - Displays all skyblock profiles with data for a user
**Other commands disabled temporarily:**
`/hy status` - Displays if a user is online, and for how long or time since last log on
#### How it works
Grabs data from the hypixel API and formats the data in embeds

## `cogs.listeners`
#### Cog init: `self.bot = bot`
##### Extra imports: None
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
#### Cog init:
```python
  self.bot = bot
  self.annoy = 0
```
##### Extra imports: `cogs.hystats.hyutil`
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

## `cogs.owner`
#### Cog init: `self.bot = bot`
##### Extra imports: `sys`, `requests`, `io`, `aioconsole.aexec`
### Handles owner/admin-only commands:
- `=eval`
- `=n`
- `=d`
- `=kickuser`
- `=purge`
- `=genbutton`/`=clown`
- `=rrsend`/`=rrdel`
- `=role` group
- `=blacklist` group
#### `=role` group
- `=role a <roleid> [member: discord.Member=None]` - Gives a role to an optional member (otherwise user who invoked command)
- `=role d <roleid> [member: discord.Member=None]` - Removes a role from an optional member
#### `=blacklist` group
_Aliases:_ `bl`
- `=blacklist set/['s', 'a', 'add'] <member> <command> [duration=1h]` - Blacklists a user from using a command
- `=blacklist rem/['d', 'r', 'del'] <member> <command>` - Removes a user from the blacklist for a command
Uncategorized:
- `=eval [-s] <code>` - Runs python code async \[-s is for silent]
- `=n * [nickname=None]` - Rename the bot
- `=d <meID>` - Deletes a message with the message ID
- `=kickuser <member: discord.Member> <reason>` - Kicks a member
- `=purge <message (amount of messages to purge)>` - Purges a certain amount of messages from a channel
- `=genbutton [label="Click me!"] [id=None] [message="friendly button"]` - Creates a new button with optional args
- `=clown` - Creates a new button which de-verifies anyone who clicks it
- `=rrsend <roleid> * [embmsg]` - Sends a new reaction role embed
- `=rrdel <messageid>` - Deletes a reaction role
#### How it works
Simple owner and admin commands with the `checks.owner_staff` check or the `@commands.is_owner` decorator

## `cogs.polls`
#### Cog init: `self.bot = bot`
##### Extra imports: `json`
### Handles all poll-related creation/deletion commands:
- `/poll` group
#### `/poll` group
- `/poll create <msg> [polltype=None] [listoptions=None] [hideanswers=False]` - Creates a poll
- `/poll conclude <pollid>` - Concludes a poll
#### How it works
Uses a data host guild to retrieve and store data. The actual events are listened by `listeners.on_button_click` or `listeners.on_select_option`, which updates the guild as well as the message.
