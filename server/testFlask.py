#!/usr/bin/env python3
from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods=['POST'])
def result():
	print(request.form['file'] + "\t from {0}".format(request.remote_addr))
	with open('logLAN.txt', 'a') as logLANHandle:
		logLANHandle.write("{0}\t{1}".format(request.remote_addr,request.form['file']))
	logLANHandle.close()
	return 'Received !' # response to your request.

app.run(host = '192.168.178.11')
