import os
import json
from app.rsa import encrypt_with_pub_key 
from app.token import new_seed
from db import user
from utils.user import check_password
from dotenv import load_dotenv

load_dotenv()
CB_API_KEY = os.getenv("CB_API_KEY")


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
    cb = user.select_by_username("cb")
    
    return check_password(api_key, cb["api_key"])

def get_cb_api_key():
    return CB_API_KEY
