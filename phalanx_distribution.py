import berserk
import matplotlib.pyplot as plt
import numpy as np

#___________________________________________________________

token = "TOKEN" #Your lichess API token
user = "NAME".casefold() #User that you want top x wins of
variant = "VARIANT" #One of the below, exactly as written below
#ultraBullet "bullet "blitz rapid classical correspondence chess960 crazyhouse antichess atomic horde kingOfTheHill racingKings threeCheck
speed = "SPEED" #One of the below, exactly as written
#blitz bullet classical rapid correspondence 
min_opponent_rating = 0
#blitz, bullet, rapid, correspondence
overflowbucket = 300 #threshold for overflow bucket
barlength = 5 #bin width

#___________________________________________________________
session = berserk.TokenSession(token)
client = berserk.Client(session=session)

stuff = client.games.export_by_player(user, as_pgn = False, rated = "true", max = 100, perf_type = variant, analysed = True, evals = True)
games = list(stuff)

gamecount = 0
numbars = overflowbucket // barlength + 1 #the +1 is for an overflow bucket
frequencies = [0]*numbars
acpl_stats = []

for game in games:
    if game: #checks if game dictionary is empty 
        if game['speed'] == speed:
            player_color = "black"
            opponent_color = "white"
            try:
                if game['players']['white']['user']['id'] == user: 
                    player_color = "white"
                    opponent_color = "black"
                
                if game['players'][opponent_color]['rating'] >= min_opponent_rating:
                    acpl = game['players'][player_color]['analysis']['acpl']
                    acpl_stats.append(acpl)
                    temp = acpl // barlength
                    if temp >= len(frequencies):
                        temp = len(frequencies)-1
                    frequencies[temp] += 1
                    gamecount += 1 
            except:
                pass #If rated isn't turned to true, you might encounter games against lichess's AI, which has no rating variable. This just weeds those out


fig = plt.figure()
acpls = [f'{x}' for x in zip(range(0, overflowbucket, barlength))]
acpls.append(f'   {str(overflowbucket)}++') #add overflow bucket labelprint(acpls)

for x in range(0, len(acpls)):
    acpls[x] = str(acpls[x]).strip(",()")
    
x_ticks = np.arange(0, overflowbucket, 5)
plt.xticks(x_ticks)

plt.bar(acpls,frequencies)
plt.xlabel('ACPL')
plt.ylabel('Number of games')
if variant != ("blitz" or "rapid" or "classical" or "bullet"):  
    plt.suptitle(f"{user} in {variant} over {gamecount} {speed} games")
else:
    plt.suptitle(f"{user} in {variant} over {gamecount} games")
mean = round(sum(acpl_stats)/len(acpl_stats), 2)
median = 0
for repetition in range(len(acpl_stats)):
    for x in range(len(acpl_stats)):
        first = int(acpl_stats[repetition])
        if int(acpl_stats[x]) > first: 
            acpl_stats[repetition] = int(acpl_stats[x])
            acpl_stats[x] = first
if len(acpl_stats) % 2 == 1:
    median = round(acpl_stats[int((len(acpl_stats) + 1)/2)], 2)
else:
    median = round((acpl_stats[int(len(acpl_stats) /2)] + acpl_stats[int(len(acpl_stats)/2) + 1])/2, 2)
if min_opponent_rating == 0:
    plt.title(f"Mean: {mean}, Median: {median}")
else:
    plt.title(f"Mean: {mean}, Median: {median}, Min Opponent Rating: {min_opponent_rating}")

plt.show()
