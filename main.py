from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import Flask, render_template, redirect, request, make_response,  url_for, send_from_directory
import gameRules
import uuid
import os
import json
from types import SimpleNamespace
import random
import html
from itertools import cycle
import time
import gameData


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
wordstoLoop = ["Haus", "Hütte", "Tür", "Tasse", "Straße", "Küsse"]
word_cycle = cycle(wordstoLoop)

players = []
secretMessages = ["Secret1", "Secret2", "Secret3", "Secret4", "Secret5",
                  "Secret1", "Secret2", "Secret3", "Secret4", "Secret5"]

selectedGame = "Game1"
json_data = []
server = "http://localhost:6767"

class Player:
    def __init__(self, name, sessionToken, secretMessage, qr_code):
        self.name = name
        self.sessionToken = sessionToken
        self.secretMessage = secretMessage
        self.qr_code = qr_code


def send_words():
    print("Send Words")

    while True:
        word = next(word_cycle)
        socketio.emit('new_word', {'word': word})
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    global data  # Declare as global to modify its value
    print("OnConnect!")
    socketio.emit('display_data', gameData.data)




@app.route("/")
def index():
    return redirect("/setup")


@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        name = request.form.get("name")
        if name:  # If a new player is being added
            #sessionToken = base64.b64encode(os.urandom(24)).decode("utf-8")
            sessionToken = str(uuid.uuid4())
            secretMessage = secretMessages[len(players) % len(secretMessages)]
            qr_code = gameData.generate_qr_code(f"{server}/player/{sessionToken}")
            players.append(Player(name, sessionToken, secretMessage, qr_code))
            print("Create:", sessionToken)  # Debugging line
        else:  # If a player is being removed
            token_to_remove = request.form.get("remove")
            if token_to_remove:
                print("Remove:", token_to_remove)  # Debugging line
                players[:] = [p for p in players if p.sessionToken != token_to_remove]

    return render_template("setup.html", players=players, server=server)



@app.route('/<path:path>')
def serve_static_files(path):
    print("Path:")
    print(path)
    path = path.replace('player/','')
    print(path)
    return send_from_directory(app.static_folder, path)


@app.route("/player/<token>")
def player(token):
    global json_data
    print("Token:")
    print(token)

    for index, p in enumerate(players):
        if p.sessionToken == token:
            if (selectedGame == "Game1"):
                return render_template("player.html", player=p, player_number=index + 1)
                word = next(word_cycle)
                socketio.emit(p.sessionToken, {'word': word})
                return
            if (selectedGame == "Game2"):
                return render_template("playerList.html", player=p, player_number=index + 1)
            if (selectedGame == "Game3"):
                return render_template("playerList.html", player=p, player_number=index + 1)
            if (selectedGame == "Game4"):
                json_data = p.secretMessage
                #return render_template("playerList.html", player=p, player_number=index + 1)
                return send_from_directory(app.static_folder, 'playerBoard.html')
            if (selectedGame == "Game10"):
                json_data = p.secretMessage
                #return render_template("playerList.html", player=p, player_number=index + 1)
                return send_from_directory(app.static_folder, 'playerBoard.html')


            ## All other games
            return send_from_directory(app.static_folder, 'board.html')

    if (token == "script.js"):
        print("script.js")
        print(json_data)
        return render_template("script.js", data=json_data)
    if (token == "playerScript.js"):
        print("playerScript.js")
        print(json_data)
        return render_template("playerScript.js", data=json_data)

    return send_from_directory(app.static_folder, token)

    return "Player not found!"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        if name:  # if a new player is being registered
            sessionToken = str(uuid.uuid4())
            secretMessage = secretMessages[len(players) % len(secretMessages)]
            qr_code = gameData.generate_qr_code(f"{server}/player/{sessionToken}")
            players.append(Player(name, sessionToken, secretMessage, qr_code))
            return redirect(url_for("player", token=sessionToken))  # redirect to the new player's page

    return render_template("register.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    global selectedGame  # Declare as global to modify its value
    global json_data

    if request.method == "POST":
        selectedGame = request.form.get("new_game")
        print("New game:", selectedGame)  # Debugging line

    game_data = games.get(selectedGame)[0]  # Assume that there is always at least one game in each category
    print("Selected game:",selectedGame)
    if (selectedGame == "Game1"):
        data_dict = gameRules.createGame1(selectedGame, games, players, socketio)
        return render_template("game.html", game=game_data, all_games=games, current_game=selectedGame,
                               content=data_dict)
    if (selectedGame == "Game2"):
        data_dict = gameRules.CreateGame2(selectedGame, games, players)
        return render_template("game2.html", game=game_data , all_games=games, current_game=selectedGame, content=data_dict)
    if (selectedGame == "Game3"):
        data_dict = gameRules.createGame3(selectedGame, games, players, socketio=socketio)
        return render_template("game.html", game=game_data, all_games=games, current_game=selectedGame,
                               content=data_dict)
    if (selectedGame == "Game4"):
        loadGame(games[selectedGame][0]["gameTitle"])
        print("Game4")
        print(json_data)
        data_dict = gameRules.game1of3(selectedGame, games, players,json_data, socketio)
        return render_template("game.html", game=game_data, all_games=games, current_game=selectedGame,
                               content=data_dict)
    if (selectedGame == "Game10"):
        loadGame(games[selectedGame][0]["gameTitle"])
        print("Game10")
        print(json_data)
        data_dict, json_data = gameRules.CreateCodeSecret(selectedGame, games, players,json_data, socketio)
        print(json_data)

        return render_template("gameBoard.html", game=game_data, all_games=games, current_game=selectedGame,
                               content=data_dict)

    #if (selectedGame == "Game4"):
    loadGame(games[selectedGame][0]["gameTitle"])
    #json_data = gameRules.createGame(selectedGame, games, players, json_data)
    return render_template("gameBoard.html", game=game_data, all_games=games, current_game=selectedGame, content=json_data)
        ##return send_from_directory(app.static_folder, 'board.html')


@app.route("/script.js")
def script():
    print("Script Loaded")
    return render_template("script.js", data=json_data)


@socketio.on('connect')
def handle_connect():
    global json_data
    # Senden der aktuellen JSON-Struktur an den gerade verbundenen Client
    emit('initial_data', json_data)
    print("WS Connect json data")
    print(json_data)

@socketio.on('update_data')
def handle_update_data(updated_json_data):
    global json_data  # Verweisen auf die globale Variable
    json_data = updated_json_data  # Aktualisieren der gespeicherten JSON-Struktur
    # Daten an alle Clients senden, außer an den Sender
    emit('refresh_data', json_data, broadcast=True, include_self=False)
    print("WS update json data")
    print(json_data)

def loadGame(name):
    global json_data
    print("JSON Loaded")
    print(name)

    with open(name+".json", encoding='utf-8') as f:
        json_data = json.load(f)

if __name__ == "__main__":
    # Load games data from JSON file
    with open("games.json", encoding='utf-8') as f:
        games = json.load(f)
        wordToGuess = random.choice(games[selectedGame][0]["words"])
    loadGame("game")
    gameData.generate_register_qr_code(server)
    socketio.start_background_task(send_words)
    socketio.run(app,  host='0.0.0.0', port=6767, debug=True, allow_unsafe_werkzeug=True)



