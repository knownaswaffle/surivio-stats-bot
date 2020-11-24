# Surviv Twitch Cog
# This cog scrapes a list of the current
# twitch streamers
import discord
from discord.ext import commands


# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivTwitch(commands.Cog):
    """ Grabs top streaming twitch streamers  """
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self._session = self.bot._session
        self.url = 'https://surviv.io/api/site_info?language=en'
        self.headers = {"content-type": "application/json; charset=utf-8"}
        self.name = 'Surviv Twitch'

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    @commands.command(aliases=['streamers', 'streamer'], name="twitch")
    async def twitch(self, ctx):
        try:
            async with self._session.get(self.url, headers=self.headers) as r:
                raw_json = await r.json()
                # parse json
                embed = discord.Embed(title="Current Surviv Streamers",
                                      description="[Surviv.io on Twitch!](https://www.twitch.tv/directory/game/surviv.io)",
                                      color=self.color)
                for t in raw_json['twitch']:
                    embed.add_field(name=f"Streamer: {t['name']}", value=f"Watch: [{t['title']}]({t['url']})\nViewers: `{t['viewers']}`",
                                    inline = True)
                if not len(raw_json['twitch']):
                    embed = discord.Embed(description="No Surviv Twitch Streamers are **currently streaming**.",
                                              color=self.color)
                embed.set_footer(text=f"{self.name} Dashboard  requested by {ctx.message.author}",
                                 icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')
                
        except Exception as e:
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')
            error_embed = discord.Embed(description=f"**{self.name}** command did not run as expected.\nPlease log an issue with `{ctx.prefix}issue`",
                                        color=self.color)
            await ctx.send(embed=error_embed)

def setup(bot):
    bot.add_cog(SurvivTwitch(bot))
