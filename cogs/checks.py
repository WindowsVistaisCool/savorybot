import discord

async def owner_staff(ctx):
    if ctx.author.id == 392502213341216769: return True
    if ctx.guild.get_role(789593786287915010) in ctx.author.roles: return True
    return False

async def owner_trusted(ctx):
    if ctx.author.id == 392502213341216769: return True
    if ctx.guild.get_role(789592055600250910) in ctx.author.roles: return True
    return False
