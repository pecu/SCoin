from flask import request, Blueprint
from app.auth import check_permission
from app.cb import set_layer_1, remove_layer_1
from error import InvalidUsage

layer_blueprint = Blueprint('layer', __name__)

@layer_blueprint.route('/set_layer1', methods=['GET'])
def set_layer1():
    if request.method == 'GET':
        ## Authentication
        x_api_key = request.headers.get('X-API-key')
        if check_permission("cb", x_api_key) == False:
            raise InvalidUsage("Authentication fail", 403)

        ## Set layer-1
        username = request.args.get('username')
        if set_layer_1(username) == False:
            raise InvalidUsage("No such account or account already exist", 400)

    return "OK"

@layer_blueprint.route('/remove_layer1', methods=['DELETE'])
def remove_layer1():
    if request.method == 'DELETE':
        ## Authentication
        x_api_key = request.headers.get('X-API-key')
        if check_permission("cb", x_api_key) == False:
            raise InvalidUsage("Fail at removing layer1, Authentication fail", 403)
        username = request.args.get('username')
        try:
            outcome = remove_layer_1(username)
            if outcome == False:
               raise ValueError
        except ValueError:
            raise InvalidUsage("Username hasn't been set to layer1 yet, please assign to it first", 400)
    return 'Remove ' + username

