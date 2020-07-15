import os
from db import user
from utils.user import make_password_hash, check_password
from utils.user import user_exist, check_password
from db import user

# Check API key
def check_api_key(username, api_key):
    if not user_exist(username):
        return False

    usr = user.select_by_username(username)
    return check_password(api_key, usr["api_key"])

def check_permission(username, api_key):
    if username != ""  and api_key != "":
        return check_api_key(username, api_key)
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
