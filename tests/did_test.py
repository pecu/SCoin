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


@pytest.fixture(scope="module", autouse=True)
def iota():
    with mock.patch('app.blockchain.tangle.Iota', side_effect=iota_mock):
        yield


def test_new_did():
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


def test_get_DID_from_username():
    assert did.get_DID_from_username(
        "testapi") == "KYVEAQJKIYSNH9SGULNSPDFGULCV9DETKWIFUUH9GICWMMYJFRVUSDWFNXIAXBHW9BNNXOKGVOMKZ9999"


def test_get_cluster():
    test_cluster = {
        "cb": "VFBDBPNWXWDFQFBZQCOCQJVGFPJIQPSUVVMESTFUBNGJXUARNTRRZMUPQ9SSORFXDDRCZWU9QZKVZ9999",
        "layer-1": ["KYVEAQJKIYSNH9SGULNSPDFGULCV9DETKWIFUUH9GICWMMYJFRVUSDWFNXIAXBHW9BNNXOKGVOMKZ9999"]}
    res = did.get_cluster()
    assert res == test_cluster


def test_teardown():
    shutil.rmtree(PATH_ACCOUNT + "testapi")
