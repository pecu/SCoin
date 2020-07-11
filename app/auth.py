import os
from werkzeug.security import generate_password_hash, \
        check_password_hash
from db import user
from utils.user import make_password_hash, check_password

# Check API key
def check_api_key(user, api_key):
    if not os.path.isdir("accounts/" + user):
        return False

    api_key_from_file = ""
    with open("accounts/" + user + "/x-api-key.txt", 'r') as outfile:
        api_key_from_file = outfile.read().splitlines()[0]

    if api_key_from_file != api_key:
        return False
    else:
        return True

def set_user_password(data):
    # Check user exist
    if not os.path.isdir("accounts/" + data["name"]):
        return False

    with open("accounts/" + data["name"] + "/password.hash", 'w') as outfile:
        outfile.write(generate_password_hash(data["password"]))

    return True

def get_password_hash(username):
    with open("accounts/" + username + "/password.hash", 'r') as outfile:
        return outfile.read()

def check_permission(username, api_key):
    if username != ""  and api_key != "":
        if check_api_key(username, api_key) == True:
            return True
        else:
            return False

    return False

#0 => user doesn't exist                                                                                              
#1 => user exist
#2 => incorrect password
def check_account(username, api_key):
    res = user.query('username', username)
    # user doesn't exist
    if res == None:
        return 0;
    res_pwd = res[0]["api_key"]
    # user exist
    if check_password(api_key, res_pwd):
        return 1;
    # password incorrect
    return 2;
