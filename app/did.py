import os
import json
import iota
from app.rsa import gen_key_pair
from app.blockchain.tangle import send_transfer, get_txn_hash_from_bundle, \
        find_transaction_message 
from db import user, connect
from utils.user import make_password_hash, user_exist
from error import InvalidUsage



PATH_ACCOUNT = "./accounts/"
receiver_address = "ILXW9VMJQVFQVKVE9GUZSODEMIMGOJIJNFAX9PPJHYQPUHZLTWCJZKZKCZYKKJJRAKFCCNJN9EWOW9N9YDGZDDQDDC"

class DID():
    def __init__(self):
        return

    def new_did(self, x_api_key, data):
        try:
            connect.start_commit()
            # Check username exist
            if user_exist(data["name"]):
                raise InvalidUsage("Account already exist", 409)

            if data["pub_key"] == "":
                pub_key, pri_key = gen_key_pair()
                data["pub_key"] = pub_key

            ## Send to Tangle
            bundle = send_transfer(data, receiver_address)
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
                "api_key": make_password_hash(x_api_key),
                "layer": 0 if data["name"] == "cb" else 2,
                "public_key": pub_key,
                "private_key": pri_key
            }
            user.insert(user_obj)

            ## Write Profile
            data["id"] = hash_txn
            connect.end_commit()
        finally:
            connect.close()
        
        return hash_txn

    def get_DID_from_username(self, username):
        return user.select_by_username(username)["hash"]


    def get_pub_key_by_DID(self, DID_id):
        return user.select_by_hash(DID_id)["public_key"]

    def get_cluster(self):
        cluster = {"cb":"","layer-1":[]}
        list_layer_1 = []

        # Set cb
        did_cb = self.get_DID_from_username("cb")
        cluster["cb"] = did_cb

        users = user.select_by_layer(1)
        for usr in users:
            cluster["layer-1"].append(usr["hash"])

        return cluster
