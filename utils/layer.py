import os
from db import user

def in_layer_1(username):
    usr = user.select_by_username(username)
    return usr["layer"] == 1
