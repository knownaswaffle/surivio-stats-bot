# Surviv Update Cog
# This cog scrapes the latest surviv.io update
# It can also return an update feed to view last updates
# ARGS: "feed" (opt.)
import discord
from discord.ext import commands
from bs4 import BeautifulSoup as soupify
import aiosqlite

# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivUpdate(commands.Cog):
    """ surviv.io update cog  """
    def __init__(self, bot):
        self.bot = bot
        self.name = 'Surviv Update'
        self.color = self.bot.color
        self._session = self.bot._session
        self.url = 'http://surviv.io/'
        
    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    @commands.command(aliases=['updates', 'releases', 'release', 'new'], name="update")
    async def update(self, ctx):
        try:
            conn = await aiosqlite.connect('data/rotating/surviv.db')
            c = await conn.cursor()
            await c.execute('select * from new')
            res = await c.fetchall()
            content = res[0][2]
            current_title = res[0][0]
            current_date = res[0][1]
            embed = discord.Embed(title=f'🆕  {current_title} ~ ({current_date}) 🆕 ',
                                  description = f'{content}',
                                  color=self.color)

            embed.set_footer(text=f"{self.name} requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')
            await conn.close()
        except Exception as e:
            try:
                await conn.close()
            except:
                pass
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')
            error_embed = discord.Embed(description=f"**{self.name}** command did not run as expected.\nPlease log an issue with `{ctx.prefix}issue`",
                                        color=self.color)
            await ctx.send(embed=error_embed)

def setup(bot):
    bot.add_cog(SurvivUpdate(bot))



