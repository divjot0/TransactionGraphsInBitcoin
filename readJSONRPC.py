import json
import requests


my_dict = requests.get('http://localhost:8332/rest/block/000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506.json').json()
jstr = json.dumps(my_dict)
data = json.loads(jstr)
index=0
for key in data['tx']:
	for x in key['vin']:
		if 'txid' in x:
			print(x['txid'])
			print(x['vout'])
		else:
			print("coinbase")
		print("\n")
	print ("\n\n")
	index=index+1