import base64

from algosdk.future import transaction
from algosdk import account, mnemonic, logic, encoding
from algosdk.v2client import algod
from algosdk.logic import get_application_address
from algosdk.error import WrongChecksumError, WrongMnemonicLengthError, WrongKeyLengthError

# These are general functions for running smart contracts contracts

def compile_program(client, source_code):
    """
    @notice This function compiles smart contracts written in pyteal into TEAL
    @dev ---
    @param client The client/network that the contract is to be deployed on
    @param source_code The smart contract written in pyteal
    @return Smart Contract in TEAL
    """
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])



def wait_for_confirmation(client, transaction_id, timeout):
    """
    @notice This function pauses the terminal to allow for block production
    @dev ---
    @param client The client/network that the contract is to be deployed on
    @param transaction_id The unique id used to identify each transaction
    @param timeout The maximum number of blocks to wait for the transaction
        to complete before an error is thrown
    @return pending transaction information, or throws an error if the transaction
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



def exec_txn(client, txn, pKey):
    """
    @notice This function signs and executes 1 transaction on the network
    @dev ---
    @param client The client/network that the contract is to be deployed on
    @param txn The transaction created to execute
    @param pKey The private key of the sender
    @return txnData The transaction data produced
    """
    # Sign the transaction with the private key
    try:
        signed_txn = txn.sign(pKey)
        # Generates the transaction id
        tx_id = signed_txn.transaction.get_txid()
        # Sends transaction to the network
        client.send_transactions([signed_txn])
        # Wait for network to process transaction
        wait_for_confirmation(client, tx_id, 10)
        return client.pending_transaction_info(tx_id)
    except WrongChecksumError:
        return {"passphrase": "Checksum error"}
    except ValueError:
        return {"passphrase": "Unknown word in the passphrase"}
    except WrongMnemonicLengthError:
        return {"passphrase": "Incorrect size of the passphrase"}



def exec_gtxn(client, txns, pKey):
    """
    @notice This function signs and executes multiple transaction on the network
    @dev ---
    @param client The client/network that the contract is to be deployed on
    @param txn The transactions created to execute
    @param pKey The private key of the sender
    @return txnData The transaction data produced
    """
    # Creates group and group ids for transactions
    stxns = []
    gid = transaction.calculate_group_id(txns)
    for txn in txns:
        txn.group = gid
    # Sign the transaction with the private key
    for txn in txns:
        stxns.append(txn.sign(pKey))
    # Sends transaction to the network
    tx_id = client.send_transactions(stxns)
    # Wait for network to process transaction
    wait_for_confirmation(client, tx_id, 10)
    return client.pending_transaction_info(tx_id)


def read_all_assets(client, address):
    """
    @notice This function reads the assets in an app
    @dev ---
    @param client The client/network that the contract is to be deployed on
    @param address The address to search within
    @return asset_ids All asset ids of the assets in the address
    """
    asset_ids = []
    account_data = client.account_info(address)
    all_assets = account_data['assets']
    for asset in all_assets:
        asset_ids.append(asset['asset-id'])
    return asset_ids

def read_global_state(client, app_id): 
    """
    @notice This function reads the global state of an app
    @dev ---
    @param client The client/network that the contract is to be deployed on
    @param app_id The app ID to read the global state of
    @return appGlobalState The global state of the app in .json b64 format
    """
    results = client.application_info(app_id)
    appGlobalState = results['params']['global-state'] if "global-state" in results["params"] else []
    return appGlobalState



def read_local_state(client, pubKey, app_id): 
    """
    @notice This function reads the local state of an app for a specific user
    @dev ---
    @param client The client/network that the contract is to be deployed on
    @param pubKey The public key of the sender
    @param app_id The app ID to read the local state of
    @return appLocalState The local state of the app in .json b64 format
    """
    appLocalState = ""
    results = client.account_info(pubKey)
    localState = results['apps-local-state']
    for i in range (0,len(localState)):
        if localState[i]['id'] == app_id:
            appLocalState = localState[i]['key-value']
    return appLocalState


def read_key_all(state):
    """
    @notice This function reads states in .json b64 and outputs array in ascii
    @dev ---
    @param state The input state in .json b64
    @return output The input state in an array in ascii
    """
    output = []
    if state != "":
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



def read_key_specific(state, key):
    """
    @notice This function reads states in .json b64 and a specific key 
        and outputs the value at that key in ascii
    @dev ---
    @param state The input state in .json b64
    @param key The key at which the data is required
    @return output The data held at that key in ascii
    """
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


def contract_deployment(client, pKey, contract):
    """
    @notice This function deploys a smart contract
    @dev There is no allowance for extra parameters such as args or accounts
    @param client The client/network that the contract is to be deployed on
    @param pKey The private key of the sender
    @param contract An array of approval method, clear method, 
        global bytes, global ints, local bytes, local ints
    @return txnData The transaction data produced
    """
    # Get public key from input private key
    sendFromPublic = account.address_from_private_key(pKey)
    # Get default transaction parameters
    params = client.suggested_params()
    # Get approval and clear from Smart Contract
    compiledApproval = compile_program(client, contract[0])
    compiledClearstate = compile_program(client, contract[1])
    # Set Global and Local Schema
    globalSchema = transaction.StateSchema(contract[2], contract[3])
    localSchema = transaction.StateSchema(contract[4], contract[5])
    # Set condition for after contract deployed, what function is run
    on_complete = transaction.OnComplete.NoOpOC.real
    # Create transaction for contract deployment
    txn0 = transaction.ApplicationCreateTxn(sendFromPublic, 
                                            params, 
                                            on_complete, 
                                            compiledApproval, 
                                            compiledClearstate, 
                                            globalSchema, 
                                            localSchema)
    # Sign and execute transaction
    txnData = exec_txn(client, txn0, pKey)
    return txnData


def contract_deployment_with_args(client, pKey, contract, app_args, accounts, foregin_apps):
    """
    @notice This function deploys a smart contract
    @dev There is no allowance for extra parameters such as args or accounts
    @param client The client/network that the contract is to be deployed on
    @param pKey The private key of the sender
    @param contract An array of approval method, clear method, 
        global bytes, global ints, local bytes, local ints
    @param app_args Txn.application_args in smart contract
    @param accounts Txn.accounts in smart contract
    @param foregin_apps Txn.applications in smart contract
    @return txnData The transaction data produced
    """
    # Get public key from input private key
    sendFromPublic = account.address_from_private_key(pKey)
    # Get default transaction parameters
    params = client.suggested_params()
    # Get approval and clear from Smart Contract
    compiledApproval = compile_program(client, contract[0])
    compiledClearstate = compile_program(client, contract[1])
    # Set Global and Local Schema
    globalSchema = transaction.StateSchema(contract[2], contract[3])
    localSchema = transaction.StateSchema(contract[4], contract[5])
    # Set condition for after contract deployed, what function is run
    on_complete = transaction.OnComplete.NoOpOC.real
    # Create transaction for contract deployment
    txn0 = transaction.ApplicationCreateTxn(sendFromPublic, 
                                            params, 
                                            on_complete, 
                                            compiledApproval, 
                                            compiledClearstate, 
                                            globalSchema, 
                                            localSchema,
                                            app_args,
                                            accounts,
                                            foregin_apps)
    # Sign and execute transaction
    txnData = exec_txn(client, txn0, pKey)
    return txnData


def optin(client, pKey, app_id):
    """
    @notice 
    """
    # Get default transaction parameters
    params = client.suggested_params()
    # Details for Payment Transaction
    sendFromPublic = account.address_from_private_key(pKey)
    # Details for Optin Transaction
    app_args = []
    accounts = []
    foreign_apps = []
    # Create transactions for optin
    txn = transaction.ApplicationOptInTxn(sendFromPublic, 
                                           params,
                                           app_id, 
                                           app_args,
                                           accounts,
                                           foreign_apps)
    # Sign and execute group transaction
    txnData = exec_txn(client, txn, pKey)
    return txnData