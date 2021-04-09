# Surviv Help Cog
# Cog that displays the commands you can run
import discord
from discord.ext import commands

import traceback

# temp hack
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from loggers import AssessLogger, StreamLogger, WarningLogger
class SurvivHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color 
        self.name = "Surviv Help"
    
    @commands.Cog.listener()
    async def on_ready(self):
        AssessLogger.log(f'Successfully loaded {self.name} Cog.')
    
    @commands.command(name="help")
    async def help(self, ctx):
        try:
            disc = f"\n**NOTE**: You can find the arguments a command supports by typing the command with `args` at the end.\n**Example**: `{ctx.prefix}player ARGS`\n"
            intro = "Surviv Stat Bot Commands!\nThe Game is playable at https://surviv.io/."
            info_command_desc  = f"ℹ️ `{ctx.prefix}info` - Returns some information on the game surviv.io.\n"
            melee_command_desc = f"🔪 `{ctx.prefix}melee` - Returns stats for a melee weapon in surviv.io.\n"
            link_command_desc = f"🔗 `{ctx.prefix}link` - Returns a party link for surviv.io that expires in 7 seconds.\n"
            ping_command_desc = f"🏓 `{ctx.prefix}ping` - Gets the current latency of the bot.\n"
            gun_command_desc = f"\U0001F52B `{ctx.prefix}gun` - Returns stats for a gun in surviv.io.\n"
            player_command_desc = f"⛹ `{ctx.prefix}player` - Returns stats for a player in surviv.io.\n"
            twitch_command_desc = f"🕹️ `{ctx.prefix}twitch` - Returns the top streamers currently streaming surviv.io.\n"
            update_command_desc = f"🆕 `{ctx.prefix}update` - Returns the current update in surviv.io.\n" 
            website_command_desc = f"🔗`{ctx.prefix}website` - Link to the website.\n" 
            supportserver_command_desc = f"🔗`{ctx.prefix}support` - Link to the support server.\n" 
            surviv_regions_command_desc = f"🌎 `{ctx.prefix}regions` - All of the surviv.io regions.\n"
            ad_command_desc = f"Your Server Could be here! Join the support server for more info.\n"    
            embed = discord.Embed(title="<:survivio:787315420074868768> Surviv.io Commands <:survivio:787315420074868768>",
                                                           description = f"{disc}\n{intro}\n\n{info_command_desc}{melee_command_desc}{ping_command_desc}{gun_command_desc}{player_command_desc}{twitch_command_desc}{update_command_desc}{ surviv_regions_command_desc}{supportserver_command_desc}",                               
        color=self.color)          
            embed.set_footer(text=f"{self.name} Dashboard requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')
        except Exception as e:
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(SurvivHelp(bot))
