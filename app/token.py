import time
import string
import random
import json
import os
from app.did import DID
from app.rsa import encrypt_with_pub_key, decrypt_with_pri_key
from app.blockchain.tangle import send_transfer, get_txn_hash_from_bundle, \
        find_transaction_message, generate_new_address, get_account_data
from app.auth import check_api_key

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

    msg_txn = find_transaction_message(txn_hash)
    obj_msg = json.loads(msg_txn)
    enseed = obj_msg["enseed"]

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
    if data["txn"] == "" or data["method"] == "1":
        # Method 1 (CB to layer-1) or create a new branch
        seed = new_seed(data["sen"])
    else:
        # Method 2 (layer to layer)
        # Decrypt sender enseed
        enseed = get_txn_enseed(data["txn"])
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
    hash_bundle = send_transfer(cred, address, seed)
    hash_txn = get_txn_hash_from_bundle(hash_bundle)

    ## Save to history
    with open(PATH_ACCOUNT + data["rev"] + "/history.txt", 'a') as outfile:
        outfile.write(hash_txn + "\n")

    ## Update history list
    if data["txn"] != "" or data["method"] != "1":
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
    balanceInfo = {
        'balance' : None,
        'tx' : [],
        'status' : 'Success',
    }

    if not os.path.isdir(PATH_ACCOUNT + user):
        balanceInfo['status'] = 'Fail'
        balanceInfo['error'] = 'User is not exist'

        return balanceInfo

    # Check history file exist
    if not os.path.isfile(PATH_ACCOUNT + user + "/history.txt"):
        balanceInfo['status'] = 'Fail'
        balanceInfo['error'] = '''User doesn't has tx history'''
        
        return balanceInfo

    with open(PATH_ACCOUNT + user + "/history.txt", 'r') as outfile:
        for i, l in enumerate(outfile):
            balanceInfo['tx'].append(l)
        
        balanceInfo['balance'] = i + 1

        return balanceInfo

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
