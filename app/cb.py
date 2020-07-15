import os
import json
from app.rsa import encrypt_with_pub_key 
from app.auth import check_permission
from db import user
from utils.user import check_password, user_exist
from dotenv import load_dotenv
from error import InvalidUsage

load_dotenv()
CB_API_KEY = os.getenv("CB_API_KEY")


def set_layer_1(username):
    if not user_exist(username):
        raise InvalidUsage("User does not exist.", 404)

    # Set layer-1
    user.set_layer_by_username(username, 1)

def remove_layer_1(username):
    if not user_exist(username):
        raise InvalidUsage("User does not exist.", 404)

    user.set_layer_by_username(username, 2)
        
def verify_cb_api_key(api_key):
    return check_permission("cb", api_key)

def get_cb_api_key():
    return CB_API_KEY
