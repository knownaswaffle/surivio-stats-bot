# Python program to explain os.system() method  
      
# importing os module  
import os  
  
# Command to execute 
# Using Windows OS command 
cmd = 'pip install discord.py'
  
# Using os.system() method 
os.system(cmd) 
# run with -B flag to supress byte compiled pycache


import discord
from discord.ext import commands, tasks

from loggers import AssessLogger, WarningLogger, ErrorLogger, StreamLogger
from utils.session_handlers import wrapup_all, get_current_time

import requests
from bs4 import BeautifulSoup as soupify
import yaml
import os
import aiohttp
import shutil
import aiosqlite
import sys
import traceback

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# remove __pycache__ in main dir
try:
    shutil.rmtree('__pycache__')
except:
    pass # if it's already removed

# gettings some static variables
BOT_TOKEN = config.get('BOT_TOKEN')
DEVELOPERS = config.get('DEVELOPERS')
SHARD_COUNT = config.get('SHARD_COUNT')
EMBED_COLOR = config.get('DEFAULT_COLOR')
DEFAULT_PREFIX = config.get('DEFAULT_PREFIX')

dont_load = {'surviv': ['match.py'], 'krunker': ['player.py', 'clan.py']}


class RiptideBot(commands.AutoShardedBot):
    def __init__(self, **params):
        """ Initialize Bot with params   """
        super().__init__(DEFAULT_PREFIX, **params)
        self.developers = DEVELOPERS
        self.color = EMBED_COLOR
         # initialize session once
        self.dont_load = dont_load
        self._session = aiohttp.ClientSession()

    def startup(self):
        """" Startup bot and load all cogs """
        try:
            os.remove('cogs/__pycache__')
        except FileNotFoundError:
            WarningLogger.log('Could not remove __pycache__ (did not exist).')

        for game in os.listdir('cogs'): # load all cogs
            for cog in os.listdir('cogs/' + game):
                if cog.endswith('.py') and cog not in self.dont_load[game]: # don't load cogs if they're in don't load
                    try:
                        self.load_extension("cogs." + game + '.'+ cog[:-3])
                        AssessLogger.log(f'Successfully loaded {cog} extension from {game} folder.')
                    except Exception as e:
                        error_state = 'Could not load cog: {} from {} folder. Raised {}'
                        if not str(e).endswith('.'): # tiny tidbit to make logs a bit more cleaner
                            error_state += '.'
                        ErrorLogger.log(error_state.format(cog, game, str(e)))
                        AssessLogger.log('Encountered Error: Could not load Cog.')
                        wrapup_all()
                elif cog == '__pycache__':
                    shutil.rmtree(f'cogs/{game}/{cog}')
                else:
                    AssessLogger.log(f'Not loading {cog} cog from {game} folder.')
        print('All Cogs Loaded.')


