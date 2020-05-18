import sys
import pytest
import iota
from tests.mocks.iota import iota_mock
from unittest import mock
import os
import shutil

from app.did import DID

did = DID()

PATH_ACCOUNT = "./accounts/"


def test_new_did(env):
    x_api_key = 'testapikey'
    data = {
        "method": "light",
        "name": "testapi",
        "description": "Zhushan light eID",
        "pub_key": ""}
    did.new_did(x_api_key, data)
    assert os.path.isdir(PATH_ACCOUNT + data["name"])
    with open(PATH_ACCOUNT + data["name"] + "/x-api-key.txt", 'r') as outfile:
        fileapikey = outfile.read().splitlines()
        assert fileapikey[0] == x_api_key
    shutil.rmtree(PATH_ACCOUNT + "testapi")



def test_get_DID_from_username(env):
    x_api_key = 'testapikey'
    data = {
        "method": "light",
        "name": "testapi",
        "description": "Zhushan light eID",
        "pub_key": ""}
    did.new_did(x_api_key, data)
    assert did.get_DID_from_username("testapi") == "KYVEAQJKIYSNH9SGULNSPDFGULCV9DETKWIFUUH9GICWMMYJFRVUSDWFNXIAXBHW9BNNXOKGVOMKZ9999"
    shutil.rmtree(PATH_ACCOUNT + "testapi")

def test_get_cluster(env):
    
    test_cluster = {
        "cb": "KYVEAQJKIYSNH9SGULNSPDFGULCV9DETKWIFUUH9GICWMMYJFRVUSDWFNXIAXBHW9BNNXOKGVOMKZ9999",
        "layer-1": []}
    x_api_key = '9jhy765ae128e45629ihbn292b2b3f19084ijygv'
    data = {
        "method": "light",
        "name": "cb",
        "description": "Zhushan light eID",
        "pub_key": ""
        }
    did.new_did(x_api_key, data)
    res = did.get_cluster()
    assert res == test_cluster
