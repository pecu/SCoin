from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
import binascii
from db import user
from utils.user import check_password
from error import InvalidUsage, InternalError

def bin2hex(bin_str):
    return binascii.hexlify(bin_str)

def hex2bin(hex_str):
    return binascii.unhexlify(hex_str)

def gen_key_pair():
    key = RSA.generate(1024)
    public_key = key.publickey().exportKey('PEM').decode('ascii')
    private_key = key.exportKey('PEM').decode('ascii')

    return public_key, private_key

def encrypt_with_pub_key(pub_key, data):
    publickey = RSA.importKey(pub_key)
    encryptor = PKCS1_OAEP.new(publickey)
    # Convert data to byte and encrypt it
    encrypted = encryptor.encrypt(str.encode((data)))
    # Convert byte to hex
    encrypted = bin2hex(encrypted)
    # Convert hex to string
    encrypted = encrypted.decode('ascii')

    return encrypted

def decrypt_with_pri_key(username, user_api_key, data):
    # Check API key
    usr = user.select_by_username(username)
    if not check_password(user_api_key, usr["api_key"]):
        raise InvalidUsage("Permission denied.", 403)

    # Decrypt
    private_key = usr["private_key"]
    privatekey = RSA.importKey(private_key)
    decryptor = PKCS1_OAEP.new(privatekey)

    # Convert string to byte
    encrypted = data.encode('ascii')
    
    # Hex to bin
    encrypted = hex2bin(encrypted)
    decrypted = ""
    try:
        decrypted = decryptor.decrypt(encrypted)
    except:
        raise InternalError("Decrypt failed.", 500)

    return decrypted.decode()
