#!/usr/bin/env python3
#(c) Inne Lemstra & Bart Marinissen 24-02-2017
from flask import Flask, request, render_template
import time
app = Flask(__name__)
@app.route('/', methods=['POST'])
def result():
    with open('logLAN.txt', 'a') as logLANHandle:
    	logLANHandle.write("{0}\t{1}".format(request.remote_addr,request.form['file']))
    logLANHandle.close()

    sawPlayerPlay(request.remote_addr, request.form['file'])

    return 'Received !' # response to your request.

@app.route('/whoIsPlaying')
def currentlyPlayingPage():
    lastPlayed = getLastPlayed()
    return render_template('lastPlayed.html', lastPlayed=lastPlayed)
    

@app.route('/whatIsPlayed')
def currentGamesPage():
    lastPlayed = getLastPlayed()
    playedRightNow = parseGames(lastPlayed)
    return render_template('currentGames.html', playedRightNow = playedRightNow)

# GOD please dont hate me for using a global variable
# This should be a front-end to a database or something
lastPlayed = {} # ip-addr -> string
def sawPlayerPlay(player, game):
    lastPlayed[player] = game

def getLastPlayed():
    # Copy for thread-safety
    return lastPlayed.copy()

def parseGames(lastPlayed = lastPlayed):
    """parsing the data recieved into dictionary of number of people playing which games currently."""
    gamesPlayedNow = {}
    for ip in lastPlayed.keys():
        data = lastPlayed[ip].strip() #remove \n at the end
        games = data.split("\t")[:-1]
        timestamp = int(data.split("\t")[-1])
        if int(time.time()) - timestamp > 60:
            #check if data is older then 60 seconds if so don't count this data
            #(clients have 45 seconds update rate)
            continue
        for game in games:
            gamesPlayedNow[game] = gamesPlayedNow.get(game, 0) + 1
    return gamesPlayedNow


app.run(host = '192.168.178.11')
    

