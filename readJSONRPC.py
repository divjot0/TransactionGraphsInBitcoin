import json
import requests

myDict = requests.get('http://localhost:8332/rest/block/0000000000000832e0f70b86d818755ab0aef51541e1f2bbe5146784daaa517c.json').json()
jStr = json.dumps(myDict)
block = json.loads(jStr)

for transaction in block['tx']:
	for inputTransaction in transaction['vin']:
		if 'txid' in inputTransaction:
			print(str(inputTransaction['txid']) + " " + str(inputTransaction['vout']))
		else:
			print("Coinbase")
	print ("\nnext block")
