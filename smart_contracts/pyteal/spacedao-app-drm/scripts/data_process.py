from .blockchain_general import *
from .blockchain_interaction import *
from datetime import datetime
import json

# These functions process data and call blockchain interactions in disaster_response


def new_drm_app_id(app_id_disaster_warnings, app_id_disaster_consensus):
    clean_file = {
        "app_id_disaster_warnings": app_id_disaster_warnings,
        "app_id_disaster_consensus": app_id_disaster_consensus
    }
    json_object = json.dumps(clean_file, indent=4)
    with open("app_data/contract_ids.json", "w") as f:
        f.write(json_object)


def setup_drm(client, pKey, contract_warnings, contract_consensus, contract_new_disaster):
    """
    @notice
    """
    txn_data1 = contract_deployment(client, pKey, contract_warnings)
    print("Warning Contract Deployed")
    txn_data2 = contract_deployment_with_args(client, pKey, contract_new_disaster, [0, "t", 0, 0, 0, 0, "t", "t"], [account.address_from_private_key(pKey)], None)
    print("Disaster Template Contract Deployed")
    txn_data3 = contract_deployment_with_args(client, pKey, contract_consensus, [txn_data2['application-index']], None, None)
    print("Consensus Contract Deployed")
    return (txn_data1, txn_data2)


def check_deployed():
    try:
        with open('app_data/contract_ids.json', "r") as f:
            app_data = json.load(f)
        if app_data['app_id_disaster_warnings'] == 0 or app_data['app_id_disaster_consensus'] == 0:
            return 1
        else:
            return 0
    except:
        new_drm_app_id(0, 0)
        return 1


def get_app_ids():
    try:
        with open('app_data/contract_ids.json', "r") as f:
            app_data = json.load(f)
        if app_data['app_id_disaster_warnings'] == 0 or app_data['app_id_disaster_consensus'] == 0:
            return 1, app_data['app_id_disaster_warnings'], app_data['app_id_disaster_consensus']
        else:
            return 0, app_data['app_id_disaster_warnings'], app_data['app_id_disaster_consensus']
    except:
        return 1, 0, 0






# CHECK TRUE FUNCTION
# Check if similar to a different disaster
# Check if your api agrees