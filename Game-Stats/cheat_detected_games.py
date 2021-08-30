import berserk
user = "USERNAME"
token = "TOKEN"

session = berserk.TokenSession(token)
client = berserk.Client(session=session)

games = client.games.export_by_player(user, max = 10981)
for game in games:
    if game['status'] == "cheat":
        
        if game['players']['white']['user']['id'] == user.casefold():
            player_color = "white"
        else:
            player_color = "black"
                
        if game['winner'] != player_color:
            print(game['id'])
