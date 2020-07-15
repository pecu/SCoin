# Usage
# python3 send_tokens_layer-2.py sender receiver amount

import requests
import sys
import json

url = "http://52.44.57.177:8888/"
r = requests.get(url + "get_balance?user=" + sys.argv[1])

balances = (r.content.decode("utf-8")).split("\n")
if len(balances) < int(sys.argv[3]):
    print("Not enough balance\n")
    exit()

for i in range(int(sys.argv[3])):
    data = {"sen": sys.argv[1], "rev": sys.argv[2], "method": 2, "description": "SCU Coin", "txn": balances[i]}
    headers = {"Content-type": "application/json", "X-API-key": "fu06ji3ul4"}
    r = requests.post(url + "send_token", data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        print("Send failed, code " + str(r.status_code))
