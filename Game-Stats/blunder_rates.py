import berserk

#___________________________________________________________

token = "TOKEN" #Your lichess API token
user = "NAME".casefold() #User that you want top x wins of

variant = "VARIANT" #One of the below, exactly as written below
#ultraBullet "bullet "blitz rapid classical correspondence chess960 crazyhouse antichess atomic horde kingOfTheHill racingKings threeCheck

speed = "SPEED" #One of the below, exactly as written
#blitz, bullet, rapid, correspondence

min_opponent_rating = 0

#___________________________________________________________


session = berserk.TokenSession(token)
client = berserk.Client(session=session)

stuff = client.games.export_by_player(user, rated = "true", perf_type = variant, analysed = True, evals = True)

games = list(stuff)
total_blunders = 0
total_moves = 0
game_count = 0
for game in games:
    if game:
        if game['speed'] == speed:
            player_color = "black"
            opponent_color = "white"       
            if game['players']['white']['user']['id'] == user: 
                player_color = "white"
                opponent_color = "black"
            if game['players'][opponent_color]['rating'] >= min_opponent_rating:
                moves = game['moves'].split()
                white_turn = False
                white_moves = 0
                black_moves = 0
                for move in moves:
                    white_turn = not white_turn
                if white_turn == True:
                    white_moves = int((len(moves)-1)/2 + 1 )
                    black_moves = len(moves) - white_moves
                else:
                    white_moves = int(len(moves)/2)
                    black_moves = white_moves
                if player_color == "white":
                    total_moves += white_moves
                else:
                    total_moves += black_moves
                game_count = game_count + 1 
                #print(game_count)
            


        try:
            total_blunders += (game['players'][player_color]['analysis']['blunder'])
        except:
            print("Some stupid error...")

print(f"User: {user}, Total blunders to total moves ratio: {round(total_blunders/total_moves, 3)}, Total blunders to total games ratio: {round(total_blunders/game_count,3)}, Games: {game_count}, Time control: {speed}, Min Opponent Rating: {min_opponent_rating}")



