import sys
import pytest
from app.cb import set_layer_1, remove_layer_1, verify_cb_api_key


def test_set_layer_1():
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


def test_remove_layer_1():
    test_username = 'removable'
    result = remove_layer_1(test_username)
    assert result
    with open("cluster/layer_1.txt", 'r') as outfile:
        list_layer_1 = outfile.read().splitlines()
    assert test_username not in list_layer_1
    with open("cluster/layer_1.txt", 'a') as outfile:
        outfile.write(test_username + "\n")
    return True


def test_verify_cb_api_key():
    test_x_api_key = "9jhy765ae128e45629ihbn292b2b3f19084ijygv"
    result = verify_cb_api_key(test_x_api_key)
    assert result
