import os
import random
import string

def random_string(stringLength=8):
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(stringLength))

def append_file(path, string):
    with open(path, 'a') as outfile:
        outfile.write(string)

# ACCESS TOKEN
print("Generating ADMIN_ACCESS_TOKEN ...")
admin_access_token = "ADMIN_ACCESS_TOKEN = \"" + random_string(40)  + "\""
append_file("../config.py", admin_access_token)

# Make accounts directory
os.mkdir("../accounts")

print("Success!Follow the steps as below to finish the account setup:")
print("1. Run the server by: $python3 server")
print("2. Generate a new cb did (Remember to modify the header <X-API-key>): $bash new_cb.sh")
print("Enjoy!")
