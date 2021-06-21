import json
import websocket

result = ""
audioPath = ""
access_token = ""
url = "wss://api.us-south.speech-to-text.watson.cloud.ibm.com/v1/recognize?access_token=" + access_token

def on_open(ws):
	print("WebSocket connection established")
	# Start
	ws.send(json.dumps({
		"timestamps": True,
		"content-type": "audio/mp3",
		"interim_results": True,
		"keywords": [
			"IBM",
			"admired",
			"AI",
			"transformations",
			"cognitive",
			"Artificial Intelligence",
			"data",
			"predict",
			"learn"
		],
		"keywords_threshold": 0.01,
		"word_alternatives_threshold": 0.01,
		"smart_formatting": True,
		"speaker_labels": False,
		"action": "start"
	}))
	# Send audio data
	with open(audioPath, mode='rb') as f:
		audio = f.read()
	ws.send(audio, websocket.ABNF.OPCODE_BINARY)
	print("Audio sent")
	# Stop
	ws.send(json.dumps({"action": "stop"}))

def on_message(ws, message):
	data = json.loads(message)

	if data["results"][0]["final"]:
		global result
		result = data["results"][0]["alternatives"][0]["transcript"]
		print("Result: " + result)
		# This is an error...
		ws.close()

def on_error(ws, error):
    print('Websocket Error: ' + str(error))

def on_close(ws):
    print('Websocket closed')

def get_token():
	global access_token
	
def audioToText(path):
	global audioPath
	audioPath = path
	get_token()
	ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
	ws.run_forever()
	return result