import pytest
import os
import shutil
from unittest import mock
import iota
from server import app
from tests.mocks.iota import iota_mock


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module", autouse=True)
def iota():
    with mock.patch('app.blockchain.tangle.Iota', side_effect=iota_mock):
        yield


@pytest.fixture()
def env():
    try:
        os.stat("accounts")
    except BaseException:
        os.mkdir("accounts")
    try:
        os.stat("cluster")
    except BaseException:
        os.mkdir("cluster")
    open("cluster/layer_1.txt", "w").close()

    yield

    shutil.rmtree("cluster")
    shutil.rmtree("accounts")