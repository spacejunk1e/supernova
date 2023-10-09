import logging
import re
from collections import defaultdict

import discord
from discord.ext import commands

# Regex pattern to match URLs
URL_PATTERN = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class LeaderboardFlags(commands.FlagConverter):
    time_frame: str = commands.flag(default='daily', description='The time frame to display the leaderboard for')
    channel_name: str = commands.flag(default='<#1137690004097880146>',
                                      description='The channel to display the leaderboard for')


class Leaderboards(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {
            'daily': {},
            'weekly': {},
            'monthly': {}
        }

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'{self.client.user} has connected to Discord!')
        guilds = list(self.client.guilds)
        guild = guilds[0]
        categories = list(guild.categories)
        for category in categories:
            if category.name != "🫶____SHARING____🫶":
                continue
            logging.info(f"Found category: {category.name}")
            channels = list(category.channels)
            for channel in channels:
                # self.data['daily'][channel.name] = {}
                # self.data['weekly'][channel.name] = {}
                # self.data['monthly'][channel.name] = {}
                #
                # logging.info(f"Channel: {channel}")
                # logging.info(f"Channel name: {channel.name}")
                # logging.info(f"Channel type: {channel.type}")
                # logging.info(f"Channel id: {channel.id}")

                contained = dir(channel)
                logging.info(f"Channel contains: {contained}")
                logging.info(f"Found channel: {channel.name}")
                result = await self.get_history_of_channel(channel)
                channel_key = "<#" + str(channel.id) + ">"
                self.data['daily'][channel_key] = result
                self.data['weekly'][channel_key] = result
                self.data['monthly'][channel_key] = result
                logging.info(f"Result: {self.data}")

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx, *, flags: LeaderboardFlags):
        time_frame = flags.time_frame
        channel_name = flags.channel_name
        """
        Command to display the leaderboard.
        """
        logging.info('Received leaderboard command!')

        # # Define mock data for each time frame and channel
        # mock_data = {
        #     'daily': {
        #         '<#1155522318202851460>': {'@User1': 10, '@User2': 9, '@User3': 8},
        #         '#music': {'@User4': 15, '@User5': 12},
        #         '#art-and-photography': {'@User6': 20, '@User7': 18},
        #     },
        #     'weekly': {
        #         '<#1155522318202851460>': {'@User1': 100, '@User2': 90, '@User3': 85},
        #         '#music': {'@User4': 150, '@User5': 120},
        #         '#art-and-photography': {'@User6': 200, '@User7': 180},
        #     },
        #     'monthly': {
        #         '<#1155522318202851460>': {'@User1': 400, '@User2': 350, '@User3': 300},
        #         '#music': {'@User4': 500, '@User5': 480},
        #         '#art-and-photography': {'@User6': 600, '@User7': 580},
        #     }
        # }

        logging.info(f"Time frame: {time_frame}")
        logging.info(f"Channel name: {channel_name}")

        # Validate time frame and channel name
        if time_frame.lower() not in self.data:
            await ctx.send("Invalid time frame. Please choose 'daily', 'weekly', or 'monthly'.")
            return
        logging.info(f"AAAAA {self.data[time_frame.lower()]=}")
        logging.info(f"AAAAA {channel_name.lower()=}")
        if channel_name.lower() not in self.data[time_frame.lower()]:
            valid_channels = list(self.data[time_frame.lower()].keys())
            await ctx.send("Invalid channel name. Please choose one of the following: " + ", ".join(valid_channels))
            return

        # Fetch and sort the appropriate data
        selected_data = self.data[time_frame.lower()][channel_name.lower()]
        sorted_data = {k: v for k, v in sorted(selected_data.items(), key=lambda item: item[1], reverse=True)}

        # Create the leaderboard message
        names = list(sorted_data.keys())
        values = list(sorted_data.values())
        message = f"🏆 **{time_frame.capitalize()} Leaderboard for {channel_name}** 🏆\n"
        for i in range(len(names)):
            message += f"{i + 1}. **{names[i]}**: {values[i]} points\n"

        await ctx.send(message)

        # await ctx.send(content="Here's the leaderboard:", file=file)

    async def get_history_of_channel(self, channel):
        """Fetch and process the entire message history of a specific channel.

        Parameters
        ----------
        channel : discord.TextChannel
            The channel whose message history we want to fetch and process.
        """
        user_scores = defaultdict(int)  # A dictionary to keep track of each user's score

        async for message in channel.history(limit=None):
            # Ignore messages from the bot itself
            if message.author == self.client.user:
                continue

            user = message.author.name  # You can also use `message.author.id` if you want a unique identifier

            # Check for attachments (images, etc.)
            if message.attachments:
                user_scores[user] += len(message.attachments)
                for attachment in message.attachments:
                    logging.info(f"Found attachment: {attachment.url}")

            # Check for URLs using regex
            urls = URL_PATTERN.findall(message.content)
            if urls:
                user_scores[user] += len(urls)
                logging.info(f"Found URLs: {urls}")

            # Check for reactions
            if message.reactions:
                for reaction in message.reactions:
                    # Assume each reaction counts as 1 point for the user who posted the message
                    user_scores[user] += reaction.count
                    logging.info(f"Found reaction: {reaction.emoji} x {reaction.count}")

        # Now user_scores contains the scores for each user
        sorted_scores = {k: v for k, v in sorted(user_scores.items(), key=lambda item: item[1], reverse=True)}
        return sorted_scores

    @commands.command()
    async def command(self, ctx):
        await ctx.send("Hello World!")


async def setup(client):
    await client.add_cog(Leaderboards(client))
