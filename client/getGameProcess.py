import subprocess
import re
import json
import imp
import all_the_games
from threading import Timer

def initiateGamesList(gamesListFilePath = "something"):
	imp.reload(all_the_games)
	gameList = all_the_games.initiate() 
	exeList = []
# 	make a list of tuples, tuple contains (exeName, gameName)	
	for game in gameList:
		exes = game["executables"].get("win32", False)
#		exes = [[exe, game.get("name", "unknown")]for exe in exes]
		
		if exes:
			exesAndNames = [(exe, game.get("name", "unknown"))\
							for exe in exes]
			exeList = exeList + exesAndNames
	
	exeDict = {i[0]:i[1]for i in exeList}
	return exeDict

def listenForCommands(timeOut = 60):
	timeWindow = Timer(timeOut, print, ["Wait a minute, refreshing tasklist"])
	command =  False
	timeWindow.start()
	command = input("Input command now: (type help to see options)\n")
	timeWindow.cancel()
	return command
			
if __name__ == "__main__":
	fileToSend = open("info.txt","w")		
	tasksByte = subprocess.check_output("tasklist")
	tasks = tasksByte.decode("utf-8").split("\r\n")
	#tasks_handle = open("example.txt", "r")
	#tasks = tasks_handle.readlines()


	## get to the outpur line that is  only ===== === ==
	tabGaps = [tabGap.start() for tabGap in re.finditer(" ",tasks[2])] 
	#ending index of Name, IDm sessionName, Sessionnr, memoryUsage

		

	for process in tasks:
		processName = process[:tabGaps[0]].strip() #remove whitspace at the end
		gameName = exeList.get(processName, False)
		if gameName:
	#		fileToSend.write(gameName)
			print("Now playing {0}".format(gameName))

