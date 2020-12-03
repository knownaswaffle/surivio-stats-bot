# Surviv Info Cog
# Returns some basic info on surviv.io
import discord
from discord.ext import commands

import traceback

# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivSupport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self.name = "Surviv Support"
        self.support_server= 'https://discord.gg/StEcaQk'

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    @commands.command(name="support")
    async def support(self, ctx):
        """ Support Command  """
        try:
            await ctx.send(self.support_server) 
        except Exception as e:
     
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')

def setup(bot):
    bot.add_cog(SurvivSupport(bot))
