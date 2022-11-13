# Name: Graham Schacht
# Date: Nov, 2022

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl
import os
from time import sleep

# Get token from Discord Developer Portal
TOKEN = 'PUT YOUR OWN TOKEN'

client = commands.Bot(intents=discord.Intents.all(), command_prefix="l!")

# Indicates bot has logged in on startup
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Activated when user leaves call
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is not None and after.channel is None:
        if os.path.exists(str(member)):
            channel = before.channel
            voice = await channel.connect()

            # Plays the audio file of member
            source = FFmpegPCMAudio(str(member))
            voice.play(source)
            while voice.is_playing():
                sleep(1)
            await voice.disconnect()

# Makes the bot leave the voice channel
@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()

# Sets the users leave sound
# Parameters: url - Youtube link containing leave sound
@client.command(pass_context = True)
async def set(ctx, url:str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    completed = False

    # Downloads the leave sound
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(url, download=False)
            if dictMeta['duration'] > 5:
                await ctx.send("Video is too long")
            else:
                ydl.download([url])

                # Renames the file to the users name
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, str(ctx.message.author))    
                        completed = True

    # Indicates whether leave sound was set or not
    if completed:
        await ctx.send('Leave sound set')
    else:
        await ctx.send('Could not set leave sound')

# Removes the users leave sound
@client.command(pass_context = True)
async def remove(ctx):
    if os.path.exists(str(ctx.message.author)):
        os.remove(str(ctx.message.author))
        await ctx.send("Leave sound removed")
    else:
        await ctx.send("No sound to remove")

# Displays the list of commands the bot can use
@client.command(pass_context = True)
async def commands(ctx):
    await ctx.send("List of commands you can use for Leave Sound Lenny!")
    await ctx.send("l!commands : Displays the list of available commands.")
    await ctx.send("l!set url : Lets you set your leave sound using a youtube link. (Max 5 seconds)")
    await ctx.send("l!remove : Removes your leave sound.")
    await ctx.send("l!leave : Makes the bot leave the voice channel.")

# Runs the bot
client.run(TOKEN)