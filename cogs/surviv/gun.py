# Surviv Gun Cog
# Return the stats of a gun in surviv.io
# utilizes the api to get data from updated table
import discord
from discord.ext import commands

import aiosqlite
import traceback
import string # for capwords


# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivGun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self._session = self.bot._session
        self.name = "Surviv Gun"

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    @commands.command(aliases=['guns'], name="gun")
    async def gun(self, ctx, *args):
        gun = ' '.join(args).strip()
        if gun == '':
            gun = "''"
        try:
            conn = await aiosqlite.connect('data/rotating/surviv.db')
            c = await conn.cursor()
            await c.execute('select * from guns')
            res = await c.fetchall()
            for t in res:
                if gun.lower() == t[0].lower():
                    break
            if t[0].lower() != gun.lower():
                guns = [i for i in list(zip(*res))[0]]
                embed = discord.Embed(
                    description=f"\"**{gun}**\" is not a valid gun in **surviv.io**\n\n**Valid Guns**: {', '.join(guns)}",
                    color=self.color,
                )
                embed.set_footer(text=f"{self.name} Stats requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{t[0]} Stats",
                    description=f"**Bullet Damage**: {t[1]} \n **Shot Spread**: {t[2]} \n **Reload Time**: {t[3]} \n **Firing Delay**: {t[4]}",
                    color=self.color,
                )
                embed.set_footer(text=f"{self.name} Stats requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')
            await conn.close()
        except Exception as e:
            try:
                 await conn.close()
            except:
                pass
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')
def setup(bot):
    bot.add_cog(SurvivGun(bot))
