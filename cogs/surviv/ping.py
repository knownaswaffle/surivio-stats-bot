# Surviv Ping Cog
# Gives you the current ping of the bot
import discord
from discord.ext import commands

import traceback

# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self.name = "Surviv Ping"

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    @commands.command(name="ping")
    async def ping(self, ctx):
        """ Ping Command  """
        try:
            await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
            
        except Exception as e:
     
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')

def setup(bot):
    bot.add_cog(SurvivPing(bot))

