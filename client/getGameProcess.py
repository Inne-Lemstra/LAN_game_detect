#(c) Inne Lemstra 21-02-2017 
import subprocess
import re
import json
import imp
import time
import msvcrt
import sys
import os

def loadJsonGameList(gameListPath):
	with open(gameListPath, "r", encoding='utf-8-sig') as gameListHandle:
		gameListString = gameListHandle.read()
	gameListHandle.close()
	return json.loads(gameListString)



def initiateGamesList():
	gameList = loadJsonGameList("./all_the_games.txt")
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
	return (exeDict, gameList)

class TimeoutExpired(Exception):
    pass

def listenForCommands(prompt, timeout, timer=time.monotonic):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout
    result = []
    while timer() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche()) #XXX can it block on multibyte characters?
            if result[-1] == '\r':   #XXX check what Windows returns here (it is \r)
                return ''.join(result[:-1])
        time.sleep(0.04) # just to yield to other processes/threads
    return ""

def help():
	"""Print documentation to screen, so user can see what all the availible commands do"""
	print("this is going to be a help function")	

def add(exeDict, gameListJson):
	"""Add a exeName and GameName dictionary to all_the_games so program can recognize games not in the list"""
	exeName = input("enter exe name or q to cancel")
	if exeName == "q": break
	gameName = input("enter game name (use UPPER case for every seperate word) or q to cancel")
	if gameName == "q": break
	errata = {"executables": {"win32": [exeName]},"id": gameListJson[-1]["id"] + 1, "name": gameName}
	gameListJson.append(errata)
	with open("all_the_games.txt", "r") as gameListHandle:
		gameListHandle.write(json.dumps(gameListJson, indent = 4))
	gameListHandle.close()
	exeDict[exeName] = gameName
	return (exeList, gameListJson)
	
	
	

if __name__ == "__main__":
	command = ""
	availibleCommands = ["add", "help"]
	while not(command == "quit"):
		fileToSend = open("info.txt","a")		
		tasksByte = subprocess.check_output("tasklist")
		tasks = tasksByte.decode("utf-8").split("\r\n")
		#tasks_handle = open("example.txt", "r")
		#tasks = tasks_handle.readlines()

		(exeList, gamesListJson) = initiateGamesList()
		## get to the outpur line that is  only ===== === ==
		tabGaps = [tabGap.start() for tabGap in re.finditer(" ",tasks[2])] 
		#ending index of Name, ID, sessionName, Sessionnr, memoryUsage
		currentlyPlaying = False
		
		for process in tasks:
			processName = process[:tabGaps[0]].strip() #remove whitspace at the end
			gameName = exeList.get(processName, False)
			if gameName:
				fileToSend.write("{0}\t{1}\n".format(gameName, int(time.time())))
				print("Now playing {0}".format(gameName))
				currentlyPlaying = True
		
		if not(currentlyPlaying): print("Not playing any games")
		command = listenForCommands("type quit to stop program\n", 10)
		if command in availibleCommands:
			pass
	fileToSend.close()
	print("goodbye")
				
				
