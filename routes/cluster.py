from flask import request, Blueprint
from app.cluster import check_alliance, bridge_cluster

cluster_blueprint = Blueprint('cluster', __name__)

## Bridge
#### Different backbone:
#### 1. Use API to bridge accounts
#### 1-1. Customer API should refer the new_did API
#### 2. Re-issue token by this API
#### Same backbone:
#### 1. Use this API to new DID reference
#### 2. Re-issue token by this API

# Clutser: Layer-1 or 2 ?
#          layer-2: Currency issue
@cluster_blueprint.route('/bridge', methods=['POST'])
def bridge():
    if request.method == 'POST':
        data = request.get_json()
        x_api_key = request.headers.get('X-API-key')

        # Chcek permission for customer CB
        if not check_alliance(data["name"], x_api_key):
            raise InvalidUsage("Not in the alliance", 400)

        # Bridge cluster
        result = bridge_cluster(data)

        return result

