import re
import os
import yaml
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'player_list_api',
    'version': '0.1.0',
    'name': 'PlayerListAPI',
    'description': "A MCDR plugin for listing players and bots",
    'author': ['Youmiel'],
    'link': '',
    'dependencies': {
		'mcdreforged': '>=1.0.0',
	}
}

online_list = [] # all player entities
bot_list = []    # bots

PLAYER_PATTERN = re.compile(r'(\w+)\[([0-9\.:/]+|local|CarpetPlugin)\] logged in with entity id')
                # compatibility with CarpetPlugin by ishland (for paperspigot users)
CONFIG_PATH = os.path.join('config', 'PlayerListAPI.yml')

default_config = {
    'tag_bots': False,  # an option for datapacks
    'isCarpet': True,   # false for player list only, true for carpet feature(CarpetPlugin too)
    'clean_logs': True  # prevent /tag command feedback in logs
    }
config = default_config.copy()

#-------API START-------

def get_list_all():
    return online_list.copy()
    
def get_list_player():
    player_list = online_list.copy()
    for bot in bot_list:
        player_list.remove(bot)
    return player_list.copy()
    
def get_list_bot():
    return bot_list.copy()

#--------API END--------

def on_load(server: ServerInterface, old_module):
    #TODO: config, OOP(list)
    global online_list, bot_list
    if old_module and type(old_module.online_list) == type(online_list):
        online_list = old_module.online_list
        bot_list = old_module.bot_list
    load_config(server)

def on_server_startup(server: ServerInterface):
    global online_list, bot_list
    online_list = []
    bot_list = []
    
def on_player_joined(server: ServerInterface, player, info):
    global online_list, bot_list
    online_list.append(player)
    if config['isCarpet']:
        botinfo = judge_bot(info.content)
        if botinfo[1] == 'bot' and player not in bot_list:
            bot_list.append(player)
            if config['tag_bots']:
                add_tag(server, player)                
        elif config['tag_bots'] and botinfo[1] == 'player':
            remove_tag(server, player)

def on_player_left(server: ServerInterface, player):
    global online_list, bot_list
    online_list.remove(player)
    if player in bot_list:
        bot_list.remove(player)

def load_config(server: ServerInterface):
    global config;
    try:
        config = {};
        with open(CONFIG_PATH) as file: 
            conf_yaml = yaml.load(file, Loader=yaml.Loader) # idk why CLoader doesn't work
            for key in default_config.keys():
                config[key] = conf_yaml[key]
            server.logger.info('Config file loaded')
    except Exception as e: 
        server.logger.info('fail to read config file: %s using default config'%e)
        config = default_config.copy()
        with open(CONFIG_PATH, 'w') as file: 
            yaml.dump(default_config, file)
    

def judge_bot(msg):
    global PLAYER_PATTERN
    joined_player = re.match(PLAYER_PATTERN, msg)
    if joined_player:
        if joined_player.group(2) == 'local':
            return [True, 'bot', joined_player.group(1)] # return [<isPlayer>,<type>,<name>]
        else:
            return [True, 'player', joined_player.group(1)]
    return [False]

def add_tag(server:ServerInterface, bot):
    if config['clean_logs']:
        server.execute('execute as %s run tag @s[tag=!isBot] add isBot'%bot)
    else:
        server.execute('tag %s add isBot'%bot) # will produce one more line in log
    
def remove_tag(server:ServerInterface, bot):
    if config['clean_logs']:
        server.execute('execute as %s run tag @s[tag=isBot] remove isBot'%bot)
    else:
        server.execute('tag %s remove isBot'%bot) # will produce one more line in log
  
  
    '''
def on_info(server: ServerInterface, info):    #debug use
    global online_list, bot_list
    if info.is_player and info.content == '!!list':
            send_list(server)

@new_thread("send_list")
def send_list(server: ServerInterface):        #debug use
    global online_list, bot_list
    server.logger.info("online_list: %s" % online_list)
    server.logger.info("bot_list: %s" % bot_list)
    player_list = online_list.copy()
    for bot in bot_list:
        player_list.remove(bot)
    server.logger.info("player_list: %s" % player_list)
    '''