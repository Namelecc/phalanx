import requests as req
import json
import statistics as stat

#__________________________

username = input("Username: ").casefold()
move_minimums = 10
variant = input("Variant: ")
speed = input("Speed: ")
min_opponent = int(input("Minimum opponent rating: "))
#These are all inputs

#__________________________

url = f"https://lichess.org/api/games/user/{username}"
request = req.get(
    url,
    params={"rated":"true", "perfType":variant, "analysed":"true", "pgnInJson":"true", "clocks":"true","evals":"True"},
    # "max":x where x is any number you choose is a possible inclusion above if you want
    headers={"Accept": "application/x-ndjson"}
)
#Using request module to get the endpoint from the API
#__________________________

stuff = request.iter_lines() #This is going to allow us to read ndjson as json
more_stuff = list(stuff)

coefficient = [] #Lists that we will use later
games = [] 

for x in more_stuff:
    game = json.loads(x) #Since the game itself is json compatible, we can read it
    try: #If the game is old, keys might not exist causing errors so we just try-except those games
        if game['speed'] == speed: 
            initial = game['clock']['initial'] 
            increment = game['clock']['increment']
            berserk = False #We are first going to assume no berserk, will check it later

            #__________________________

            player_color = ""
            opponent_color = ""
            if game['players']['white']['user']['id'] == username.casefold():
                player_color = "white"
                opponent_color = "black"
            else:
                player_color = "black"
                opponent_color = "white"
            #This whole section is just finding out which color our player is
            #__________________________

            if game['players'][opponent_color]['rating'] >= min_opponent: #Checking the minimum rating filter
                acpl = game["players"][player_color]["analysis"]["acpl"]
                if acpl < 5:
                    acpl = 5 #Because in variants such as rk, 0 acpl basically negates the effect of standard dev

                pgn = game["pgn"]

                #__________________________
                clock = []
                clock_reader = []
                pgn = pgn.split("[")
                for y in pgn:
                    if "clk" in y:            
                        clock.append(y[6:12].strip(":"))
                for x in range(0, len(clock)):
                    if player_color == "white":
                        if x % 2 == 0:
                            clock_reader.append(clock[x])
                    else:
                        if x % 2 == 1:
                            clock_reader.append(clock[x])
                move_times = []
                for x in range(0, len(clock_reader)):
                    y = clock_reader[x].split(":")
                    seconds = int(y[0]) * 60 + int(y[1]) 
                    clock_reader[x] = seconds

                #This whole part is just reading clock times out of the pgn format
                #__________________________


                if clock_reader[0] != initial and initial != 0: 
                    #If the game time control isn't the same as the starting time, then the player has berserked
                    #This of course isn't true for 0 + x time controls, which is why we exclude those (and they can't be berserked either)
                    berserk = True

                if berserk == False:
                    #__________________________
                    clock_reader.insert(0, initial) 
                    for x in range(1, len(clock_reader)):
                        move_times.append(clock_reader[x-1] - clock_reader[x] + increment)
                    #Turning clock times into move times
                    #__________________________

                    if len(move_times) >= move_minimums: #Move minimum is defined at the top... goal is to not count super short games
                        stdev = stat.stdev(move_times) #This is our measure of spread
                        acpl_dev = acpl * stdev / (game["clock"]["totalTime"]) #This is a combination of spread and accuracy. Read the doc to understand it
                        coefficient.append(acpl_dev) 
                        games.append(game["id"])
                else: 
                    #__________________________
                    clock_reader.insert(0, initial/2) #Since the game is berserked, we will half initial time
                    for x in range(1, len(clock_reader)):
                        move_times.append(clock_reader[x-1] - clock_reader[x])
                    #Turning clock times into move times
                    #__________________________

                    if len(move_times) >= move_minimums: #Move minimum is defined at the top... goal is to not count super short games
                        stdev = stat.stdev(move_times) #This is our measure of spread
                        acpl_dev = acpl * stdev / (initial/2) #This is a combination of spread and accuracy. Read the doc to understand it
                        coefficient.append(acpl_dev)
                        games.append(game["id"])
    except:
        pass #If the API can't fetch all the data necessay from the old games we just ignore them
#__________________________

for repetition in range(len(games)):
    for x in range(len(games)):
        first = coefficient[repetition]
        if coefficient[x] > first: 
            coefficient[repetition] = coefficient[x]
            coefficient[x] = first
            first_game = games[repetition]
            games[repetition] = games[x]
            games[x] = first_game
#Simple sort algorithm, I'm not using sort() because I need to sort 2 lists concurrently 
#__________________________

for x in range(0, 30): #Just giving the top 30 suspicious games
    try: 
        print(f"Game: https://lichess.org/{games[x]}, Coefficient: {coefficient[x]}")
    except:
        pass
        #We may get an array out of bounds error if the player has very few games

#As mentioned earlier, to understand the logic behind this code, please read the doc in the folder.

