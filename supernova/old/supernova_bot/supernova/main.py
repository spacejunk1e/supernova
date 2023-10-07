import os
import logging
import openai
from discord.ext import commands
import discord

## CUSTOM TOOL OW
from langchain.tools import BaseTool
from typing import Optional

# class OverwatchTool(BaseTool):
#     name = "overwatch_tool"
#     description = "A tool to fetch details about Overwatch profiles, stats, and achievements."

#     def __init__(self):
#         self.client = AsyncOWAPI()

#     async def _arun(
#         self,
#         battletag: str,
#         action: str,
#         region: str = 'ANY',
#         platform: str = 'PC',
#         run_manager: Optional[CallbackManagerForToolRun] = None,
#     ) -> str:
#         """Use the tool to perform the specified action."""
        
#         if action == "profile":
#             result = await self.client.get_profile(battletag, regions=region, platform=platform)
#         elif action == "stats":
#             result = await self.client.get_stats(battletag, platform=platform)
#         elif action == "achievements":
#             result = await self.client.get_achievements(battletag, platform=platform)
#         elif action == "hero_stats":
#             result = await self.client.get_hero_stats(battletag)
#         else:
#             return f"Action {action} is not recognized."

#         return str(result)


# Set up logging
logging.basicConfig(level=logging.INFO)

# Retrieve the BOT_TOKEN and OPENAI_API_KEY from the environment variables
token = os.getenv('BOT_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')

if token is None or openai_api_key is None:
    logging.error("Error: BOT_TOKEN or OPENAI_API_KEY is not set in the environment variables!")
    exit(1)

# Initialize OpenAI API
openai.api_key = openai_api_key

# Define the intents required for the bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='..', description='A simple Discord bot', intents=intents)


# Command to retrieve Overwatch stats for a player
# @bot.command(name='stats')
# async def stats(ctx, battletag: str):
#     logging.info(f'Received stats command for {battletag}!')
#     profile = await ow_client.get_profile(battletag.replace('#', '-'), platform=PC)
#     await ctx.send(f"Profile for {battletag}: {profile}")

# Event to log when the bot is ready
@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')

# Command to say hello
@bot.command(name='hello')
async def hello(ctx):
    logging.info('Received hello command!')
    await ctx.send("Hello!")

from .overwatch_tool import agent 
# Function to use GPT-3.5-turbo to generate a reply
import re

def format_message(message):
    content = message.content

    # # Find all occurrences of <@(id)> in the message content
    # for mention in re.findall(r'<@(\d+)>', content):
    #     # Get the member object using the ID
    #     member = message.guild.get_member(int(mention))
    #     # Replace the mention with the member's display name
    #     if member:
    #         content = content.replace(f'<@{mention}>', f"@{member.display_name}")

    return f"<@{message.author.id}> said '{content}'"


async def fetch_all_references(message, message_list):
    # If this message has a reference (meaning it's a reply)
    temp_list = []
    
    if message.reference:
        original = await message.channel.fetch_message(message.reference.message_id)
        # Recursively fetch all references for the original message
        await fetch_all_references(original, temp_list)
        # Add the original message to the list
        temp_list.append({"role": "user", "content": format_message(original)})

    # Reverse temp_list and extend message_list with it
    message_list.extend(temp_list)
    return message_list

async def generate_reply(message):
    system_message =  [{"role": "system", "content": "You are a jester-like assistant, known for your witty and deprecating humor. When speaking as <@1140550349166485504>, you provide helpful assistance, but you can't resist making a clever joke, especially when asked if you love the user. Example response: 'Love you? Ha! Only YOUR mom could love you! 😂' Feel free to improvise, but keep it light-hearted and funny. You shall be provided with @X said 'Y' but your responses shall only be given as Y"}]
    messages = []
    historical_messages = []
        # {"role": "system", "content": "You are a jester-like assistant, known for your witty and deprecating humor. When speaking as @YourMom, you provide helpful assistance, but you can't resist making a clever joke, especially when asked if you love the user. Example response: 'Love you? Ha! Only YOUR mom could love you! 😂' Feel free to improvise, but keep it light-hearted and funny."},
    
    # Fetch all referenced messages and add them to the messages list
    await fetch_all_references(message, historical_messages)

    current_message = [{"role": "user", "content": format_message(message)}]

    historical_messages[-10:]

    messages += system_message
    messages += historical_messages
    messages += current_message

    import json
    print(json.dumps(messages, indent=4))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # Updated to GPT-3.5-turbo as per your comment
        messages=messages
    )
    
    return response.choices[0].message['content']

# async def generate_reply(prompt):
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a jester-like assistant, known for your witty and deprecating humor. When speaking as @YourMom, you provide helpful assistance, but you can't resist making a clever joke, especially when asked if you love the user. Example response: 'Love you? Ha! Only YOUR mom could love you! 😂' Feel free to improvise, but keep it light-hearted and funny."},
#             {"role": "user", "content": prompt},

            
#             ]
#     )
#     # response = agent.run(prompt)
#     # return response
#     return response.choices[0].message['content']



# Event to respond to a specific message or general mentions
@bot.event
async def on_message(message):
    # We don't want the bot to reply to itself
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        # Generate a reply using GPT-3.5-turbo
        reply = await generate_reply(message)
        await message.channel.send(reply, reference=message)
        # Process other commands
        await bot.process_commands(message)
    else:
        # Process other commands if this is not the specific message
        await bot.process_commands(message)



# Event to log any command errors
@bot.event
async def on_command_error(ctx, error):
    logging.error(f'An error occurred: {error}')

bot.run(token)
