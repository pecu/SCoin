import os
import json
from app.rsa import encrypt_with_pub_key 
from app.token import new_seed


def set_layer_1(username):
    # Check if the username in the accounts
    list_accounts = os.listdir("accounts")
    if username not in list_accounts:
        return False

    # Search for duplicate
    with open("cluster/layer_1.txt", 'r') as outfile:
        list_layer_1 = outfile.read().splitlines()
        if username in list_layer_1:
            print("Error: Duplicate username in layer-1")
            return False

    # Set layer-1
    with open("cluster/layer_1.txt", 'a') as outfile:
        outfile.write(username + "\n")

    return True

def remove_layer_1(username):
    #Find if user exist:
    list_layer_1 = []
    with open("cluster/layer_1.txt", 'r') as outfile:
        list_layer_1 = outfile.read().splitlines()
        if username in list_layer_1:
            list_layer_1.remove(username)
        else:
            return False
    with open("cluster/layer_1.txt", 'w') as outfile:
        for item in list_layer_1:
            outfile.write(item + '\n')
    return True
        
def verify_cb_api_key(api_key):

    api_key_cb = ""
    with open("accounts/cb/x-api-key.txt", 'r') as outfile:
        api_key_cb = outfile.read().splitlines()[0]

    if api_key_cb == api_key:
        return True
    else:
        return False
