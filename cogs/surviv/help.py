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
            disc = f"\n**NOTE**: You can find the arguments a command supports by typing the command with `args` at the end.\n**Example**: `{ctx.prefix}player`\n"
            intro = "The Riptide Bot supports commands for the game **surviv.io**.\nThe Game is playable at https://surviv.io/."
            info_command_desc  = f"ℹ `{ctx.prefix}info` - Returns some information on the game surviv.io.\n"
            melee_command_desc = f"🔪 `{ctx.prefix}melee` - Returns stats for a melee weapon in surviv.io.\n"
            link_command_desc = f"🔗 `{ctx.prefix}link` - Returns a party link for surviv.io that expires in 7 seconds.\n"
            gun_command_desc = f"\U0001F52B `{ctx.prefix}gun` - Returns stats for a gun in surviv.io.\n"
            player_command_desc = f"⛹ `{ctx.prefix}player` - Returns stats for a player in surviv.io.\n"
            twitch_command_desc = f"🕹️ `{ctx.prefix}twitch` - Returns the top streamers currently streaming surviv.io.\n"
            update_command_desc = f"🆕 `{ctx.prefix}update` - Returns the current update in surviv.io.\n" 
            embed = discord.Embed(title="<:surviv:743213975889641575>  Surviv.io Commands  <:surviv:743213975889641575>",
                                  description = f"{disc}\n{intro}\n\n{info_command_desc}{melee_command_desc}{link_command_desc}{gun_command_desc}{player_command_desc}{twitch_command_desc}{update_command_desc}",
                                  color=self.color)
            embed.set_footer(text=f"{self.name} Dashboard requested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            StreamLogger.log(f'{ctx.message.author} ran {self.name} Command successfully.')
        except Exception as e:
            WarningLogger.log(f'{ctx.message.author} ran {self.name} Command unsuccessfully. Raised {traceback.format_exc()}')

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(SurvivHelp(bot))
