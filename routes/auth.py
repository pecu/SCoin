from flask import request, Blueprint                                                                                          
from db import user
from app.auth import check_account
from error import InvalidUsage

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/import_account', methods = ['POST'])
def import_account():
    if request.method == 'POST':
        data = request.get_json()
        req_name = data['name']
        x_api_key = request.headers.get('X-API-key')
        res = check_account(req_name, x_api_key)
        if res == 0:
            raise InvalidUsage("Account not found", 403)
        if res == 2:
            raise InvalidUsage("Incorrect api key", 403)
        return 'Account authenticated';

