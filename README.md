# PlayerListAPI
A MCDR plugin designed for listing players and Carpet/CarpetPlugin bots

- Differentiate players and bots via player join info 
- A config file for settings
  - tag bots: adding an "isBot" tag to all bots, providing an API for commands/datapacks to use
  - isCarpet: define the environment is carpet-like or not, with false value the plugin will consider all players as players, not bots
  - clean_logs: controlling whether the console returns command feedback when applying tags
- Compatibility with gnembon's carpet mod(fabric) and ishland's CarpetPlugin(bukkit)
  - You can get capet mod and CarpetPlugin here: <br>
    https://github.com/gnembon/fabric-carpet<br>
    https://github.com/ishlandbukkit/CarpetPlugin
- Current APIs  (use get_plugin_instance('player_list_api') to get the instance of this plugin)
  - get_list_all()    returns the list of all players and bots
  - get_list_player() returns the list of all players
  - get_list_bot()    returns the list of all bots, returns an empty list if no bots online or configuration 'isCarpet' is false
    
- Further improvement:<br>
[ ] add events for other plugin to use 
