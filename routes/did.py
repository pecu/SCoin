from flask import request, Blueprint
from app.did import DID
from app.blockchain.tangle import find_transaction_message

did_blueprint = Blueprint('did', __name__)

@did_blueprint.route('/new_did', methods=['POST'])
def new_did():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')
        
        did = DID()
        hash_bundle = did.new_did(x_api_key, data)

        return str(hash_bundle)

@did_blueprint.route('/did', methods=['GET'])
def did():
    if request.method == 'GET':
        hash_did = request.args.get('hash')

        ## Read from blockchain
        content = find_transaction_message(hash_did)

    return content

@did_blueprint.route('/get_all_cluster', methods=['GET'])
def get_all_cluster():
    cluster = ""

    did = DID()
    cluster = did.get_cluster()

    return cluster
