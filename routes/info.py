from flask import request, Blueprint, jsonify
from db import transaction, user
from utils.user import get_total_user

info_blueprint = Blueprint('info', __name__)

@info_blueprint.route('/get_transactions_by_timestamp', methods=['GET'])
def get_transactions_by_timestamp():
    start = request.args.get("start")
    end = request.args.get("end")

    txns = transaction.select_by_timestamp(start, end)
    return jsonify(txns)


@info_blueprint.route('/get_users_by_timestamp', methods=['GET'])
def get_users_by_timestamp():
    start = request.args.get("start")
    end = request.args.get("end")

    users = user.select_by_timestamp(start, end)
    for u in users:
        u.pop("id", None)
        u.pop("password", None)

    return jsonify(users)

@info_blueprint.route('/info', methods=['GET'])
def info():
    ret = { "totalUser": get_total_user() }
    return jsonify(ret)

