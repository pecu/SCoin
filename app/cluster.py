import os
import json
from app.did import DID
from app.token import layer_to_layer
from app.cb import get_cb_api_key

def check_alliance(name, x_api_key):
    # Check account reference
    if not os.path.isfile("cluster/alliance/" + name + ".txt"):
        return False

    # Check API key
    with open("cluster/alliance/" + name + ".txt", 'r') as outfile:
        obj_alliance = json.load(outfile)
        if obj_alliance["key"] == x_api_key:
            return True
        else:
            return False

def bridge_cluster(data):
    cred = {}
    did = DID()
    # Re-issue token from Light-CB
    cred["sen"] = "cb"

    # Set receiver
    cred["rev"] = data["rev"]

    # Method
    cred["method"] = "1"

    # Description
    cred["description"] = "Scoin"

    # API key
    api_key_sender = get_cb_api_key()

    # Others
    cred["txn"] = ""

    # Send
    new_token = layer_to_layer(api_key_sender, cred)

    return new_token
