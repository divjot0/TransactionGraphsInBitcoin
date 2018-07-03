import json
import requests
import subprocess

def edges(blockHash, listOfTxs):
	s='http://localhost:8332/rest/block/'+blockHash+'.json'
	myDict = requests.get(s).json()
	jStr = json.dumps(myDict)
	block = json.loads(jStr)

	E = []
	for transaction in block['tx']:
		for inputTransaction in transaction['vin']:
			if 'txid' in inputTransaction:
				if inputTransaction['txid'] in listOfTxs:
					E.append(inputTransaction['txid'], transaction['txid'])
					"""
						From-To Relationship
					"""
	print("Done with a block")
	return E


def getBlockTxs(blockHash):
	s='http://localhost:8332/rest/block/'+blockHash+'.json'
	myDict = requests.get(s).json()
	jStr = json.dumps(myDict)
	block = json.loads(jStr)

	listOfTxsInBlock = []

	for transaction in block['tx']:
		listOfTxsInBlock.append(transaction['txid'])
	print("Done with a block")
	return listOfTxsInBlock


start_block = int(input())
end_block = int(input())
block_hashes = []
command = "bitcoin-cli"

for x in range(start_block, end_block):
	result = subprocess.run([command, 'getblockhash', str(x)], stdout=subprocess.PIPE)
	block_hashes.append(result.stdout.decode()[:-1])

listOfTxs = []
listOfEdges = []

print("Got all block hashes. Now starting to get address")

for blkhash in block_hashes:
	listOfTxs.append(getBlockTxs(blkhash))

for blkhash in block_hashes:
	listOfEdges.append(edges(blkhash, listOfTxs))