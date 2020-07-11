import os
import random
import string
import hashlib
from db import user

def user_exist(username):
    usr = user.select_by_username(username)
    if (usr == None)
        return False
    return True

def get_total_user():
    return len(os.listdir("accounts/"))

def make_salt(length=10):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))

def make_password_hash(password, salt=None):
    if salt is None:
        salt = make_salt()
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest() + "|" + salt

def check_password(password, password_hash):
    salt = password_hash.split("|")[1]
    return make_password_hash(password, salt) == password_hash

