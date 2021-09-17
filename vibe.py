import os
import random

import discord
from discord.ext import commands

import youtube as yt


queue = []
loop = False
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category='Player'
)

# Create the bot and pass it the modified help_command
client = commands.Bot(
    command_prefix="!",
    help_command=help_command
)


@client.command(name="play", help="Loads your input and adds it to the queue; If there is no playing track, then it will start playing.")
async def play(ctx, url: str):
    try:
        channel = ctx.author.voice.channel
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(channel))
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    except Exception as ex:
        print(ex)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    queue.append(yt.stream(url))
    if voice.is_playing():
        await ctx.send("Added " + queue[-1][0] + " to queue.")
    else:
        await ctx.send("Playing " + queue[0][0])
        if loop is True:
            voice.play(discord.FFmpegPCMAudio(queue[0][2], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx, voice=voice, queue=queue))
        if loop is False:
            voice.play(discord.FFmpegPCMAudio(queue[0][2], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx, voice=voice, queue=queue))
            queue.pop(0)


def play_next(ctx, queue, voice):
    if len(queue) > 0:
        ctx.send("Playing " + queue[0][0])
        if loop is True:
            voice.play(discord.FFmpegPCMAudio(queue[0][2], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx, voice=voice, queue=queue))
        if loop is False:
            voice.play(discord.FFmpegPCMAudio(queue[0][2], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx, voice=voice, queue=queue))
            queue.pop(0)
    else:
        print('All Tracks Played')


@client.command(name="pause", help="Pauses playback.")
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command(name="resume", help="Resumes playback.")
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command(name="skip", help="Skips to the next song.")
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if len(queue) > 0:
        voice.stop()
        play_next(ctx, voice=voice, queue=queue)
        await ctx.send("Skipping track.")
    else:
        await ctx.send("Cannot skip because queue is empty.")


@client.command(name="shuffle", help="Shuffles queue.")
async def shuffle(ctx):
    try:
        random.shuffle(queue)
        await ctx.send("The tracks have been shuffled.")
    except Exception as ex:
        print(ex)
        await ctx.send("Failed to shuffle tracks. Make sure there are songs in the queue.")


@client.command(name="repeat", help="Loops currently playing song. Type again to toggle off.")
async def repeat(ctx):
    global loop
    if loop is False:
        loop = True
        await ctx.send("Repeat turned on.")
    elif loop is True:
        loop = False
        await ctx.send("Repeat turned off.")
    print(loop)


@client.command(name="clear", help="Clears queue.")
async def clear(ctx):
    if len(queue) > 0:
        queue.clear()
        await ctx.send("Queue has been cleared.")
    else:
        await ctx.send("The queue is already empty.")


@client.command(name="leave", help="Disconnects bot from voice channel and clears queue.")
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("No such command. For assistance type, !help")

client.run(os.environ['token'])
