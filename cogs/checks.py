import discord
from cogs.util import store

# Ver 1
async def owner_staff(ctx):
    if ctx.author.id == 392502213341216769 or ctx.author.id == 406629388059410434: return True
    if ctx.guild.get_role(789593786287915010) in ctx.author.roles: return True
    return False

async def owner_trusted(ctx):
    if ctx.author.id == 392502213341216769 or ctx.author.id == 406629388059410434: return True
    if ctx.guild.get_role(789592055600250910) in ctx.author.roles: return True
    return False

async def blacklist(ctx, com):
    try:
        e = store('blacklist.json', str(ctx.author.id), True)
        for command in e['blacklistedCommands']:
            if command == com:
                await ctx.send("Sorry! You have been blacklisted from using this command.")
                return True
    except Exception as ex: pass
    return False

# Ver 2 Code (unimplemented/unsupported as of now)
# Taken directly from https://github.com/applediscord/dpy-frame/blob/master/cogs/checks.py
# class checkFuncs():
#     def handleFlags(ctx, flags):
#         validFlags = [
#             "alwaysTrue",
#             "alwaysFalse"
#         ] # More may be added
#         debug = True if flags[0] == "debug" else False
#         firstLoopIteration = True
#         for flag in flags:
#             if flag not in validFlags and flag != "debug":
#                 return f"'{flag}'"
#             if debug and firstLoopIteration:
#                 firstLoopIteration = False
#                 continue
#             elif debug:
#                 if flag == "alwaysTrue": return True
#                 elif flag == "alwaysFalse": return False
#         return False

#     def handleRoles(ctx, roles):
#         for roleID in roles:
#             role = ctx.guild.get_role(roleID)
#             if role in ctx.author.roles: return True
#         return False

#     def handleUsers(ctx, users):
#         if ctx.author.id in users:
#             return True
#         return False
    
#     @classmethod
#     def parseCheck(cls, ctx, data):
#         f, r, u = False, False, False
#         if data['flags'] != []:
#             f = cls.handleFlags(ctx, data['flags'])
#             if type(f) != bool:
#                 print(f"Invalid flag defined: {f}")
#                 return False
#         if data['roles'] != []:
#             r = cls.handleRoles(ctx, data['roles'])
#         if data['users'] != []:
#             u = cls.handleUsers(ctx, data['users'])
#         if r or u or f: return True
#         return False