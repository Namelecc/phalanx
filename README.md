# Project Phalanx

Project Phalanx is an open source set of hunting tools, meant for use on lichess. 

DISCLAIMER: The tools here shouldn't be used as evidence in public shaming claims. Remember that the proper way to go about dealing with cheaters is to *report* them (using lichess.org/report), not to cause unecessary damage by exposing them publicly. 

We believe that everyone should have access to tools if they need them. There is a lack of publicly available cheat detection tools, and we aim to change that.

You will need to of course get python set up, as well as get the modules in requirements.txt . You will also need to fill out some of the variables at the top of the code yourself: For example, the "token" variable should be replaced with your lichess API token. Get one here: https://lichess.org/account/oauth/token

phalanx_distribution: Provides you with a graph of a persons ACPL over their past analyzed games in a given variant and time control (time control is redundant for standard chess, so make sure that both fields match when chugging standard stats). Can be restricted by opponent rating as well using the opponent_rating field. Still quite experimental. 

blunder_rates.py: Blunder rates of a player in a given variant and speed (printed in console). Can be restricted by opponent rating as well using the opponent_rating field.

low_acpl_games.py: Gives a list of a player's lowest ACPL games in a given variant. The length of the list can be changed by changing num_games. Can be restricted by opponent rating as well using the opponent_rating field.

cheat_detected_games.py: Finds all of someone's cheat detected games and gives you the game IDs.

botter_scan.py: Scans someone for botted games in a given variant and speed. Calculates a coefficient for each game based on acpl, move time standard deviation, and totalTime (a combination of starting time and increment). Lower coefficients are more suspcicious. Returns 30 lowest coefficient games. In our tests this has been quite good, and we use it regularly. 

The contributions in here are not representative of actual dev team contributions: those contributions are in a private dev repo.

Lead dev: Namelecc

Main tester: ijhchess

Correspondent and idea hatcher: erinisafox

If you want to improve the code or have an issue, please make an issue. Thanks and good luck!

Just want to shoutout another open source project that looks promising: https://github.com/erinisafox/Welgaia
