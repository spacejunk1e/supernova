import re
import discord
from discord.ext import commands
import logging

import os

# Constants and Configurations
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
COMMAND_PREFIX = '..'
INTENTS = discord.Intents.default()
INTENTS.message_content = True

# Send a test message to the #development channel
import discord
from overwatch_api.core import AsyncOWAPI

# Constants and Configurations
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
COMMAND_PREFIX = '..'
INTENTS = discord.Intents.default()
INTENTS.message_content = True
OW_PLATFORM = os.getenv('OW_PLATFORM')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Check Environment Variables
if BOT_TOKEN is None or OPENAI_API_KEY is None:
    logging.error("Error: BOT_TOKEN or OPENAI_API_KEY is not set in the environment variables!")
    exit(1)

# Initialize the bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, description='A simple Discord bot', intents=INTENTS)


async def get_history_of_channel(channel):
    messages = await channel.history(limit=None)
    for message in messages:
        # check if message content matches a specific regex pattern
        if re.match('your-regex-pattern', message.content):
            print(message.content)


# Events and Commands
@bot.event
async def on_ready():
    """
    Event handler for when the bot is ready.
    """
    logging.info(f'{bot.user} has connected to Discord!')


@bot.command(name='hello')
async def hello(ctx):
    """
    Command to say hello.
    """
    logging.info('Received hello command!')
    await ctx.send("Hello!")


bot.run(BOT_TOKEN)
