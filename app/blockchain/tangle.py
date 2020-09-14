import json
from iota import Iota, ProposedTransaction, Address, TryteString, Tag, Transaction, ProposedBundle, Hash
from iota.trits import trits_from_int
from app.blockchain.config import SEED, DEPTH, MIN_WEIGHT_MAGNITUDE, NODE_URL

txn_tag = "SCOIN"
value = 0

def send_transfer(data, receiver_address, seed = SEED):
    # Iota instance
    api = Iota(NODE_URL, seed)

    # Txn description
    txn = ProposedTransaction(
        address = Address(receiver_address),
        message = TryteString.from_string(json.dumps(data)),
        tag = Tag(txn_tag),
        value = value,
    )

    # Send transaction
    prepared_transferes = []
    bundle = ""
    prepared_transferes.append(txn)
    try:
        bundle = api.send_transfer(
            depth = DEPTH,
            transfers = prepared_transferes,
            min_weight_magnitude = MIN_WEIGHT_MAGNITUDE
        )
    except Exception as e:
        print(e)

    return bundle['bundle']

def send_transfers(data):
    # Iota instance
    api = Iota(NODE_URL, SEED)
    prepared_transferes = []

    for enseed, address in zip(data["enseed"], data["address"]):
        # Txn description
        txn = ProposedTransaction(
            address = Address(address),
            message = TryteString.from_string(json.dumps({
                "sen": data["sen"],
                "rev": data["rev"],
                "method": data["method"],
                "description": data["description"],
                "enseed": enseed,
                "address": address,
            })),
            tag = Tag(txn_tag),
            value = value,
        )

        prepared_transferes.append(txn)

    # Send transaction
    bundle = ""
    try:
        bundle = api.send_transfer(
            depth = DEPTH,
            transfers = prepared_transferes,
            min_weight_magnitude = MIN_WEIGHT_MAGNITUDE
        )
    except Exception as e:
        print(e)

    return bundle['bundle']

def find_transaction_message(hash_txn):
    # Iota instance
    api = Iota(NODE_URL)

    message = ""
    list_txn = []

    try:
        list_txn = api.get_trytes([hash_txn])
    except BaseException:
        return ""

    trytes_txn = str(list_txn['trytes'][0])
    txn = Transaction.from_tryte_string(trytes_txn)

    try:
        message = TryteString(txn.signature_message_fragment).decode()
    except BaseException:
        return ""

    return message

def get_txn_hash_from_bundle(hash_bundle):
    # Iota instance
    api = Iota(NODE_URL)

    obj_txn = api.find_transactions(bundles=[hash_bundle])
    return str(obj_txn['hashes'][0])

def generate_new_address(seed):
    # Iota instance
    api = Iota(NODE_URL, seed)
    address = api.get_new_addresses(count = None, index = None)
    
    return str(address["addresses"][0])

def get_account_data(seed):
    api = Iota(NODE_URL, seed)
    return api.get_account_data()
    # return api.get_balances()
    # return api.get_inputs()
