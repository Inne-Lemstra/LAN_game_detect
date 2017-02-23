from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods=['POST'])
def result():
	print(request.form['file'])
	with open('logLAN.txt', 'a') as logLANHandle:
		logLANHandle.write("{0}\t{1}".format(request.remote_addr,request.form['file']))
	logLANHandle.close()
	return 'Received !' # response to your request.

app.run(debug = True)