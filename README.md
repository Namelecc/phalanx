# Project Phalanx

Project Phalanx is an open source set of hunting tools, meant for use on lichess. 

We believe that everyone should have access to tools if they need them. These tools provide you with macrostatistics regarding a user's games... hence, this isn't a tool for catching cheating in one game. Instead, it is a tool for catching the harder cheaters: the ones that evade the system and simply improve their play using an engine instead of cheating 100%. We call this long-term softcheating. Although lichess should in theory be able to catch these players with their tools, sometimes they don't. 

We aren't going to tell you how to use these tools. It's your job to figure that out. The only way you will be able to use these tools well is if you have explored them thoroughly, and babysitting you ultimately won't make you a good hunter. Tip: Graphs mean nothing without comparisons. We will note that it took a very long time to make and learn to use these tools, and it will take you a long time to figure them out as well. Patience and perserverence is key to understanding the complicated. In order for the tools to work, you will need to of course get python set up, as well as get the modules in requirements.txt . You will also need to fill out some of the variables at the top of the code yourself: For example, the "token" variable should be replaced with your lichess API token. Get one here: https://lichess.org/account/oauth/token

phalanx_distribution: Provides you with a graph of a persons ACPL over their past analyzed games in a given variant and time control (time control is redundant for standard chess, so make sure that both fields match when chugging standard stats). Can be restricted by opponent rating as well using the opponent_rating field.

blunder_rates.py: Blunder rates of a player in a given variant and speed (printed in console). Can be restricted by opponent rating as well using the opponent_rating field.

low_acpl_games.py: Gives a list of a player's lowest ACPL games in a given variant. The length of the list can be changed by changing num_games. Can be restricted by opponent rating as well using the opponent_rating field.

The contributions in here are not representative of actual dev team contributions: those contributions are in a private dev repo.

Lead dev: Namelecc

Main tester: ijhchess

Minor dev contributions and correspondent: erinisafox

If you want to improve the code or have an issue, please make an issue. Thanks and good luck!
