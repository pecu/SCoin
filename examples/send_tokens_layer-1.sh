username=$1
tokenAmount=$2

for((i=0;i<${tokenAmount};i++));
do
	curl http://3.87.137.58:8888/send_token \
			-X POST \
      -H 'Content-Type: application/json' \
      -H 'X-API-key: 9jhy765ae128e45629ihbn292b2b3f19084ijygv' \
      -d '{"sen": "cb", "rev": "'${username}'", "method": "1", "description": "SCU Token", "txn":""}';

  echo ""
done
