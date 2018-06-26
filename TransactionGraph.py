import subprocess

start_block = int(input())
end_block = int(input())
block_hashes = []
command = "bitcoin-cli"

for x in range(start_block, end_block):
	result = subprocess.run([command, 'getblockhash', str(x)], stdout=subprocess.PIPE)
	block_hashes.append(result.stdout.decode()[:-1])

for block_hash in block_hashes:
	print (block_hash)