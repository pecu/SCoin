import os
import random
import string
import hashlib

def user_exist(user):
    if user == "":
        return False
    if not os.path.isdir("accounts/" + user):
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

