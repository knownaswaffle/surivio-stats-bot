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

class SurvivInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self.name = "Surviv Description"

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    @commands.command(aliases=['information'], name="info")
    async def info(self, ctx):
        """ Info Command  """
        try:
            surviv_brief_desc = "\"Surviv.io is a popular top-down battle royale game in which players spawn on an island and gear up to fight each other to be the last one standing and win the chicken dinner. As well as having outstanding mechanics and game knowledge, players must choose from a variety of different weapons, skins, and equipments in order to outplay their opponents and survive.\" - **Surviv.io Wiki**\n\nYou can play at https://surviv.io/."
            embed = discord.Embed(description=f"**What is surviv.io?**\n\n{surviv_brief_desc}",
                                  color = self.color)
            embed.set_footer(text=f"{self.name} requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed) 
        except Exception as e:
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')

def setup(bot):
    bot.add_cog(SurvivInfo(bot))

