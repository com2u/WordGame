import random

import gameData

wordToGuess = ""
def createGame1(selectedGame, games, players, socketio):
    global data  # Declare as global to modify its value
    wordList = []
    while len(wordList) < 16:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordList:
            wordList.append(word_to_append)
    secret = random.choice(wordList)
    name = "words"
    print(wordList)
    data_dict = {name: wordList}
    secrets = []
    random_index = random.randint(0, len(players) - 1)
    secrets.append(secret)
    for index, p in enumerate(players):
        if index != random_index:
            p.secretMessage = secret
            #gameData.data = gameData.replace_values(gameData.data, "Words", data_dict)
            gameData.data = gameData.replace_values(gameData.data, "Secret", secrets)
            gameData.delete_key(gameData.data, "Words")
            gameData.delete_key(gameData.data, "Exclude")
            gameData.delete_key(gameData.data, "Opponent")
            #word = next(word_cycle)
            socketio.emit(p.sessionToken,  gameData.data)
            #print(word)
        else:
            p.secretMessage = "Cameleon"
            p.secretMessage = secret
            gameData.data = gameData.replace_values(gameData.data, "Words", data_dict)
            gameData.delete_key(gameData.data, "Exclude")
            gameData.delete_key(gameData.data, "Opponent")
            gameData.delete_key(gameData.data, "Secret")
            socketio.emit(p.sessionToken, gameData.data)
    return data_dict


def CreateGame2(selectedGame, games, players):
    if (len(players) <= 3):
        return
    global data  # Declare as global to modify its value
    wordListTeam1 = []
    wordListTeam2 = []
    wordListExclude = []
    wordListNoTeam = []
    while len(wordListTeam1) < 6:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListTeam1:
            wordListTeam1.append(word_to_append)
    while len(wordListTeam2) < 6:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListTeam2:
            wordListTeam2.append(word_to_append)
    while len(wordListExclude) < 1:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListExclude:
            wordListExclude.append(word_to_append)
    while len(wordListNoTeam) < 3:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListNoTeam:
            wordListNoTeam.append(word_to_append)
    name = "words"
    allWords = wordListTeam1 + wordListTeam2 + wordListExclude + wordListNoTeam
    random.shuffle(allWords)
    print(allWords)
    data_dict = {name: allWords}
    Master1 = random.randint(0, len(players) - 1)
    print("Master1:", Master1)
    Master2 = Master1
    while (Master1 == Master2):
        Master2 = random.randint(0, len(players) - 1)
    print("Master2:", Master2)
    for index, p in enumerate(players):
        if index == Master1:
            p.secretMessage = wordListTeam1
            gameData.data = gameData.replace_values(gameData.data, "Words", wordListTeam1)
            gameData.data = gameData.replace_values(gameData.data, "Exclude", wordListExclude)
            gameData.data = gameData.replace_values(gameData.data, "Opponent", wordListTeam1)
            p.secretMessage.append("Exclude: "+wordListExclude[0])
        elif (index == Master2):
            p.secretMessage = wordListTeam2
            gameData.data = gameData.replace_values(gameData.data, "Words", wordListTeam2)
            gameData.data = gameData.replace_values(gameData.data, "Exclude", wordListExclude)
            gameData.data = gameData.replace_values(gameData.data, "Opponent", wordListTeam1)
            p.secretMessage.append("Exclude: " + wordListExclude[0])
        else:
            p.secretMessage = []
            p.secretMessage.append("Player")
            gameData.data = gameData.replace_values(gameData.data, "Words", allWords)

    return data_dict


def createGame3(selectedGame, games, players):
    global wordToGuess
    wordList = []
    wordList.append(wordToGuess)
    name = "words"
    data_dict = {name: wordList}
    wordToGuess = random.choice(games[selectedGame][0]["words"])
    for index, p in enumerate(players):
        wordList = []
        wordList.append(wordToGuess)
        wordList.append(random.choice(games[selectedGame][0]["words"]))
        wordList.append(random.choice(games[selectedGame][0]["words"]))
        random.shuffle(wordList)
        name = "words"
        data_dict = {name: wordList}
        p.secretMessage = wordList
    print(wordToGuess)
    return data_dict