# Scrape the some website stats for storing
# they don't change that often
# it'll be faster to return results
# I'll probably want to fix this to allow for merging conflicts
@tasks.loop(hours=12)
async def scrape_via_bs4(bot: RiptideBot):
    await bot.wait_until_ready()
    # Start Surviv Scrape
    try:
        surviv_conn = await aiosqlite.connect('data/rotating/surviv.db')
        surviv_cur = await surviv_conn.cursor()
        await surviv_cur.execute("""CREATE TABLE IF NOT EXISTS GUNS(
        NAME TEXT,
        DAMAGE REAL,
        SPREAD REAL,
        RELOAD REAL,
        DELAY REAL)""") # create table if not exists for reach thing
        await surviv_conn.commit()
        await surviv_cur.execute("""CREATE TABLE IF NOT EXISTS MELEE(
        NAME TEXT,
        SPEED REAL,
        DAMAGE REAL,
        RADIUS REAL,
        COOLDOWN REAL,
        AUTO REAL)""")
        await surviv_conn.commit()
        await surviv_cur.execute("""CREATE TABLE IF NOT EXISTS NEW(
        TITLE TEXT,
        TIME TEXT,
        CHANGE TEXT)""")
        await surviv_conn.commit()

        # get current surviv.io update
        async with bot._session.get("http://surviv.io/") as r:
                raw = await r.read()
        html = soupify(raw, "html.parser")
        current_news = html.find("div", {"id": "news-current"})
        current_title = current_news.find('strong').text
        current_date = current_news.find('small').text
        body = []
        for p in current_news.findAll('p', {"class": 'news-paragraph'})[1:]:
            inner_html = p.decode_contents()
            inner_html = inner_html.replace('<span class="highlight">', '**').replace('</span>', '**') # make highlighted portions bold
            body.append(inner_html)
        content = "\n\n".join(body)
        await surviv_cur.execute("""select * from new""")
        rows = await surviv_cur.fetchall()
        if len(rows) == 0:
            await surviv_cur.execute("""insert into new values ('placeholder', 'placeholder', 'placeholder')""")
        # put the new update in the table
        await surviv_cur.execute("""UPDATE NEW
                                 SET CHANGE = ?,
                                 TITLE = ?,
                                 TIME = ?""",
                                 [content, current_title, current_date])
        await surviv_conn.commit()

        # get the stats of melee in surviv.io
        await surviv_cur.execute("""delete from melee""")
        await surviv_conn.commit()
        url = "https://survivio.fandom.com/wiki/Melee_Weapons"
        async with bot._session.get(url) as r:
            raw_melee = await r.read()
        html = soupify(raw_melee, 'html.parser')
        weapons_html = html.find('table', {'class': 'article-table'})
        weapons = weapons_html.find_all('tr')
        for w in weapons[1:]:
            wep_link = w.find_all("a")[0]["href"]
            wep_name = w.find_all("a")[0].text
            async with bot._session.get("https://survivio.fandom.com/wiki/" + wep_name) as r:
                unparsed = await r.read()
            html = soupify(unparsed, 'html.parser')
            html = soupify(unparsed, "html.parser")
            # quick
            # could've found a better way with thought
            try:
                equip_speed = html.find("div", {"data-source": "equipSpeed"}).text
            except:
                equip_speed = "N/A"
            try:
                damage = html.find("div", {"data-source": "damage"}).text
            except:
                damage = "N/A"
            try:
                rad = html.find("div", {"data-source": "rad"}).text
            except:
                rad = "N/A"
            try:
                cltime = html.find("div", {"data-source": "cooldownTime"}).text
            except:
                cltime = "N/A"
            try:
                auto = html.find("div", {"data-source": "autoAttack"}).text
            except:
                auto = "N/A"
            await surviv_cur.execute("""insert into melee values (?, ?, ?, ?, ?, ?)""",
                               [wep_name.lower(), equip_speed, damage, rad, cltime, auto])
            await surviv_conn.commit()

        # get the stats of guns in surviv.io
        await surviv_cur.execute("""delete from guns""")
        await surviv_conn.commit()
        url = "https://survivio.fandom.com/wiki/Weapons"
        async with bot._session.get(url) as r:
            unparsed = await r.read()
        gun_list = (
                    soupify(unparsed, "html.parser")
                    .find_all("table", {"class": "article-table"})[1]
                    .find_all("tr")
                   )[1:]
        for idx, g in enumerate(gun_list):
            gun_list[idx] = (g.find("a")["href"], g.find("a").text)
        for idx, n in enumerate(gun_list):
            if n[1] == 'M9':
                gun_list = gun_list[idx:]
                break
        for p in gun_list:
            if 'http' in p[0]:
                url = p[0]
            else:
                url = "https://survivio.fandom.com" + p[0]
            async with bot._session.get(url) as r:
                g_unparsed = await r.read()
                html = soupify(g_unparsed, "html.parser")
                try:
                    fire_delay = html.find("div", {"data-source": "fireDelay"}).text
                except:
                    fire_delay = 'N/A'
                try:
                    rel_time = html.find("div", {"data-source": "reloadTime"}).text
                except:
                    rel_time = 'N/A'
                try:
                    spread = html.find("div", {"data-source": "shotSpread"}).text
                except:
                    spread = 'N/A'
                try:
                    damage = html.find("div", {"data-source": "dmg"}).text
                except:
                    damage = 'N/A'
                await surviv_cur.execute("""insert into guns values (?, ?, ?, ?, ?)""",
                                         [p[1], damage, spread, rel_time, fire_delay])
                await surviv_conn.commit()

        # Do Fortnite Scraping
        


        AssessLogger.log('Finished Routine Scrape.')
        # close connection
        await surviv_conn.close()
    except Exception as e:
        ErrorLogger.log(f'Failed get new data. Raised {traceback.format_exc()}')
        AssessLogger.log(f'Failed get new data.')
        wrapup_all()



