import os

def user_exist(user):
    if user == "":
        return False
    if not os.path.isdir("accounts/" + user):
        return False
    return True

