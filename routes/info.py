from flask import request, Blueprint, jsonify
from db import transaction, user
from utils.user import get_total_user

info_blueprint = Blueprint('info', __name__)

@info_blueprint.route('/get_transactions_by_timestamp', methods=['GET'])
def get_transactions_by_timestamp():
    start = request.args.get("start")
    end = request.args.get("end")

    txns = transaction.select_by_timestamp(start, end)
    filtered_txns = []

    for txn in txns:
        obj = {
                "hash": txn["hash"],
                "sender": txn["sender"],
                "receiver": txn["receiver"],
                "description": txn["description"],
                "timestamp": txn["timestamp"],
                "spent": txn["spent"]
              }
        filtered_txns.append(obj)

    return jsonify(filtered_txns)


@info_blueprint.route('/get_users_by_timestamp', methods=['GET'])
def get_users_by_timestamp():
    start = request.args.get("start")
    end = request.args.get("end")

    users = user.select_by_timestamp(start, end)
    filtered_users = []

    for usr in users:
        obj = {
                "username": usr["name"],
                "hash": usr["hash"],
                "created_at": usr["created_at"],
                "description": usr["description"]
              }
        filtered_users.append(obj)

    return jsonify(filtered_users)

@info_blueprint.route('/info', methods=['GET'])
def info():
    ret = { "totalUser": get_total_user() }
    return jsonify(ret)

