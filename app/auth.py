import os

# Check API key
def check_api_key(user, api_key):
    api_key_from_file = ""
    with open("accounts/" + user + "/x-api-key.txt", 'r') as outfile:
        api_key_from_file = outfile.read().splitlines()[0]

    if api_key_from_file != api_key:
        return False
    else:
        return True

def get_api_key(username):
    api_key_from_file = ""
    with open("accounts/" + username + "/x-api-key.txt", 'r') as outfile:
        api_key_from_file = outfile.read().splitlines()[0]

    return api_key_from_file

def new_user(data):
    # Check username exist
    if os.path.isdir("accounts/" + data["name"]):
        return False 

    ## Create account folder on local
    os.mkdir("accounts/" + data["name"])

    ## Save hash of password
    with open("accounts/" + data["name"] + "/x-api-key.txt", 'w') as outfile:
        outfile.write(data["password"])

    return True