if __name__ == "__main__":
    time_init, tzname = get_current_time()
    for logger in (AssessLogger, WarningLogger, ErrorLogger, StreamLogger):
        logger.log(f'Session Instantiated ~ {time_init} ({tzname}).')
    riptide = RiptideBot(shard_count = SHARD_COUNT) # instantiate bot
    riptide.startup() # startup bot
    scrape_via_bs4.start(riptide)
    try:
        AssessLogger.log(f'Using Token: {BOT_TOKEN}.')
        riptide.run(BOT_TOKEN)
    except discord.errors.LoginFailure: # improper token passed
        # log as an error
        time_error, tzname = get_current_time()
        ErrorLogger.log(f'Failed to run bot (improper token): {BOT_TOKEN} ~ {time_error} ({tzname}).')
        AssessLogger.log('Encountered Error: Improper Token Passed.')
        # add a divider if session ends (not for stream)
        wrapup_all()


# BAD ARGUMENT ERROR HANDLER NEEDED
# ADD A FEED OF UPDATES FOR SURVIV.IO INSTEAD OF JUST THE CURRENT
# MAKE SURVIV PLAYER HAVE MORE DATA
# FOR ABOVE MAKE ERRORHANDLER
# HERE'S HOW ALL COGS SHOULD LOOK LIKE
# beginning stuff:
#| try:
#|    do everything
#|    StreamLogger.log("success")
#| except Exception as e:
#|   ErrorHandler.check() # logs in the warning as well
#| following this format helps with debugging and having cleaner code
#| LINK GENERATOR SCHEDULE A PARTY LINK (probably premium)
#| MAKE BOT NOT READY UNTIL BS4 TASK IS COMPLETE
#| GET BETTER EMOJIS
#| ADD STREAM LOGGER TO ALL COMMANDS / USE TRACEBACK FOR ALL COMMAND EXCEPTIONS
#| ADD "ARGS" TO THE END OF A COMMAND TO RECIEVE ARG INFORMATION
#| GROUPS ARE NOT WORKING (WE HAVE TO REUSE GROUPS)

# THINGS THE BOT CAN DO
#| GET MAJOR STATS OF ALL GAMES EASILY
#| MOD COMMANDS (KICK, BAN, STRIKE)
#| MAKE PROFILES FOR GAMERS TO MAKE IT EASIER TO VIEW STATS (@someone returns stats)
#| ADD A TOURNEY ASPECT THAT ALLOWS TO CONFIGURE TOURNEY'S, AND THE BOT WILL PUT THE LIVE STREAM IN DISCORD
#| CONFIGURE THE BOT TO RUN ONLY IN CERTAIN CHANNELS
#| ADD A SERVER ROSTER
#| SCHEDULE GAME LINKS FOR TIMES (SCHEDULE TOURNEYS & GAMES)
#| GREET NEWCOMERS
#| CHATS TO TALK TO OTHER SERVERS BOT IS IN FOR CLAN WARS
#| ADVERTISE CLAN WHICH WILL BE SHOWN RANDOMLY
#| HAVE THE BOT HAVE A QUEUE FOR VOICE CHANNEL
#| ALLOW GAMERS FROM DIFFERENT SERVERS TO COMMUNICATE VIA VOICE CHANNEL
#| ADD A GAMER STREAM COMMAND TO LET SHOW WHEN GAMER IS STREAMING
#| ADD A GAMER STREAM COMMAND TO 
#| STREAM A MOVIE

