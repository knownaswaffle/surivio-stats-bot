# Surviv Player Cog
# Return the player stats for a single player in surviv.io
import discord
from discord.ext import commands

# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self._session = self.bot._session
        self.name = "Surviv Player"
        self.url = "https://surviv.io/api/user_stats"
        self.headers = {"content-type": "application/json; charset=UTF-8"}

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    # might need a few arguments in the function
    @commands.command(aliases=['surviver', 'user'], name="player")
    async def player(self, ctx, player_name):
        try:
            player_lowered = player_name.lower()
            player_payload = {"slug": f"{player_lowered}", "interval": "all", "mapIdFilter": "-1"}
            async with self._session.post(self.url,
                               headers=self.headers,
                               json=player_payload) as r:
                player_data = await r.json()
            if not player_data: # no such player
                embed = discord.Embed(description=f"**{player_name}** is not a valid player of surviv.io.",
                                      color=self.color)
                embed.set_footer(text=f"{self.name} Stats requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                kills = player_data["kills"]
                wins = player_data["wins"]
                games = player_data["games"]
                kg = player_data["kpg"]
                mostkills = max([i["mostKills"] for i in player_data["modes"]])
                maxDamage = max([i["mostDamage"] for i in player_data["modes"]])
                embed = discord.Embed(
                    title=f" **{player_data['username']}'s Stats**",
                    description=f"**Wins**: {wins} \n **Kills**: {kills} \n **Games**: {games} \n **Kill Per Game Avg**: {kg} \n **Max Kills**: {mostkills} \n **Most Damage**: {maxDamage}",
                    color=self.color,
                )
                embed.set_footer(text=f"{self.name} Stats requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

            StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')

        except Exception as e:
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')
            error_embed = discord.Embed(description=f"**{self.name}** command did not run as expected.\nPlease log an issue with `{ctx.prefix}issue`",
                                        color=self.color)
            await ctx.send(embed=error_embed)

def setup(bot):
    bot.add_cog(SurvivPlayer(bot))
