import os
import json
from app.did import DID
from app.token import layer_to_layer

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
    cred["description"] = "Light token"

    # API key
    api_key_sender = did.get_api_key_by_user("cb")

    # Others
    cred["txn"] = ""

    # Send
    new_token = layer_to_layer(api_key_sender, cred)

    return new_token
