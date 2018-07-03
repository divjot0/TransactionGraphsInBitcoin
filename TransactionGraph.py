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
	print("Done with a block")
	return listOfSetsInBlock

def addAllEntityEdges(blockHash, listOfSets):
	""" 
		Add info about tx as well
	"""
	s='http://localhost:8332/rest/block/'+blockHash+'.json'
	myDict = requests.get(s).json()
	jStr = json.dumps(myDict)
	block = json.loads(jStr)

	listOfEdgesInBlock=[]
	realListIndex1=-1
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
						i=0
						for aSet in listOfSets:
							if r in aSet:
								realListIndex1=i
								break
							i=i+1
						break
		if realListIndex1!=-1:
			for outputTransaction in transaction['vout']:
				if outputTransaction['scriptPubKey']['type']=="pubkeyhash":
					addr = outputTransaction['scriptPubKey']['addresses'][0]
					i=0
					for aSet in listOfSets:
						if addr in aSet:
							realListIndex2=i
							listOfEdgesInBlock.append([realListIndex1,realListIndex2])
							break
						i=i+1

	return listOfEdgesInBlock


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

listOfEdges = []

for blkhash in block_hashes:
	listOfEdges.append(addAllEntityEdges(blkhash, listOfSets))


for aSet in listOfSets:
	print(aSet)
