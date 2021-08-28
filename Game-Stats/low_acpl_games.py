import berserk

#___________________________________________________________

token = "TOKEN" #Your lichess API token
user = "NAME".casefold() #User that you want top x wins of
variant = "RAPID" #One of the below, exactly as written below
#ultraBullet "bullet "blitz rapid classical correspondence chess960 crazyhouse antichess atomic horde kingOfTheHill racingKings threeCheck
num_games = 25 #Number of games you want outputted
opponent_rating_min = 0

#___________________________________________________________

session = berserk.TokenSession(token)
client = berserk.Client(session=session)

stuff = client.games.export_by_player(user, rated = "true", perf_type = variant, analysed = True, evals = True)
games = list(stuff)
acpl_list = []
opponent_list = []
game_list = []
for game in games:
    player_color = "black"
    opponent_color = "white"
    try:
        if game['players']['white']['user']['id'] == user: 
            player_color = "white"
            opponent_color = "black"

        if game['players'][opponent_color]['rating'] >= opponent_rating_min:
            acpl_list.append(game['players'][player_color]['analysis']['acpl'])
            opponent_list.append(game['players'][opponent_color]['user']['id'])
            game_list.append(game['id'])


    except:
        pass
for repetition in range(len(acpl_list)):
    
    for x in range(len(acpl_list)):
        first = int(acpl_list[repetition])
        first_user = str(opponent_list[repetition])
        first_game = str(game_list[repetition])
        if int(acpl_list[x]) < first: 
            acpl_list[repetition] = int(acpl_list[x])
            acpl_list[x] = first
            opponent_list[repetition] = opponent_list[x]
            opponent_list[x] = first_user
            game_list[repetition] = game_list[x]
            game_list[x] = first_game
try:
    for x in range(num_games):
        print(f"ACPL: {acpl_list[x]}, Opponent: {opponent_list[x]}, Game: https://lichess.org/{game_list[x]}")

except:
    pass


