import json
import websocket

result = ""
audioPath = ""
access_token = "eyJraWQiOiIyMDIyMDYxOTE4MzciLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJpYW0tU2VydmljZUlkLTdiODcxMzBiLTFmMTItNDAyNC1hYTI4LTcyZDVmMmVhYjA3MSIsImlkIjoiaWFtLVNlcnZpY2VJZC03Yjg3MTMwYi0xZjEyLTQwMjQtYWEyOC03MmQ1ZjJlYWIwNzEiLCJyZWFsbWlkIjoiaWFtIiwianRpIjoiMjE3YmZkYzUtMGJlZi00ZTA0LTgxY2ItNTIwYjFlY2I0NDU1IiwiaWRlbnRpZmllciI6IlNlcnZpY2VJZC03Yjg3MTMwYi0xZjEyLTQwMjQtYWEyOC03MmQ1ZjJlYWIwNzEiLCJuYW1lIjoiQXV0by1nZW5lcmF0ZWQgc2VydmljZSBjcmVkZW50aWFscyIsInN1YiI6IlNlcnZpY2VJZC03Yjg3MTMwYi0xZjEyLTQwMjQtYWEyOC03MmQ1ZjJlYWIwNzEiLCJzdWJfdHlwZSI6IlNlcnZpY2VJZCIsInVuaXF1ZV9pbnN0YW5jZV9jcm5zIjpbImNybjp2MTpibHVlbWl4OnB1YmxpYzpzcGVlY2gtdG8tdGV4dDp1cy1zb3V0aDphL2Q1YWFiNzFmZGEzZTE2ZDc3NDUwZTNhYmI1YzdlMTU0OjgxYmQ4Njc3LTkzNjctNDQ5NS1iMGFjLWZkN2NjMzY0OWIxODo6Il0sImF1dGhuIjp7InN1YiI6ImlhbS1TZXJ2aWNlSWQtN2I4NzEzMGItMWYxMi00MDI0LWFhMjgtNzJkNWYyZWFiMDcxIiwiaWFtX2lkIjoiaWFtLWlhbS1TZXJ2aWNlSWQtN2I4NzEzMGItMWYxMi00MDI0LWFhMjgtNzJkNWYyZWFiMDcxIiwic3ViX3R5cGUiOiJTZXJ2aWNlSWQiLCJuYW1lIjoiQXV0by1nZW5lcmF0ZWQgc2VydmljZSBjcmVkZW50aWFscyJ9LCJhY2NvdW50Ijp7ImJvdW5kYXJ5IjoiZ2xvYmFsIiwidmFsaWQiOnRydWUsImJzcyI6ImQ1YWFiNzFmZGEzZTE2ZDc3NDUwZTNhYmI1YzdlMTU0IiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjI0MjgxNTE5LCJleHAiOjE2MjQyODUxMTksImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.aNSaco2MZVv1IBfRT-5AFY8ovVwFwPFN_jjmvM9fJbDx6xdKGuUdc24lCsB1NAP7D1cyHP_YVk1YekQze0jGg9jX77cPZPFhgSEsZs6Kb2qTJlSGZj1xpQ7OmIV7QfvUywvKT-Hj6s4uxFXOEJEHFcBNpUVeUY8Rbzm4wOZXFhqbVhvPBLFV56Ruj82-qWSSppJS5N5DVoFTpZEXn660ZYtZjwA6tOCt-ef1Le6EYAIw7NImtXX6cJmiA81sXnAT0sK5_iKIMnePwhz33gXSJb0D5c5nVhFBXzVVf0Q-2kD0abA2Q-Diqk5HUFCm5r4BqIZD0IUfarxDglcLf7xyyQ"
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

def audioToText(path):
	global audioPath
	audioPath = path
	ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
	ws.run_forever()
	return result