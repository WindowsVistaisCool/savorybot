import discord
import asyncio
from slashrequest import store

client = discord.Client()

async def commandcheck(message, ctx, lms):
    voicecom = ['/join', '/leave', '/annoy', '/move', '/mute', '/unsup', '/unmute', '/deafen', '/undeafen']
    if message.startswith('/close'):
            print("Closing...")
            return "Close"
    elif message.startswith('/role'):
        try:
            new = message.replace('/role', '')
            if new == ' ' or new == '':
                return "Fail"
            if new.startswith(' a'):
                nee = new.replace(' a', '')
                if nee == '' or nee == ' ':
                    return "Fail"
                return f"MEMBERADD-{nee}"
            newe = new.replace(' d', '')
            if newe == ' ' or newe == '':
                return "Fail"
            return f"MEMBERDEL-{newe}"
        except Exception as e:
            print(f"{e}")
            return "Fail"
    elif message.startswith('/channel'):
        new = message.replace('/channel ', '')
        if new != '':
            try:
                d = discord.utils.get(ctx.guild.text_channels, name=new)
            except:
                print("Could not find channel")
                return "Fail"
            print(f"Switched to channel {new}")
            try:
	            return f"Sw {d.id}"
            except:
                    print("Please add a space after /channel!")
                    return "Fail"
        print("GUILD TEXT CHANNELS:")
        for channel in ctx.guild.text_channels:
            print(f"NAME: #{channel.name} ID: {channel.id}")
        chn = input("Channel Name: ")
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
    elif message.startswith('/history'):
        return "History"
    elif message.startswith('/lms'):
        new = message.replace('/lms ', '')
        print(new)
        if new == '' or new == '/lms':
            return f"LEMMS"
        return f"LMSID-{new}"
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
        try:
            for l in new:
                eee = new.replace(l, region[l])
            print(eee)
            await lms.add_reaction(eee)
        except Exception as e:
            print(f"{e}")
        try:
            await lms.add_reaction(new)
        except Exception as e:
            print(f"Failure {e}")
        return "Done"
    elif message.startswith('/ea'):
        new = message.replace('/ea ', '')
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
    elif message.startswith('/loop'):
        new = message.replace('/loop ', '')
        try:
            bird = await ctx.guild.fetch_member(406629388059410434)
            chn = bird.voice.channel
            try:
                await chn.connect()
            except:
                pass
            while True:
                voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
                if voice_client.is_playing(): continue
                audio_source = discord.FFmpegPCMAudio(new+'.mp3')
                voice_client.play(audio_source, after=None)
                # convert this to an argument in the command
                if new == 'boom' or new == 'y':
                    await asyncio.sleep(1.25)
                elif new == 'fart':
                    await asyncio.sleep(3.75)
                elif new == 'bounce':
                    await asyncio.sleep(7.5)
                else:
                    await asyncio.sleep(6)
                if voice_client.is_playing(): continue
                audio_source = discord.FFmpegPCMAudio(new+'.mp3')
                voice_client.play(audio_source, after=None)
            # never gets called but just for sake of my eyes:
            return "Done"
        except Exception as e:
            print(f"{e}")
            return "Fail"
    elif message.startswith('/p'):
        new = message.replace('/p ', '')
        try:
            bird = await ctx.guild.fetch_member(406629388059410434)
            chn = bird.voice.channel
            try:
                await chn.connect()
            except:
                pass
            guild = ctx.guild
            try:
                voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
            except:
                pass
            audio_source = discord.FFmpegPCMAudio(new+".mp3")
            if voice_client.is_playing():
                voice_client.stop()
            voice_client.play(audio_source, after=None)
            # player = chn.create_ffmpeg_player(new, after=lambda: print('done'))
            # player.start()
            # while not player.is_done():
            #     await asyncio.sleep(1)
            # player.stop()
            # await chn.disconnect()
            return "Done"
        except Exception as e:
            print(f"{e}")
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

