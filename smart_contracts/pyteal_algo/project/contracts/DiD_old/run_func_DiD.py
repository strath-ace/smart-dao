import base64

from algosdk.future import transaction
from algosdk import account, mnemonic, logic, encoding
from algosdk.v2client import algod
from algosdk.logic import get_application_address

from contracts.erc725.algoERC725 import *






# Prints information about input accounts console
def printAccounts(client, acc1_pkey, acc2_pkey, acc3_pkey):
    acc1_pubkey = account.address_from_private_key(acc1_pkey)
    acc2_pubkey = account.address_from_private_key(acc2_pkey)
    acc3_pubkey = account.address_from_private_key(acc3_pkey)

    # Account Print Data
    print()
    print("--------------")
    print()
    print("Account 1")
    print("Public Key: {}".format(acc1_pubkey))
    print("Private Key: {}".format(acc1_pkey))

    acc1_info = client.account_info(acc1_pubkey)
    print("Account balance: {} microAlgos".format(acc1_info.get('amount')) + "\n")

    print()
    print("--------------")
    print()
    print("Account 2")
    print("Public Key: {}".format(acc2_pubkey))
    print("Private Key: {}".format(acc2_pkey))

    acc2_info = client.account_info(acc2_pubkey)
    print("Account balance: {} microAlgos".format(acc2_info.get('amount')) + "\n")

    print()
    print("--------------")
    print()
    print("Account 3")
    print("Public Key: {}".format(acc3_pubkey))
    print("Private Key: {}".format(acc3_pkey))

    acc3_info = client.account_info(acc3_pubkey)
    print("Account balance: {} microAlgos".format(acc3_info.get('amount')) + "\n")








# Compiles pyteal code into deployable format
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

# Waits for transaction to complete or reject
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))






# READ DATA FROM BLOCKCHAIN

# Reads all local state information at specific address and app id
def read_global_state(client, pkey, app_id): 
    addr = account.address_from_private_key(pkey)
    results = client.application_info(app_id)
    app_global_state = results['params']['global-state'] if "global-state" in results["params"] else []
    return app_global_state

# Reads all local state information at specific address and app id
def read_local_state(client, pkey, app_id): 
    addr = account.address_from_private_key(pkey)
    results = client.account_info(addr)
    local_state = results['apps-local-state']
    for i in range (0,len(local_state)):
        if local_state[i]['id'] == app_id:
            app_local_state = local_state[i]['key-value']
    return app_local_state

# Converts state json file into list
def read_key_all(state):
    output = []
    for i in range (0,len(state)):
        if state[i]['value']['type'] == 1:  # If byteslice is stored
            try:    # Try encoding into ascii
                output.append([ base64.b64decode(state[i]['key']).decode('ascii') , base64.b64decode(state[i]['value']['bytes']).decode('ascii')])
            except:
                try:    # Try encoding into 32 bit address
                    output.append([ base64.b64decode(state[i]['key']).decode('ascii') , encoding.encode_address(base64.b64decode(state[i]['value']['bytes'])) ])
                except:     # Just decode from 64 bit
                    output.append([ base64.b64decode(state[i]['key']).decode('ascii') , base64.b64decode(state[i]['value']['bytes']) ])
        else:   # If uint is stored
            output.append([ base64.b64decode(state[i]['key']).decode('ascii') , state[i]['value']['uint'] ])
    return output

# Outputs specific data at a key within the state json file
def read_key_specific(state, key):
    output = "no value stored at key"
    for i in range (0,len(state)):
        if base64.b64decode(state[i]['key']).decode('ascii')  == key:
            if state[i]['value']['type'] == 1:
                try:
                    output = base64.b64decode(state[i]['value']['bytes']).decode('ascii')
                except:
                    output = base64.b64decode(state[i]['value']['bytes'])
            elif state[i]['value']['type'] == 2:
                output = state[i]['value']['uint']            
    return output








# Deploys approval_program and clear_program to the client blockchain
def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema):

    sender = account.address_from_private_key(private_key)

    on_complete = transaction.OnComplete.NoOpOC.real

    params = client.suggested_params()

    txn = transaction.ApplicationCreateTxn(sender, params, on_complete,
                                        approval_program, clear_program,
                                        global_schema, local_schema)

    return exec_txn(client, txn, private_key)

# Opts In to the client blockchain
def optIn(client, private_key, app_id, app_args, accounts):

    public_key = account.address_from_private_key(private_key)

    params = client.suggested_params()

    txn = transaction.ApplicationOptInTxn(public_key, params,
                                        app_id, 
                                        app_args,
                                        accounts)

    return exec_txn(client, txn, private_key)

# Opts Out of the client blockchain
def closeOut(client, private_key, app_id):

    public_key = account.address_from_private_key(private_key)

    params = client.suggested_params()

    txn = transaction.ApplicationCloseOutTxn(public_key,
                                        params,
                                        app_id)

    return exec_txn(client, txn, private_key)

# Regular No Operation Call
def noopCall(client, private_key, app_id, app_args, accounts):

    public_key = account.address_from_private_key(private_key)

    params = client.suggested_params()

    if app_args[0] == "deploy":
        params.flat_fee = True
        params.fee = 3000
        
    txn = transaction.ApplicationNoOpTxn(public_key,
                                        params,
                                        app_id,
                                        app_args,
                                        accounts)

    return exec_txn(client, txn, private_key)



# Signs and executes the transaction
def exec_txn(client, txn, private_key):
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    client.send_transactions([signed_txn])
    wait_for_confirmation(client, tx_id, 10)
    return client.pending_transaction_info(tx_id)

# Atomic Transfer, sign multiple transactions
def exec_gtxn(client, txns, private_key):
    stxns = []
    gid = transaction.calculate_group_id(txns)
    for txn in txns:
        txn.group = gid
    for txn in txns:
        stxns.append(txn.sign(private_key))

    tx_id = client.send_transactions(stxns)

    wait_for_confirmation(client, tx_id, 10)
    return client.pending_transaction_info(tx_id)