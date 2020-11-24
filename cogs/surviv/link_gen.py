# Surviv Link Gen Cog
# Generate party link in surviv.io
import discord
from discord.ext import commands

import asyncio

# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))


# first time using arsenic!
from arsenic import start_session, services, browsers, stop_session

from loggers import AssessLogger, StreamLogger, WarningLogger

class SurvivLinkGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self.name = 'Surviv Link Generator'
        self.url = 'https://surviv.io/'

    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')

    @commands.command(aliases=['link_gen', 'linkgen'], name="link")
    async def link(self, ctx):
        try:
            embed = discord.Embed(description="(1/5) **Starting Process** ...",
                                  color=self.color)
            status = await ctx.send(embed=embed)
            arsenic_session = await start_session(
                services.Geckodriver(),
                browsers.Firefox(),
            )
            embed = discord.Embed(description="(2/5) **Spawned Instance** ...",
                                  color=self.color)
            await status.edit(embed=embed)
            await arsenic_session.get(self.url)
            make_team_btn = await arsenic_session.get_element('#btn-create-team')
            embed = discord.Embed(description="(3/5) **Locating target** ...",
                                  color=self.color)
            await status.edit(embed=embed)
            await make_team_btn.click()
            embed = discord.Embed(description="(4/5) **Retrieving Party Link** ...",
                                  color=self.color)
            await status.edit(embed=embed)
            await asyncio.sleep(2) # add a small sleep delay for the party link to load up (a bit risky)
            party_url = await arsenic_session.get_url()
            embed = discord.Embed(description=f"**Party Link**: {party_url}\nLink Generator will leave in 7 seconds.",
                                  color=self.color)
            await status.edit(embed=embed)
            await asyncio.sleep(4) # waits 7 seconds before leaving
            await status.edit(embed=discord.Embed(description=f"**Party Link**: {party_url}\nLink Generator is leaving soon ...",
                                      color=self.color))

            await asyncio.sleep(6) # add more than 3 for extra time
            embed=discord.Embed(description=f"**Link Generator left.**\nOld Link: {party_url}",
                                      color=self.color)
            embed.set_footer(text=f"{self.name} requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
            await status.edit(embed=embed)
            StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')
            await stop_session(arsenic_session)
        except Exception as e:
            try:
                await stop_session(arsenic_session)
            except:
                pass
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {e}')
            error_embed = discord.Embed(description=f"**{self.name}** command did not run as expected.\nPlease log an issue with `{ctx.prefix}issue`",
                                        color=self.color)
            await ctx.send(embed=error_embed)

def setup(bot):
    bot.add_cog(SurvivLinkGen(bot))
