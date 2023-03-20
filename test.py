import json

outgoing_msg = {"probability": [[1, 2, 3]], "mood": 'ok',}

res = json.dumps(outgoing_msg)
print(res)
