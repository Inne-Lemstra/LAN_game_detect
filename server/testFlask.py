#!/usr/bin/env python3
from flask import Flask, request, render_template
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
    

# GOD please dont hate me for using a global variable
# This should be a front-end to a database or something
lastPlayed = {} # ip-addr -> string
def sawPlayerPlay(player, game):
    lastPlayed[player] = game

def getLastPlayed():
    # Copy for thread-safety
    return lastPlayed.copy()



app.run(host = '192.168.178.11')


