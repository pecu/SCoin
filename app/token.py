import time
import string
import random
import json
import os
import iota
from app.did import DID
from app.rsa import encrypt_with_pub_key, decrypt_with_pri_key
from app.blockchain.tangle import send_transfer, get_txn_hash_from_bundle, \
        find_transaction_message, generate_new_address, get_account_data
from app.auth import check_api_key
from utils.layer import in_layer_1
from error import InvalidUsage
from db import transaction

PATH_ACCOUNT = "./accounts/"

def new_seed(user):
    seed = ''.join(random.choice(string.ascii_uppercase + "9") for _ in range(81))
    with open(PATH_ACCOUNT + user + "/seed.txt", 'a') as outfile:
        outfile.write(seed + "\n")

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

def check_token_in_history(user, txn):
    with open(PATH_ACCOUNT + user + "/history.txt", 'r') as outfile:
        list_balance = outfile.read().splitlines()
        if txn in list_balance:
            return True
        else:
            return False

def layer_to_layer(api_key, data):
    if data["txn"] != "":
        if check_token_in_history(data["sen"], data["txn"]) == False:
            return {"status":"error","msg":"No this token in wallet"}

    # Load basic token cred
    cred = load_token_json_obj()

    # Set method
    cred["method"] = data["method"]

    # Get/Set sender DID ID
    did = DID()
    id_sender = did.get_DID_from_username(data["sen"])
    cred["sen"] = id_sender

    # Check receiver exist
    if not os.path.isdir("accounts/" + data["rev"]):
        return {"status":"error", "msg":"Receiver not exist."}

    # Get/Set receiver DID ID
    id_receiver = did.get_DID_from_username(data["rev"])
    cred["rev"] = id_receiver

    # Get seed
    seed = ""
    if data["txn"] == "" and data["method"] == "1":
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
            return {"status":"error","msg":"invalid token"}

        enseed = get_txn_enseed(data["txn"])

        if enseed == "":
            return {"status":"error","msg":"invalid token"}

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
        raise InvalidUsage("Internal server error", 500)

    ## Insert into database
    obj = {
            "hash": str(txn.hash),
            "sender": data["sen"],
            "receiver": data["rev"],
            "description": json.dumps(cred),
            "timestamp": tx.timestamp
          }
    transaction.insert(obj)
    hash_txn = str(tx.hash)

    ## Save to history
    with open(PATH_ACCOUNT + data["rev"] + "/history.txt", 'a') as outfile:
        outfile.write(hash_txn + "\n")

    ## Update history list
    if data["txn"] != "" and data["method"] != "1":
        list_balance = []
        with open(PATH_ACCOUNT + data["sen"] + "/history.txt", 'r') as outfile:
            list_balance = outfile.read().splitlines()
            try:
                list_balance.remove(data["txn"])
            except ValueError:
                print("No " + data["txn"] + " in history.")

        with open(PATH_ACCOUNT + data["sen"] + "/history.txt", 'w') as outfile:
             for listitem in list_balance:
                 outfile.write('%s\n' % listitem)

    return hash_txn

def get_user_balance(user):
    # Check user exist
    if not os.path.isdir(PATH_ACCOUNT + user):
        return ""#{"status":"error", "msg":"User not exist."}

    # Check history file exist
    if not os.path.isfile(PATH_ACCOUNT + user + "/history.txt"):
        return ""#""

    with open(PATH_ACCOUNT + user + "/history.txt", 'r') as outfile:
        return outfile.read()[:-1]

def check_token_valid(user, api_key, data):
    # Get transaction message field    
    msg_txn = find_transaction_message(data["token"])
    obj_msg = json.loads(msg_txn)
    enseed = obj_msg["enseed"]
 
    # Decrypt seed
    seed = decrypt_with_pri_key(user, api_key, enseed)

    # Verify address
    # start = time.time() 
    account_info = get_account_data(seed)
    # print("account_info : " + str(account_info))
    # end = time.time()
    # print("Duration of get_account_data function: " + str(end - start))
    
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

    # Re-set txn information
    did = DID()

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
    api_key_sender = did.get_api_key_by_user("cb")

    # snapshot
    new_token = layer_to_layer(api_key_sender, obj_msg)

    return new_token
