from .blockchain_general import *
from datetime import datetime

# These functions create transactions in disaster_response process


def new_warning(client, pKey, app_id, data):
    """
    @notice 
    """
    # Get default transaction parameters
    params = client.suggested_params()
    # Details for Payment Transaction
    sendFromPublic = account.address_from_private_key(pKey)
    sendToPublic = get_application_address(app_id)
    sendAmount = 300000     # This is the minimum amount for a new asset (Check for future assets)
    # Create Payment Transaction
    txn0 = transaction.PaymentTxn(sendFromPublic, params, sendToPublic, sendAmount)
    # Cover all fees throughout current transaction
    params.flat_fee = True
    params.fee = 10000
    # Details for NoOp Transaction
    current_time = round(datetime.timestamp(datetime.now()))
    app_args = ["new_warning", data.data_provider_code, str(current_time)+data.event_type+str(data.lat)+str(data.lon), data.url, data.url_hash]
    accounts = []
    foreign_apps = []
    foreign_assets = []
    # Create NoOp Transaction
    txn1 = transaction.ApplicationNoOpTxn(sendFromPublic, params, app_id, app_args, accounts, foreign_apps, foreign_assets)
    # Sign and execute group transaction
    txn_data = exec_gtxn(client, [txn0, txn1], pKey)
    return txn_data



def new_disaster(client, pKey, app_id, disaster_args):
    """
    @notice 
    """
    # Get default transaction parameters
    params = client.suggested_params()
    # Details for Payment Transaction
    sendFromPublic = account.address_from_private_key(pKey)
    sendToPublic = get_application_address(app_id)
    sendAmount = 300000     # This is the minimum amount for a new asset (Check for future assets)
    # Create Payment Transaction
    txn0 = transaction.PaymentTxn(sendFromPublic, params, sendToPublic, sendAmount)
    # Cover all fees throughout current transaction
    params.flat_fee = True
    params.fee = 10000
    # Details for NoOp Transaction
    app_args = ["new_disaster", disaster_args[0], disaster_args[1], disaster_args[2], disaster_args[3], disaster_args[4], disaster_args[5], "default"]
    print(app_args)
    accounts = []
    foreign_apps = []
    foreign_assets = []
    # Create NoOp Transaction
    txn1 = transaction.ApplicationNoOpTxn(sendFromPublic, params, app_id, app_args, accounts, foreign_apps, foreign_assets)
    # Sign and execute group transaction
    txn_data = exec_gtxn(client, [txn0, txn1], pKey)
    return txn_data


def timed_out(client, pKey, app_id):
    """
    @notice 
    """
    # Get default transaction parameters
    params = client.suggested_params()
    # Details for Payment Transaction
    sendFromPublic = account.address_from_private_key(pKey)
    # Get all assets in this contract
    # Maybe close asset leftover money to sender?
    asset_ids = read_all_assets(client, get_application_address(app_id))
    # Cover all fees throughout current transaction
    params.flat_fee = True
    params.fee = 10000
    # Application variables
    app_args = ["timed_out"]
    accounts = [get_application_address(app_id)]
    foreign_apps = []
    # Creates return file
    txn_data = []
    # Divides assets into groups of 3 or less and runs timed_out
    i = 0
    for i in range(len(asset_ids)):
        if i%3 == 0:
            if i != 0:
                # Create NoOp Transaction
                txn = transaction.ApplicationNoOpTxn(sendFromPublic, params, app_id, app_args, accounts, foreign_apps, foreign_assets)
                txn_data.append(exec_txn(client, txn, pKey))
            foreign_assets = []
        foreign_assets.append(asset_ids[i])
    if len(asset_ids)%3 != 3:
        txn = transaction.ApplicationNoOpTxn(sendFromPublic, params, app_id, app_args, accounts, foreign_apps, foreign_assets)
        txn_data.append(exec_txn(client, txn, pKey))
    # Return all txn_data from all transactions
    return txn_data