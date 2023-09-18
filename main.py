import discord
import json
from discord.ext import commands, tasks

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix="he ", intents=intents)

# Load channel IDs from JSON file
try:
    with open("channels.json", "r") as f:
        channels = json.load(f)
except FileNotFoundError:
    channels = []

# Save channel IDs to JSON file
def save_channels():
    with open("channels.json", "w") as f:
        json.dump(channels, f)

# Command to start posting YouTube link
@bot.command(name="throw")
async def throw(ctx):
    channel_id = ctx.channel.id
    if channel_id not in channels:
        channels.append(channel_id)
        save_channels()
        await ctx.send("*chirp chirp*")  # Message when a channel is subscribed
        await ctx.send("https://www.youtube.com/watch?v=bFvqf8Z13PU")

# Command to stop posting YouTube link
@bot.command(name="go")
async def go(ctx):
    channel_id = ctx.channel.id
    if channel_id in channels:
        channels.remove(channel_id)
        save_channels()
        await ctx.send("https://i.imgur.com/vRrMlJY.png")

# Task to post YouTube link
@tasks.loop(hours=1)
async def post_link():
    for channel_id in channels:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send("https://www.youtube.com/watch?v=bFvqf8Z13PU")

# Start task when bot is ready and send "tweep" in all subscribed channels
@bot.event
async def on_ready():
    for channel_id in channels:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send("tweep")  # Message when the bot goes online
    post_link.start()

# Run the bot
bot.run("token")
