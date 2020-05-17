import pytest
import json
from unittest import mock
import random
import string
import iota
import app.blockchain.tangle as tangle


def test_new_did_api(env, client):
    letters = string.ascii_letters + string.digits
    data = {
        "name": "".join(random.choice(letters) for i in range(10)),
        "pub_key": "",
        "method": "light",
        "description": "Scoin light eID"
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-key": "secret"
    }
    rv = client.post("/new_did", data=json.dumps(data), headers=headers)

    assert rv.status_code == 200
    assert len(rv.data) == 81
