import discord
import asyncio
from slashrequest import store

client = discord.Client()

async def commandcheck(message, ctx, lms):
    voicecom = ['/join', '/leave', '/annoy', '/move', '/mute', '/unmute', '/deafen', '/undeafen']
    if message.startswith('/close'):
            print("Closing...")
            return "Close"
    elif message.startswith('/channel'):
        new = message.replace('/channel ', '')
        if new != ' ':
            try:
                d = discord.utils.get(ctx.guild.text_channels, name=new)
            except:
                print("Could not find channel")
                return "Fail"
            print(f"Switched to channel {new}")
            return f"Sw {d.id}"
        print("GUILD TEXT CHANNELS:") 
        for channel in ctx.guild.text_channels:
            print(f"NAME: {channel.name} ID: {channel.id}")
        chn = input("Channel ID: ")
        if chn is None:
            chn = ctx.guild.get_channel(788886124159828012)
        else:
            try:
                if type(chn) is str:
                    d = discord.utils.get(ctx.guild.text_channels, name=chn)
                    cn = d.id
            except:
                print("Error")
                return "Cont"
        print(f"Switched to channel {chn}")
        return f"Sw {cn}"
    elif message.startswith('/lms'):
        return f"LMS {ctx.last_message_id}"
    # elif message.startswith('/callback'):
        # await comcallback(ctx)
    elif message.startswith('/del'):
        def c(m):
            return client.user == m.author
        await ctx.purge(limit=1, check=c)
        print("Deleted last sent message")
        return "Done"
    elif message.startswith('/edit'):
        new = message.replace('/edit ', '')
        await lms.edit(content=new)
        return "Done"
    elif message.startswith('/r'):
        new = message.replace('/r ', '')
        if new == ' ':
            f = ctx.guild.emojis
            for emoji in f:
                print(emoji.name)
            return "Done"
        try:
            e = discord.utils.get(ctx.guild.emojis, name=new)
            await lms.add_reaction(e)
        except:
            print("Failed")
        return "Done"
    elif message.startswith('/embed'):
        await embed(ctx)
        return "Done"
    elif message.startswith('/play'):
        new = message.replace('/play ', '')
        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(new))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            return "Done"
        except:
            return "Fail"
    elif message.startswith('/purge'):
        new = message.replace('/purge ', '')
        def check(m):
            return client.user == m.author
        await ctx.purge(limit=int(new), check=check)
        print(f"purged {new} messages")
        return "Done"

    elif message.startswith('/getid'):
        new = message.replace('/getid ', '')
        try:
            member = discord.utils.get(ctx.guild.members, name=new)
            print(member.id)
            return "Done"
        except:
            print("Failure")
            return "Fail"
    
    # thanks to jackson for the annoy code
    elif message.startswith('/nick'):
        # add members
        new = message.replace('/nick ', '')
        await ctx.guild.me.edit(nick=new)
        return "Done"
    elif message.startswith('/spam'):
        # merge /spam and times
        m = input("Times: ")
        message = input("Spam Message: ")
        for x in range(int(m)):
            await ctx.send(message)
            await asyncio.sleep(0.1)
        return "Done"
    # voice commands
    for comm in voicecom:
        if message.startswith(comm):
            c = await voice(ctx, message)
            if c == "Cont":
                return "Fail"
            else:
                return "Done"

async def embed(ctx):
    print("Embed setup starting...")
    # need to merge embed startup command with title and rearrange this code
    col = input("Color: ")
    print("OK")
    ts = False
    atxt = None
    ft = None
    def clr(color):
        if color == 'green':
            return discord.Color.green()
        elif color == 'red':
            return discord.Color.red()
        else:
            return discord.Color.blurple()
    etitle = input("Embed title: ")
    def emty(var):
        if var is None:
            return discord.Embed.Empty
        else:
            return var
    def time(s):
        if s is True:
            return datetime.datetime.utcnow()
        else:
            return discord.Embed.Empty
    action = input("Footer: ")
    if action == 't':
        ft = input("Footer text: ")
        ts = input("Timestamp: ")
        if ts is 't':
            ts = True
    action = input("Author: ")
    if action == 't':
        lnk = input("Link: ")
        if lnk is '':
            lnk = None
        atxt = input("Author title text: ")
    e = discord.Embed(title=etitle, color=clr(col), timestamp=time(ts))
    if ft is not None:
        e.set_footer(text=ft)
    if atxt is not None:
        e.set_author(name=atxt, url=lnk)
    await ctx.send(embed=e)

@client.event
async def on_ready():
    c = client.get_channel(788886124159828012)
    global lms
    lms = None
    while True:
        message = input("Message: ")
        if message == '':
            await c.trigger_typing()
            continue
        command = await commandcheck(message, c, lms)
        if command == "Close":
            try:
                await client.close()
            except:
                pass
            break
        elif command == "Done":
            pass # maybe add something else
        elif command != None:
            if "Sw" in command:
                command = command.replace("Sw ", '')
                c = client.get_channel(int(command))
                continue
            elif "LMS" in command:
                new = command.replace("LMS ", '')
                print(new)
                try:
                    lms = await c.fetch_message(int(new))
                except:
                    print("Fail")
        elif command == "Fail":
            continue
        else:
            if "\\" in message:
                message = message.replace('\\', '')
            try:
                lms = await c.send(message)
            except:
                print("Error in setting LMS")

client.run(store('config.json', 'token', True))
