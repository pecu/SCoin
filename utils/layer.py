import os

def in_layer_1(username):
    list_accounts = os.listdir("accounts")
    if username not in list_accounts:
        return False
    with open("cluster/layer_1.txt", 'r') as outfile:
        list_layer_1 = outfile.read().splitlines()
        if username in list_layer_1:
            return True
    return False