def game1of3(selectedGame, games, players, json_data, socketio):

    global wordToGuess
    wordList = []
    json_dataPlayer = []
    wordList.append(wordToGuess)
    name = "words"
    data_dict = {name: wordList}
    wordToGuess = random.choice(games[selectedGame][0]["words"])
    for index, p in enumerate(players):
        wordList = []
        wordList.append(wordToGuess)
        json_dataPlayer.append(json_data)
        print(json_dataPlayer[index])

        wordList.append(random.choice(games[selectedGame][0]["words"]))
        wordList.append(random.choice(games[selectedGame][0]["words"]))
        random.shuffle(wordList)
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{token}}', p.sessionToken)
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{text1}}', wordList[0])
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{text2}}', wordList[1])
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{text3}}', wordList[2])
        p.secretMessage = str(json_dataPlayer[index])
        name = "words"
        #data_dict = {name: wordList}
        socketio.emit(p.sessionToken, str(json_dataPlayer[index]).replace('\'','"'))
        print(p.sessionToken)
        print(json_dataPlayer[index])
        #p.secretMessage = wordList
    print(wordToGuess)
    return data_dict

def CreateCodeSecret(selectedGame, games, players, json_data, socketio):
    if (len(players) <= 3):
        return
    global data  # Declare as global to modify its value
    json_dataPlayer = []
    wordListTeam1 = []
    wordListTeam2 = []
    wordListExclude = []
    wordListNoTeam = []
    print("Init CreateCodeSecret")
    while len(wordListTeam1) < 6:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListTeam1:
            wordListTeam1.append(word_to_append)
    while len(wordListTeam2) < 6:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListTeam2:
            wordListTeam2.append(word_to_append)
    while len(wordListExclude) < 1:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListExclude:
            wordListExclude.append(word_to_append)
    while len(wordListNoTeam) < 3:
        word_to_append = random.choice(games[selectedGame][0]["words"])
        if word_to_append not in wordListNoTeam:
            wordListNoTeam.append(word_to_append)
    name = "words"
    allWords = wordListTeam1 + wordListTeam2 + wordListExclude + wordListNoTeam
    random.shuffle(allWords)
    print(allWords)
    data_dict = {name: allWords}
    Master1 = random.randint(0, len(players) - 1)
    print("Master1:", Master1)
    Master2 = Master1
    while (Master1 == Master2):
        Master2 = random.randint(0, len(players) - 1)
    print("Master2:", Master2)
    for index, p in enumerate(players):
        json_dataPlayer.append(json_data)
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{token}}', p.sessionToken)
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{CardUser}}',
                                                                     "CodeSecret/card.png")
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{User}}', "User: " + players[index].name)
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{BackMaster}}',
                                                                     "CodeSecret/card.png")

        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{CardMaster1}}',
                                                                     "CodeSecret/FrontA.png")
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Master1}}',"Master: "+players[Master1].name)
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Master2}}',"Master: "+players[Master2].name)
        json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{CardMaster2}}',
                                                                     "CodeSecret/FrontB.png")

        for i, thisword in enumerate(allWords):
            json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{text' + str(i+1) + '}}', thisword)
            if ((index == Master1) or (index == Master2)):
                #print("Master")
                if (thisword in wordListTeam1):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Card' + str(i+1) + '}}',"CodeSecret/FrontA.png")
                if (thisword in wordListTeam2):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Card' + str(i+1) + '}}',"CodeSecret/FrontB.png")
                if (thisword in wordListExclude):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Card' + str(i+1) + '}}',"CodeSecret/BackX.png")
                if (thisword in wordListNoTeam):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Card' + str(i+1) + '}}',"CodeSecret/card.png")
                json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i + 1) + '}}',
                                                                             "CodeSecret/card.png")

            else:
                json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Card' + str(i+1) + '}}', "CodeSecret/card.png")
                if (thisword in wordListTeam1):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}',"CodeSecret/FrontA.png")
                if (thisword in wordListTeam2):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}',"CodeSecret/FrontB.png")
                if (thisword in wordListExclude):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}',"CodeSecret/BackX.png")
                if (thisword in wordListNoTeam):
                    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}',"CodeSecret/card.png")

                #if (thisword in wordListTeam1):
                #    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}', "CodeSecret/FrontA.png")
                #if (thisword in wordListTeam2):
                #    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}', "CodeSecret/FrontB.png")
                #if (thisword in wordListExclude):
                #    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}', "CodeSecret/BackX.png")
                #if (thisword in wordListNoTeam):
                #    json_dataPlayer[index] = str(json_dataPlayer[index]).replace('{{Back' + str(i+1) + '}}',"CodeSecret/card.png")

        p.secretMessage = str(json_dataPlayer[index])
    socketio.emit(p.sessionToken, str(json_dataPlayer[index]).replace('\'', '"'))
    # Public board
    if ((index != Master1) and (index != Master2)):
        json_data = str(json_dataPlayer[index]).replace('\'', '"')

    print("CreateCodeSecret completed")
    print(json_data)

    return data_dict, json_data
