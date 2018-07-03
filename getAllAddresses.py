import json
import requests
import subprocess

def getAddress(rawTransaction, outputIndex):
	tx = json.loads(rawTransaction)
	if tx['vout'][outputIndex]['scriptPubKey']['type']=="pubkeyhash":
		return tx['vout'][outputIndex]['scriptPubKey']['addresses'][0]
	else:
		return None

def getBlockAddresses(blockHash):
	s='http://localhost:8332/rest/block/'+blockHash+'.json'
	myDict = requests.get(s).json()
	jStr = json.dumps(myDict)
	block = json.loads(jStr)

	listOfAddressesInBlock = []

	for transaction in block['tx']:
		for inputTransaction in transaction['vin']:
			if 'txid' in inputTransaction:
				result = subprocess.run(["bitcoin-cli", "getrawtransaction", str(inputTransaction['txid']), "1"], stdout=subprocess.PIPE)
				a = result.stdout.decode()
				r = getAddress(a, inputTransaction['vout'])
				if r!=None:
					if r not in listOfAddressesInBlock:
						listOfAddressesInBlock.append(r)
		for outputTransaction in transaction['vout']:
			if outputTransaction['scriptPubKey']['type']=="pubkeyhash":
				listOfAddressesInBlock.append(outputTransaction['scriptPubKey']['addresses'][0])
	print("Done with a block")
	return listOfAddressesInBlock

listOfAddresses = []

start_block = int(input("Enter start block"))
end_block = int(input("Enter end block"))
block_hashes = []
command = "bitcoin-cli"

for x in range(start_block, end_block):
	result = subprocess.run([command, 'getblockhash', str(x)], stdout=subprocess.PIPE)
	block_hashes.append(result.stdout.decode()[:-1])

print("Got all block hashes. Now starting to get address")

for blkHash in block_hashes:
	listOfAddress.append(getBlockAddresses(blkhash))