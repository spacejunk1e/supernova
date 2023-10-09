# cogs / test.py
from discord.ext import commands
import logging


class Birthday(commands.Cog):
    def __init__(self, client):
        self.client = client  # sets the client variable so we can use it in cogs

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'{self.client.user} has connected to Discord!')

    @commands.command()
    async def command(self, ctx):
        await ctx.send("Hello World!")


# an example command with cogs

async def setup(client):
    await client.add_cog(Test(client))
