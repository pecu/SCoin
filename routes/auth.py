from flask import request, Blueprint                                                                                          
from db import user
from app.auth import check_account
from error import InvalidUsage

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/import_account', methods = ['GET'])
def import_account():
    if request.method == 'GET':
        req_name = request.args.get('username')
        req_pwd = request.args.get('password')
        print(req_name)
        print(req_pwd)
        res = check_account(req_name, req_pwd)
        #0 => user doesn't exist
        #1 => user exist
        #2 => incorrect password
        if res == 0:
            raise InvalidUsage("Account not found", 404)
        if res == 2:
            raise InvalidUsage("Incorrect Password", 404)
        return 'Account authenticated';

