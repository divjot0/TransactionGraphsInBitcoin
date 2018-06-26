import json
import requests
import subprocess

def getAddress(rawTransaction, outputIndex):
	tx = json.loads(rawTransaction)
	if tx['vout'][outputIndex]['scriptPubKey']['type']=="pubkeyhash":
		return tx['vout'][outputIndex]['scriptPubKey']['addresses'][0]
	else:
		return None


myDict = requests.get('http://localhost:8332/rest/block/0000000000000832e0f70b86d818755ab0aef51541e1f2bbe5146784daaa517c.json').json()
jStr = json.dumps(myDict)
block = json.loads(jStr)

listOfSets = []

for transaction in block['tx']:
	A = set([])
	for inputTransaction in transaction['vin']:
		if 'txid' in inputTransaction:
			result = subprocess.run(["bitcoin-cli", "getrawtransaction", str(inputTransaction['txid']), "1"], stdout=subprocess.PIPE)
			a = result.stdout.decode()
			r = getAddress(a, inputTransaction['vout'])
			print(r)
			if r!=None:
				A.add(r)
				print(r)
		else:
			print("Coinbase")
	listOfSets.append(A)
	print ("\nnext transaction")


for u in listOfSets:
	print (u)
	print ("\n\n\n\n")

"""REMOVE YOUR ID AND PASSWORD"""