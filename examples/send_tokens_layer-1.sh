username=$1
tokenAmount=$2

send() {
  curl -s http://3.87.137.58:8888/send_token \
	  -X POST \
    -H 'Content-Type: application/json' \
    -H 'X-API-key: 9jhy765ae128e45629ihbn292b2b3f19084ijygv' \
    -d '{"sen": "cb", "rev": "'${username}'", "method": "1", "description": "SCU Token", "txn":""}'; \
  echo ""
}
export -f send
export username

for i in $(seq 1 $tokenAmount);
do
  sem -j 4 send 
done
sem --wait
