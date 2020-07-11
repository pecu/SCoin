from flask import request, Blueprint
from app.token import layer_to_layer, check_token_valid, get_user_balance, \
        get_txn_enseed, snapshot
from app.auth import check_permission
from utils.user import user_exist
from error import InvalidUsage

token_blueprint = Blueprint('token', __name__)

@token_blueprint.route('/send_token', methods=['POST'])
def send():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        if not user_exist(data["sen"]):
            raise InvalidUsage("Sender does not exist.", 404)

        # Permission check
        if check_permission(data["sen"], x_api_key) == False:
            raise InvalidUsage("Permission deny.", 403)

        # Transaction
        result = layer_to_layer(x_api_key, data)

    return result

@token_blueprint.route('/verify_token', methods=['POST'])
def verify_token():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Permission check
        if check_permission(data["user"], x_api_key) == False:
            raise InvalidUsage("Permission deny", 403)
        
        # Verify token
        if check_token_valid(data["user"], x_api_key, data) == True:
            return {"status":"valid"}
        else:
            raise InvalidUsage("Token invalid", 400)

@token_blueprint.route('/get_balance', methods=['GET'])
def get_balance():
    txn_hashes = get_user_balance(request.args.get('user'))
    return "\n".join(txn_hashes)

@token_blueprint.route('/get_enseed', methods=['GET'])
def get_enseed():
    enseed = get_txn_enseed(request.args.get('hash'))
    return enseed

@token_blueprint.route('/snapshot', methods=['POST'])
def snapshot_token():
     if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Permission check
        if check_permission(data["user"], x_api_key) == False:
            raise InvalidUsage("Permission deny", 403)
        
        # snapshot
        txn_hash = snapshot(x_api_key, data)

        return txn_hash
