import subprocess
import re
import json
import imp
import all_the_games
import time
import msvcrt
import sys

def initiateGamesList():
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
            if result[-1] == '\r':   #XXX check what Windows returns here
                return ''.join(result[:-1])
        time.sleep(0.04) # just to yield to other processes/threads
    return ""
			
if __name__ == "__main__":
	command = ""
	while not(command == "quit"):
		fileToSend = open("info.txt","w")		
		tasksByte = subprocess.check_output("tasklist")
		tasks = tasksByte.decode("utf-8").split("\r\n")
		#tasks_handle = open("example.txt", "r")
		#tasks = tasks_handle.readlines()

		exeList = initiateGamesList()
		## get to the outpur line that is  only ===== === ==
		tabGaps = [tabGap.start() for tabGap in re.finditer(" ",tasks[2])] 
		#ending index of Name, IDm sessionName, Sessionnr, memoryUsage

		for process in tasks:
			processName = process[:tabGaps[0]].strip() #remove whitspace at the end
			gameName = exeList.get(processName, False)
			if gameName:
		#		fileToSend.write(gameName)
				print("Now playing {0}".format(gameName))
		
		print("not playing any games")
		command = listenForCommands("type quit to cancel\n", 90)
				
				
