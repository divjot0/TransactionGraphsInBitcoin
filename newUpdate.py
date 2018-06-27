import json
import requests
import subprocess

def getAddress(rawTransaction, outputIndex):
	tx = json.loads(rawTransaction)
	if tx['vout'][outputIndex]['scriptPubKey']['type']=="pubkeyhash":
		return tx['vout'][outputIndex]['scriptPubKey']['addresses'][0]
	else:
		return None

""" Checks for same sets
	Combining and deleting sets
	Test for largest"""
		


myDict = requests.get('http://localhost:8332/rest/block/0000000000000832e0f70b86d818755ab0aef51541e1f2bbe5146784daaa517c.json').json()
jStr = json.dumps(myDict)
block = json.loads(jStr)

listOfSets = []

i=1
for transaction in block['tx']:
	A = set([])
	for inputTransaction in transaction['vin']:
		if 'txid' in inputTransaction:
			result = subprocess.run(["bitcoin-cli", "getrawtransaction", str(inputTransaction['txid']), "1"], stdout=subprocess.PIPE)
			a = result.stdout.decode()
			r = getAddress(a, inputTransaction['vout'])
			if r!=None:
				if r not in A:
					A.add(r)
	listOfSets.append(A)
	print(i)
	i=i+1
print("Done")


for u in listOfSets:
	for address in u:
		for v in listOfSets:
			if address in v:
				u = u.union(v)
				listOfSets.remove(v)

for u in listOfSets:
	print(u)

"""REMOVE YOUR ID AND PASSWORD"""
