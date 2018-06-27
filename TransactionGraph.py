import json
import requests
import subprocess

def getAddress(rawTransaction, outputIndex):
	tx = json.loads(rawTransaction)
	if tx['vout'][outputIndex]['scriptPubKey']['type']=="pubkeyhash":
		return tx['vout'][outputIndex]['scriptPubKey']['addresses'][0]
	else:
		return None

def getBlockSets(blockHash):
	s='http://localhost:8332/rest/block/'+blockHash+'.json'
	myDict = requests.get(s).json()
	jStr = json.dumps(myDict)
	block = json.loads(jStr)

	listOfSetsInBlock = []

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
		listOfSetsInBlock.append(A)
		print(i)
		i=i+1
	print("Done")
	return listOfSetsInBlock
		

listOfSets = []

start_block = int(input("Enter start block"))
end_block = int(input("Enter end block"))
block_hashes = []
command = "bitcoin-cli"

for x in range(start_block, end_block):
	result = subprocess.run([command, 'getblockhash', str(x)], stdout=subprocess.PIPE)
	block_hashes.append(result.stdout.decode()[:-1])

print("Got all block hashes. Now starting to get address")

for blkhash in block_hashes:
	listOfSets.append(getBlockSets(blkhash))

print("Got the sets of individual transactions. Now widening the entities.")

for u in listOfSets:
	for address in u:
		for v in listOfSets:
			if address in v:
				u = u.union(v)
				listOfSets.remove(v)

print("Done with all the processing. Now starting to print the results.")

for u in listOfSets:
	print(u)
