"""
A Discord bot launcher that initializes a bot with certain intents and loads extensions.
"""

import asyncio
import logging
import os

from discord.ext import commands
import discord
from dotenv import load_dotenv

# Constants
INTENTS = discord.Intents.default()
INTENTS.message_content = True


def setup_logging():
    """Set up logging for the application."""
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


async def load_extensions(client):
    """
    Load extensions for the Discord bot.

    Parameters
    ----------
    client : commands.Bot
        The Discord bot instance.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension_name = f"cogs.{filename[:-3]}"
            try:
                await client.load_extension(extension_name)
                logging.info(f"Successfully loaded extension {extension_name}")
            except Exception as e:
                logging.error(f"Failed to load extension {extension_name}. Reason: {e}")


from discord import app_commands


async def main():
    """
    Main asynchronous function to load environment variables, initialize the bot, load extensions,
    and start the bot.
    """
    # Load environment variables
    load_dotenv()
    logging.info("Environment variables loaded.")

    # Initialize the bot
    client = commands.Bot(command_prefix="/", intents=INTENTS)
    logging.info("Bot initialized.")

    # import matplotlib.pyplot as plt
    # import io

    await load_extensions(client)

    # Run the bot
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if BOT_TOKEN:
        logging.info("Starting the bot.")
        await client.start(BOT_TOKEN)
    else:
        logging.error("BOT_TOKEN not found. Exiting.")


if __name__ == '__main__':
    setup_logging()
    asyncio.run(main())
