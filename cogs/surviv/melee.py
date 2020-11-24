# Surviv Melee Cog
# Return the stats of a melee weapon in surviv.io
# utilizes the api to get data from updated table
import discord
from discord.ext import commands
import traceback

# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
import aiosqlite
import string

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivMelee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self._session = self.bot._session
        self.name = "Surviv Melee"
        self.url = "https://survivio.fandom.com/wiki/Melee_Weapons"

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')


    # might need a few arguments in the function
    @commands.command(aliases=['melees'], name="melee")
    async def melee(self, ctx, *args):
        wep = ' '.join(args).strip()
        if wep == '':
            wep = "''"
        try:
            conn = await aiosqlite.connect('data/rotating/surviv.db')
            c = await conn.cursor()
            await c.execute('select * from melee')
            res = await c.fetchall()
            for t in res:
                if wep.lower() == t[0]:
                    break
            if t[0] != wep.lower():
                weps = [string.capwords(i) for i in list(zip(*res))[0]]
                embed = discord.Embed(
                    description=f'"**{wep}**" is not a valid melee weapon in **surviv.io**\n\n**Valid Weapons**: {", ".join(weps)}',
                    color=self.color,
                )
                embed.set_footer(text=f"{self.name} Stats requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"{string.capwords(t[0])} Stats",
                    description=f"**Damage**: {t[2]} \n **Attack Radius**: {t[3]} \n **Equip Speed**: {t[1]} \n **Cooldown Time**: {t[4]} \n **Auto Attack**: {t[5]} \n",
                    color=self.color,
                )
                embed.set_footer(text=f"{self.name} Stats requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')
            await conn.close()
        except Exception as e:
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')
            try:
                 await conn.close()
            except:
                pass

def setup(bot):
    bot.add_cog(SurvivMelee(bot))

# USE STRCAMPS ON THE WEAPON TITLE
# SOMETIMES IT RETURNS THE WRONG TIME
