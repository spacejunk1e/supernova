import os
import logging
import openai
from discord.ext import commands
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

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize the bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, description='A simple Discord bot', intents=INTENTS)

# Initialize Overwatch API client
ow_client = AsyncOWAPI()


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


@bot.command(name='stats')
async def stats(ctx, battletag: str):
    """
    Command to get Overwatch stats for a given battletag.
    """
    logging.info(f'Received stats command for {battletag}!')
    try:
        profile = await ow_client.get_profile(battletag.replace('#', '-'), platform=OW_PLATFORM)
        await ctx.send(f"Profile for {battletag}: {profile}")
    except Exception as e:
        logging.error(f"Error retrieving stats for {battletag}: {e}")
        await ctx.send(f"An error occurred while retrieving stats for {battletag}.")


@bot.event
async def on_message(message):
    """
    Event handler for when a message is received.
    """
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        prompt = message.content
        reply = await generate_reply(prompt)
        await message.channel.send(reply)

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """
    Event handler for when a command raises an error.
    """
    logging.error(f'An error occurred: {error}')


# Function to generate reply using GPT-3.5-turbo
async def generate_reply(prompt):
    """
    Function to generate a reply using the OpenAI API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a jester-like assistant, known for your witty and deprecating humor. When speaking as @YourMom, you provide helpful assistance, but you can't resist making a clever joke, especially when asked if you love the user. Example response: 'Love you? Ha! Only YOUR mom could love you! 😂' Feel free to improvise, but keep it light-hearted and funny."},
                {"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logging.error(f"Error generating reply for prompt '{prompt}': {e}")
        return "An error occurred while generating a reply."


bot.run(BOT_TOKEN)