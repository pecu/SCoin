import time
import string
import random
import json
import os
import iota
from app.did import DID
from app.rsa import encrypt_with_pub_key, decrypt_with_pri_key
from app.blockchain.tangle import send_transfers, send_transfer, get_txn_hash_from_bundle, \
        find_transaction_message, generate_new_address, get_account_data
from app.auth import check_api_key
from app.cb import get_cb_api_key
from utils.layer import in_layer_1
from utils.user import user_exist
from error import InvalidUsage, InternalError
from db import transaction, connect

PATH_ACCOUNT = "./accounts/"

def new_seed(user):
    seed = ''.join(random.choice(string.ascii_uppercase + "9") for _ in range(81))
    return seed 

def load_token_json_obj():
    obj_token = {}
    with open("credential/token.json", 'r') as outfile:
        obj_token = json.load(outfile)
        
    return obj_token

def get_txn_enseed(txn_hash):
    enseed = ""

    try:
        msg_txn = find_transaction_message(txn_hash)
        obj_msg = json.loads(msg_txn)
        enseed = obj_msg["enseed"]
    except:
        return ""

    return enseed

def check_token_in_history(username, txn_hash):
    return transaction.select_by_hash(txn_hash)["receiver"] == username

def layer_to_layer_multiple(api_key, data):
    try:
        if data["method"] != "2":
            raise InvalidUsage("Only support method 2.", 404)

        if not user_exist(data["rev"]):
            raise InvalidUsage("Receiver does not exist", 404)

        if "" in data["txn"]:
            raise InvalidUsage("Invalid token", 400)

        connect.start_commit()

        for txn in data["txn"]:
            if not check_token_in_history(data["sen"], txn):
                raise InvalidUsage("Token {} not found.".format(txn), 404)

        did = DID()
        cred = load_token_json_obj()
        id_sender = did.get_DID_from_username(data["sen"])
        id_receiver = did.get_DID_from_username(data["rev"])
        receiver_pub_key = did.get_pub_key_by_DID(id_receiver)

        seeds = [] 
        enseed = []
        enseeds_sender = []
        address = []
        for txn in data["txn"]:
            enseeds_sender.append(get_txn_enseed(txn))

        for enseed_sender in enseeds_sender:
            seeds.append(decrypt_with_pri_key(data["sen"], api_key, enseed_sender))

        for seed in seeds:
            enseed.append(encrypt_with_pub_key(receiver_pub_key, seed))
            address.append(generate_new_address(seed))

        cred["method"] = data["method"]
        cred["description"] = data["description"]
        cred["sen"] = id_sender
        cred["rev"] = id_receiver
        cred["enseed"] = enseed
        cred["address"] = address

        bundle = send_transfers(cred)
        tx_hashs = []
        for tx in bundle.transactions:
            obj = {
                    "hash": str(tx.hash),
                    "sender": data["sen"],
                    "receiver": data["rev"],
                    "description": cred["description"],
                    "timestamp": tx.timestamp,
                    "spent": '0',
                }
            transaction.insert(obj)
            tx_hashs.append(str(tx.hash))

        for txn in data["txn"]:
            transaction.spend_transaction(txn)
        connect.end_commit()
    finally:
        connect.close()

    return tx_hashs

def layer_to_layer(api_key, data):
    try:
        connect.start_commit()
        if data["txn"] != "":
            if check_token_in_history(data["sen"], data["txn"]) == False:
                raise InvalidUsage("Token not found.", 404)

        # Load basic token cred
        cred = load_token_json_obj()

        # Set method
        cred["method"] = data["method"]

        # Get/Set sender DID ID
        did = DID()
        id_sender = did.get_DID_from_username(data["sen"])
        cred["sen"] = id_sender

        # Check receiver exist
        if not user_exist(data["rev"]):
            raise InvalidUsage("Receiver does not exist", 404)

        # Get/Set receiver DID ID
        id_receiver = did.get_DID_from_username(data["rev"])
        cred["rev"] = id_receiver

        cred["description"] = data["description"]

        # Get seed
        seed = ""
        if data["method"] == "1":
            if data["txn"] != "":
                raise InvalidUsage("Txn should be empty.", 400)
            if data["sen"] != "cb":
                raise InvalidUsage("Permission denied.", 403)
            if not in_layer_1(data["rev"]):
                raise InvalidUsage("User is not in the layer1 list.", 403)
            # Method 1 (CB to layer-1) or create a new branch
            seed = new_seed(data["sen"])
        else:
            # Method 2 (layer to layer)
            # Decrypt sender enseed
            if data["txn"] == "":
                raise InvalidUsage("Invalid token", 400) 

            enseed = get_txn_enseed(data["txn"])

            if enseed == "":
                raise InvalidUsage("Invalid token", 400)

            seed = decrypt_with_pri_key(data["sen"], api_key, enseed)

        # Get receiver public key
        receiver_pub_key = did.get_pub_key_by_DID(cred["rev"])

        # Encrypt seed
        enseed = encrypt_with_pub_key(receiver_pub_key, seed)
            
        # Set enseed
        cred["enseed"] = enseed

        # Generate address
        address = generate_new_address(seed)
        cred["address"] = address

        ## Send to Tangle
        bundle = send_transfer(cred, address, seed)
        # hash_txn = get_txn_hash_from_bundle(bundle.hash)
        txn = None
        for tx in bundle.transactions:
            msg = find_transaction_message(tx.hash)
            if msg == json.dumps(cred):
                txn = tx
                break
        if txn == None:
            raise InternalError("Internal server error", 500)

        ## Insert into database
        obj = {
                "hash": str(txn.hash),
                "sender": data["sen"],
                "receiver": data["rev"],
                "description": cred["description"],
                "timestamp": tx.timestamp,
                "spent": "0",
                "raw_transaction": str(txn.as_tryte_string())
              }
        transaction.insert(obj)
        hash_txn = str(tx.hash)


        ## Update transaction spent status
        if data["txn"] != "" and data["method"] != "1":
            transaction.spend_transaction(data["txn"])
        connect.end_commit()
    finally:
        connect.close()

    return hash_txn

def get_user_balance(username):
    # Check user exist
    if not user_exist(username):
        raise InvalidUsage("User does not exist.", 404)

    txns = transaction.select_unspent_by_username(username)
    return [tx["hash"] for tx in txns]

def check_token_valid(user, api_key, data):
    # Get transaction message field    
    msg_txn = find_transaction_message(data["token"])
    obj_msg = json.loads(msg_txn)
    enseed = obj_msg["enseed"]
 
    # Decrypt seed
    seed = decrypt_with_pri_key(user, api_key, enseed)

    # Verify address
    account_info = get_account_data(seed)
    
    latest_address = ""
    try:
        latest_address = str(account_info["addresses"][len(account_info["addresses"])-1])
    except:
        return False

    if latest_address == obj_msg["address"]:
        return True
    else:
        return False

def snapshot(api_key, data):
    new_token = data["token"]

    # Get transaction message field    
    msg_txn = find_transaction_message(data["token"])
    obj_msg = json.loads(msg_txn)

    ## Sender
    obj_msg["sen"] = "cb"

    ## Method
    obj_msg["method"] = "1"

    ## Receiver
    obj_msg["rev"] = data["user"]

    ## Enseed
    obj_msg["txn"] = ""

    ## Address
    obj_msg["address"] = ""

    # API key
    api_key_sender = get_cb_api_key()

    # snapshot
    new_token = layer_to_layer(api_key_sender, obj_msg)

    return new_token
