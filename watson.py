import json
import websocket

result = ""
audioPath = ""
access_token = "eyJraWQiOiIyMDIxMDYxOTE4MzciLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJpYW0tU2VydmljZUlkLTdiODcxMzBiLTFmMTItNDAyNC1hYTI4LTcyZDVmMmVhYjA3MSIsImlkIjoiaWFtLVNlcnZpY2VJZC03Yjg3MTMwYi0xZjEyLTQwMjQtYWEyOC03MmQ1ZjJlYWIwNzEiLCJyZWFsbWlkIjoiaWFtIiwianRpIjoiN2E1YTgwNTctOWU0YS00NTNhLWJiNjctNzkyNDNmZmI2YjQ3IiwiaWRlbnRpZmllciI6IlNlcnZpY2VJZC03Yjg3MTMwYi0xZjEyLTQwMjQtYWEyOC03MmQ1ZjJlYWIwNzEiLCJuYW1lIjoiQXV0by1nZW5lcmF0ZWQgc2VydmljZSBjcmVkZW50aWFscyIsInN1YiI6IlNlcnZpY2VJZC03Yjg3MTMwYi0xZjEyLTQwMjQtYWEyOC03MmQ1ZjJlYWIwNzEiLCJzdWJfdHlwZSI6IlNlcnZpY2VJZCIsInVuaXF1ZV9pbnN0YW5jZV9jcm5zIjpbImNybjp2MTpibHVlbWl4OnB1YmxpYzpzcGVlY2gtdG8tdGV4dDp1cy1zb3V0aDphL2Q1YWFiNzFmZGEzZTE2ZDc3NDUwZTNhYmI1YzdlMTU0OjgxYmQ4Njc3LTkzNjctNDQ5NS1iMGFjLWZkN2NjMzY0OWIxODo6Il0sImF1dGhuIjp7InN1YiI6ImlhbS1TZXJ2aWNlSWQtN2I4NzEzMGItMWYxMi00MDI0LWFhMjgtNzJkNWYyZWFiMDcxIiwiaWFtX2lkIjoiaWFtLWlhbS1TZXJ2aWNlSWQtN2I4NzEzMGItMWYxMi00MDI0LWFhMjgtNzJkNWYyZWFiMDcxIiwic3ViX3R5cGUiOiJTZXJ2aWNlSWQiLCJuYW1lIjoiQXV0by1nZW5lcmF0ZWQgc2VydmljZSBjcmVkZW50aWFscyJ9LCJhY2NvdW50Ijp7ImJvdW5kYXJ5IjoiZ2xvYmFsIiwidmFsaWQiOnRydWUsImJzcyI6ImQ1YWFiNzFmZGEzZTE2ZDc3NDUwZTNhYmI1YzdlMTU0IiwiZnJvemVuIjp0cnVlfSwiaWF0IjoxNjI0Mjg0MDY1LCJleHAiOjE2MjQyODc2NjUsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.MFls6SUCMjlK3LUMjfrKtgymYn33bUDIzwq4YUxP5t6oXkth5LQxnr8uEUhPaloiDgRCZUFjDNnv4F1Lpzr2QYjfREKE1ibH-IQ27SriJ5GU7qNAwHQAF9-8J2jGYOd094NILQwmV1ir4ly6cbhRB_PJq_gu8fyw2kr_SeobWxjzp4L7KAbyEPYPb9pFbTRO9izwtz4IBGM84MkPfKmPrHBTxA9zw0W6hHsegRWh7wZaugef0CcIRgA6fC1x4dlEpX1Vj8nluv4OcmzXDKOa5pjpLC-CDSJrlH8Cf7KkR-1E2QdTxKmtFBYoZ8BvE-zI6hhD1Wq7ZKlPzCG_Yqkxlw"
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