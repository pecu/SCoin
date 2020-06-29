import sys
import pytest
from app.cb import set_layer_1, remove_layer_1, verify_cb_api_key
from app.did import DID
import shutil

def test_set_layer_1(env):
    test_username = 'testapi'
    result = set_layer_1(test_username)
    assert result
    list_layer_1 = []
    with open("cluster/layer_1.txt", 'r') as outfile:
        list_layer_1 = outfile.read().splitlines()
    assert test_username in list_layer_1
    with open("cluster/layer_1.txt", 'w') as outfile:
        list_layer_1.remove(test_username)
        for item in list_layer_1:
            outfile.write(item + '\n')
    return True


def test_remove_layer_1(env):
    test_username = 'removable'
    with open("cluster/layer_1.txt", 'a') as outfile:
        outfile.write(test_username + "\n")
    result = remove_layer_1(test_username)
    assert result == True
    with open("cluster/layer_1.txt", 'r') as outfile:
        list_layer_1 = outfile.read().splitlines()
        assert test_username not in list_layer_1
    
    return True


def test_verify_cb_api_key(env):
    did = DID()
    test_x_api_key = "9jhy765ae128e45629ihbn292b2b3f19084ijygv"
    x_api_key = '9jhy765ae128e45629ihbn292b2b3f19084ijygv'
    data = {
        "method": "light",
        "name": "cb",
        "description": "Zhushan light eID",
        "pub_key": ""
        }
    did.new_did(x_api_key, data)
    result = verify_cb_api_key(test_x_api_key)
    assert result
