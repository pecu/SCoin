import os
import json
import iota
from app.rsa import gen_key_pair
from app.blockchain.tangle import send_transfer, get_txn_hash_from_bundle, \
        find_transaction_message 
from db import user
from utils.user import make_password_hash
from error import InvalidUsage


PATH_ACCOUNT = "./accounts/"
receiver_address = "ILXW9VMJQVFQVKVE9GUZSODEMIMGOJIJNFAX9PPJHYQPUHZLTWCJZKZKCZYKKJJRAKFCCNJN9EWOW9N9YDGZDDQDDC"

class DID():
    def __init__(self):
        return

    def new_did(self, x_api_key, data):
        # Check username exist
        if os.path.isdir(PATH_ACCOUNT + data["name"]):
            raise InvalidUsage("Account already exist", 409)

        # create DID

        ## Create account folder on local
        os.mkdir(PATH_ACCOUNT + data["name"])

        ## Save hash of password
        with open(PATH_ACCOUNT + data["name"] + "/x-api-key.txt", 'w') as outfile:
            outfile.write(x_api_key)

        ## Save key-pair
        if data["pub_key"] == "":
            pub_key, pri_key = gen_key_pair()
            data["pub_key"] = pub_key
            with open(PATH_ACCOUNT + data["name"] + "/private.pem", 'w') as outfile:
                outfile.write(pri_key)
        
        ## Send to Tangle
        bundle = send_transfer(data, receiver_address)
        # hash_txn = get_txn_hash_from_bundle(hash_bundle)
        txn = None
        for tx in bundle.transactions:
            msg = find_transaction_message(tx.hash)
            if msg == json.dumps(data):
                txn = tx
                break
        if txn == None:
            raise InvalidUsage("Internal server error", 500)
        hash_txn = str(tx.hash)
        
        ## Insert into database
        user_obj = {
            "username": data["name"],
            "hash": hash_txn,
            "created_at": txn.timestamp,
            "description": data["description"],
            "password": make_password_hash(x_api_key)
        }
        user.insert(user_obj)

        ## Write Profile
        data["id"] = hash_txn
        with open(PATH_ACCOUNT + data["name"] + "/profile.json", 'w') as outfile:
            json.dump(data, outfile)
        
        return hash_txn

    def get_DID_from_username(self, username):
        with open(PATH_ACCOUNT + username + "/profile.json", 'r') as outfile:
            obj_did = json.load(outfile)
            return obj_did["id"]

    def get_pub_key_by_DID(self, DID_id):
        public_key = ""
        msg_txn = find_transaction_message(DID_id)
        obj_msg = json.loads(msg_txn)

        return obj_msg["pub_key"]

    def get_api_key_by_user(self, user):
        with open(PATH_ACCOUNT + user + "/x-api-key.txt", 'r') as outfile:
            return outfile.read()

    def get_cluster(self):
        cluster = {"cb":"","layer-1":[]}
        list_layer_1 = []

        # Set cb
        did_cb = self.get_DID_from_username("cb")
        cluster["cb"] = did_cb

        # Append layer-1
        with open("cluster/layer_1.txt", 'r') as outfile:
            for line in outfile:
                stripped_line = line.strip()
                layer_did = self.get_DID_from_username(stripped_line)
                cluster["layer-1"].append(layer_did)

        return cluster