async def voice(ctx, com):
	com = com.replace('/', '')
	if com.startswith('join'):
		com = com.replace('join', '')
		if com == '':
			bird = await ctx.guild.fetch_member(406629388059410434)
			chn = bird.voice.channel
			try:
				await chn.connect()
			except Exception as e:
				print(f"error {e}")
				return "Cont"
		else:
			try:
				voice = client.get_channel(int(com))
				await voice.connect()
			except Exception as e:
				print(f"errorr {e}")
				return "Cont"
	elif com.startswith('leave'):
		new = com.replace('leave ', '')
		if new == '':
			try:
				await client.voice_clients[0].disconnect()
			except Exception as e:
				print(f"{e}")
			return "Cont"
		try:
			new = int(new)
		except:
			None
		if type(new) is str:
			member = discord.utils.get(ctx.guild.members, name=new)
			if member is None:
				member = ctx.guild.get_member_named(member)
		elif type(new) is int:
			member = await ctx.guild.fetch_member(new)
		try:
			await member.move_to(None)
		except:
			return "Cont"
	
	# elif com.startswith('annoy'):
		# new = com.replace('annoy ', '')
		# try:
			# new = int(new)
		# except:
			# pass
		# if type(new) is str:
			# member = discord.utils.get(ctx.guild.members, name=new)
			# if member is None:
				# member = ctx.guild.get_member_named(member)
		# else:
			# member = await ctx.guild.fetch_member(int(new))
		# while True:
			# try:
				# for chan in ctx.guild.voice_channels:
					# await member.move_to(chan)
					# await sleep(0.7)
			# except:
				# break
		
	elif com.startswith('move'):
		new = com.replace('move ', '')
		print("GUILD VOICE CHANNELS:") 
		for channel in ctx.guild.voice_channels:
			print(f"NAME: {channel.name} ID: {channel.id}")
		chn = input("Channel ID: ")
		if chn is None:
			chn = ctx.guild.get_channel(778272911063646258)
		else:
			try:
				if type(chn) is int:
					chn = ctx.guild.get_channel(int(chn))
				elif type(chn) is str:
					chn = discord.utils.get(ctx.guild.voice_channels, name=chn)
			except:
				print("Error")
				return "Cont"
		if new == '':
			try:
				await ctx.guild.me.move_to(chn)
			except:
				None
			return "Cont"
		try:
			new = int(new)
		except:
			None
		if type(new) is str:
			member = discord.utils.get(ctx.guild.members, name=new)
			if member is None:
				member = ctx.guild.get_member_named(new)
		elif type(new) is int:
			member = await ctx.guild.fetch_member(new)
		try:
			await member.move_to(chn)
		except:
			return "Cont"

	elif com.startswith('mute'):
		new = com.replace('mute ', '')
		if new == '':
			await ctx.guild.me.edit(mute=True)
			return "Cont"
		try:
			new = int(new)
		except:
			None
		if type(new) is str:
			member = discord.utils.get(ctx.guild.members, name=new)
			if member is None:
				member = ctx.guild.get_member_named(new)
		elif type(new) is int:
			member = await ctx.guild.fetch_member(new)
		try:
			await member.edit(mute=True)
		except:
			return "Cont"
			
	elif com.startswith('unsup'):
		new = com.replace('unsup ', '')
		if new == '':
			await ctx.guild.me.edit(suppress=False)
			return "Cont"
		try:
			new = int(new)
		except:
			pass
		if type(new) is str:
			member = discord.utils.get(ctx.guild.members, name=new)
			if member is None:
				member = ctx.guild.get_member_named(new)
		elif type(new) is int:
			member = await ctx.guild.fetch_member(new)
		try:
			await member.edit(suppress=False)
		except Exception as e:
		    print(f"{e}")
		    return "Cont"		
	elif com.startswith('unmute'):
		new = com.replace('unmute ', '')
		if new == '':
			await ctx.guild.me.edit(mute=False)
			return "Cont"
		try:
			new = int(new)
		except:
			None
		if type(new) is str:
			member = discord.utils.get(ctx.guild.members, name=new)
			if member is None:
				member = ctx.guild.get_member_named(new)
		elif type(new) is int:
			member = await ctx.guild.fetch_member(new)
		try:
			await member.edit(mute=False)
		except:
			return "Cont"
			
	elif com.startswith('deafen'):
		new = com.replace('deafen ', '')
		if new == '':
			await ctx.guild.me.edit(deafen=True)
			return "Cont"
		try:
			new = int(new)
		except:
			None
		if type(new) is str:
			member = discord.utils.get(ctx.guild.members, name=new)
			if member is None:
				member = ctx.guild.get_member_named(new)
		elif type(new) is int:
			member = await ctx.guild.fetch_member(new)
		try:
			await member.edit(deafen=True)
		except:
			return "Cont"
			
	elif com.startswith('undeafen'):
		new = com.replace('undeafen ', '')
		if new == '':
			await ctx.guild.me.edit(deafen=False)
			return "Cont"
		try:
			new = int(new)
		except:
			None
		if type(new) is str:
			member = discord.utils.get(ctx.guild.members, name=new)
			if member is None:
				member = ctx.guild.get_member_named(new)
		elif type(new) is int:
			member = await ctx.guild.fetch_member(new)
		try:
			await member.edit(deafen=False)
		except:
			return "Cont"
			
	# thanks to jackson for the annoy code

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
        if ts == 't':
            ts = True
    action = input("Author: ")
    if action == 't':
        lnk = input("Link: ")
        if lnk == '':
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
    c = client.get_channel(store('config.json', 'channel', True))
    global region
    region = store('react.json', None, True)
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
            elif "History" in command:
                print("------HISTORY (200 msg limit)----------")
                def trypass(embed, field, sub=None):
                    try:
                        if not sub:
                            return embed[field]
                        return embed[field][sub]
                    except:
                        return "Invalid Field"
                msgs = await c.history(limit=200).flatten()
                msgss = reversed(msgs)
                for m in msgss:
                    print(f"<TIME> {m.created_at} <AUTHOR> \033[92m{m.author}\033[0m <CONTENT> {m.clean_content}\n")
                    if len(m.embeds) != 0:
                        for embed in m.embeds:
                            e = embed.to_dict()
                            ps = f"    \033[93mEMBED\033[0m \033[91m[title]\033[0m > (\033[94m{trypass(e,'title')}\033[0m) -- \033[91m[description]\033[0m > (\033[94m{trypass(e,'description')}\033[0m) -- \033[91m[author]\033[0m > (\033[94m{trypass(e,'author','name')}\033[0m) -- \033[91m[footer]\033[0m > (\033[94m{trypass(e,'footer','text')}\033[0m)"
                            print(ps)
                            try:
                                field = "        \033[93mFIELDS\033[0m "
                                for ffield in e['fields']:
                                    field = field + f'\033[96m[NF]\033[0m > (\033[91m<NAME>\033[0m \033[94m{ffield["name"]}\033[0m \033[91m<VALUE>\033[m \033[94m{ffield["value"]}\033[0m) '
                                print(f"{field}\n")
                            except:
                                pass
                print("---------------------------------------")
                continue
            elif "LEMMS" in command:
                async for m in c.history(limit=1):
                    lms = m
                    print(m)
                continue
            elif "LMSID" in command:
                try:
                    e = await c.fetch_message(int(command.split('-')[1]))
                    lms = e
                    print(e)
                except Exception as e:
                    print(f"fail {e}")
                continue
            elif "MEMBERADD" in command:
                com = command.split('-')
                try:
                    m = await c.guild.fetch_member(int(com[1]))
                    await m.add_roles(c.guild.get_role(int(com[2])))
                except Exception as e:
                    print(f"fail {e}")
                continue
            elif "MEMBERDEL" in command:
                com = command.split('-')
                try:
                    m = await c.guild.fetch_member(int(com[1]))
                    await m.remove_roles(c.guild.get_role(int(com[2])))
                except Exception as e:
                    print(f"fail {e}")
                continue
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
