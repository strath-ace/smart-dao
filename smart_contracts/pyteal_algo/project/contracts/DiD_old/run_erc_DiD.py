import base64
from email.mime import application

from algosdk.future import transaction
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from algosdk.logic import get_application_address

from run_func import *

from contracts.erc725.algoERC725 import *

from contracts.erc725.verifyTestContract import *

def line(info):
    print()
    print("--------------  {}".format(info))
    print()




ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ALGOD_ADDRESS = "http://localhost:4001"

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)


# Account Setup
MNEMONIC1 = "never recall owner life soon upper animal conduct hurdle limb liar grit trip burst relax scan skin school identify laugh walnut belt fatal absorb forum"  # replace with your own mnemonic
MNEMONIC2 = "involve morning very ill biology field load lobster alarm drastic copper marble frost allow excuse check guitar jazz hole invest involve hair team about tribe"
MNEMONIC3 = "medal company divide inquiry access catch kitchen object rude what tail face recall omit emerge cry smile census odor deliver crane prefer clerk abstract forest"

acc1_pkey = mnemonic.to_private_key(MNEMONIC1)
acc2_pkey = mnemonic.to_private_key(MNEMONIC2)
acc3_pkey = mnemonic.to_private_key(MNEMONIC3)



printAccounts(algod_client, acc1_pkey, acc2_pkey, acc3_pkey)
# working





# FUNC 1
def transactionPractice(algod_client, acc1_pkey, acc2_pkey, acc3_pkey):
    # Transaction Practice
    sendFromPublic = account.address_from_private_key(acc1_pkey)
    sendFromPrivate = acc1_pkey
    sendToPublic = account.address_from_private_key(acc2_pkey)
    sendAmount = 10000000
    note = "Hello World".encode()

    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(sendFromPublic, params, sendToPublic, sendAmount, None, note)
    print("Sent {} algos from {} to {}".format((sendAmount*0.000001), sendFromPublic, sendToPublic))
    print(exec_txn(algod_client, unsigned_txn, sendFromPrivate))

#line("Send practice transaction")
# FUNC 1
#transactionPractice(algod_client, acc1_pkey, acc2_pkey, acc3_pkey)
# working





# FUNC 2
def contractDeployment(algod_client, acc1_pkey):
    # Contract Deployment
    compiled_approval = compile_program(algod_client, approval_DiD())
    compiled_clearstate = compile_program(algod_client, clear_DiD())

    global_schema = transaction.StateSchema(3, 3) # no ints or bytes stored in global or local state
    local_schema = transaction.StateSchema(5, 5)
    
    # Deploy Contracts
    createAppTxn = create_app(algod_client, acc1_pkey, compiled_approval, compiled_clearstate, global_schema, local_schema)
    app_id = createAppTxn['application-index']
    print(createAppTxn)

    return app_id

line("Deploy Contract")
# FUNC 2
# Deploy contract and return app_id
app_id = contractDeployment(algod_client, acc1_pkey)
# working
print(app_id)





# FUNC 3
def optin1(algod_client, acc1_pkey, app_id):
    user = acc1_pkey
    app_args = []
    accounts = []
    optinTxn = optIn(algod_client ,user, app_id, app_args, accounts)
    print(optinTxn)

line("Optin and create first DiD as creator")
# FUNC 3
# OPTIN as creator to create first DiD
optin1(algod_client, acc1_pkey, app_id)
#working
line("get state for acc1")
state = read_local_state(algod_client, acc1_pkey, app_id)
print(read_key_all(state))
#working




# FUNC 4
def optin2(algod_client, acc2_pkey, app_id):
    user = acc2_pkey
    app_args = ["new", "REQ", "ibms", "ibms"]
    accounts = []
    optinTxn = optIn(algod_client ,user, app_id, app_args, accounts)
    print(optinTxn)

# FUNC 5
def optin3(algod_client, acc3_pkey, app_id, acc2_pkey):
    user = acc3_pkey
    app_args = ["join"]
    accounts = [account.address_from_private_key(acc2_pkey)]
    optinTxn = optIn(algod_client ,user, app_id, app_args, accounts)
    print(optinTxn)

# FUNC 5.5
def optin4(algod_client, acc3_pkey, app_id):
    user = acc3_pkey
    app_args = ["new", "OPS", "ibms", "ibms"]
    accounts = []
    optinTxn = optIn(algod_client ,user, app_id, app_args, accounts)
    print(optinTxn)

# FUNC 6
def optout(algod_client, user, app_id):
    app_args = []
    accounts = []
    closeOutTxn = closeOut(algod_client ,user, app_id)
    print(closeOutTxn)











def fillDiDContract(algod_client, acc1_pkey, sendToPublic):
    # Transaction Practice
    sendFromPublic = account.address_from_private_key(acc1_pkey)
    sendFromPrivate = acc1_pkey
    #sendToPublic = account.address_from_private_key(acc2_pkey)
    sendAmount = 199000
    note = "Hello World".encode()

    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(sendFromPublic, params, sendToPublic, sendAmount, None, note)
    print("Sent {} algos from {} to {}".format((sendAmount*0.000001), sendFromPublic, sendToPublic))
    print(exec_txn(algod_client, unsigned_txn, sendFromPrivate))
#line("Send money from acc1 to DiD contra
# ct so that contract 2 can be deployed")

#fillDiDContract(algod_client, acc1_pkey, get_application_address(app_id))


def contract2Deployment(algod_client, user, app_id):
    compiled_approval = compile_program(algod_client, approval_verifyTest())
    compiled_clearstate = compile_program(algod_client, clear_verifyTest())
    app_args = ["deploy", compiled_approval, compiled_clearstate, 3, 3, 5, 5]
    accounts = []

    params = algod_client.suggested_params()
    
    # Payment Transaction
    sendFromPublic = account.address_from_private_key(user)
    sendToPublic = get_application_address(app_id)
    sendAmount = 435500
    note = "Hello World".encode()

    txn2 = transaction.PaymentTxn(sendFromPublic, params, sendToPublic, sendAmount, None, note)

    if app_args[0] == "deploy":
            params.flat_fee = True
            params.fee = 3000

    txn1 = transaction.ApplicationNoOpTxn(sendFromPublic,
                                        params,
                                        app_id,
                                        app_args,
                                        accounts)
    txn_data = exec_gtxn(algod_client, [txn2, txn1], user)
    state = read_local_state(algod_client, acc1_pkey, app_id)
    newApp_id = read_key_specific(state, "lastContract") 

    return (newApp_id, txn_data)

line("Deploy Contract 2 with DiD")
(newApp_id, stuff) = contract2Deployment(algod_client, acc1_pkey, app_id)
print(stuff)
print(newApp_id)
#working

def contract2Call(algod_client, user, app_id, app2_id):
    app_args = ["execute", 1, "NoOp", "The"]
    accounts = []
    applications = [app2_id]

    params = algod_client.suggested_params()
    
    # Payment Transaction
    sendFromPublic = account.address_from_private_key(user)
    #sendToPublic = get_application_address(app_id)
    #sendAmount = 435500
    #note = "Hello World".encode()

    #txn2 = transaction.PaymentTxn(sendFromPublic, params, sendToPublic, sendAmount, None, note)

    if app_args[0] == "deploy":
            params.flat_fee = True
            params.fee = 2000
    if app_args[0] == "execute":
            params.flat_fee = True
            params.fee = 2000

    txn1 = transaction.ApplicationNoOpTxn(sendFromPublic,
                                        params,
                                        app_id,
                                        app_args,
                                        accounts,
                                        applications)
    #return exec_gtxn(algod_client, [txn2, txn1], user)
    txn_data = exec_txn(algod_client, txn1, user)
    return txn_data

line("Call execute on contract 2 with DiD")
txn_data = contract2Call(algod_client, acc1_pkey, app_id, newApp_id)
print(txn_data)
    


#line("Optin and create new DiD acc2")
# FUNC 4
# Optin as acc2 and create another DiD
#optin2(algod_client, acc2_pkey, app_id)
#working

#line("Optin and join account 2's DiD")
# FUNC 5
# Optin as acc3 and join DiD for acc2
#optin3(algod_client, acc3_pkey, app_id, acc2_pkey)
#working

# FUNC 5.5
#line("Optin and create new DiD acc3")
#optin4(algod_client, acc3_pkey, app_id)

#line("get global state of app")
#g_state = read_global_state(algod_client, acc1_pkey, app_id)
#print(read_key_all(g_state))
#working

#line("get state for acc2")
#state = read_local_state(algod_client, acc2_pkey, app_id)
#print(read_key_all(state))
#working

#line("get state for acc3")
#state = read_local_state(algod_client, acc3_pkey, app_id)
#print(read_key_all(state))
#working

#line("read only org of state")
#print(read_key_specific(state, 'org'))

# Change data has been removed from the smart contract
def changeDataTest(algod_client, pkey, app_id):
    app_args = ["data", "DRM", "aqrt", "aqrt"]
    accounts = []
    noopTxn = noopCall(algod_client, pkey, app_id, app_args, accounts)
    print(noopTxn)
# Currently removed from system
#line("change data")
#changeDataTest(algod_client, acc2_pkey, app_id)

# Test that admin can approve 2 accounts in 1 transaction (WORKING)
def adminApproveDoubleTest(algod_client, pkey, app_id, pkey2, pkey3):
    app_args = ["approveWallet"]
    accounts = [account.address_from_private_key(pkey2), account.address_from_private_key(pkey3)]
    noopTxn = noopCall(algod_client, pkey, app_id, app_args, accounts)
    print(noopTxn)
#line("approval of acc2 and acc3 by acc1 (who is an admin)")
#adminApproveDoubleTest(algod_client, acc1_pkey, app_id, acc2_pkey, acc3_pkey)

# Tests approval of DiD with same id as sender works (WORKING)
# Test that admin can approve 1 account (WORKING)
def adminApproveTest(algod_client, pkey, app_id, pkey2):
    app_args = ["approveWallet"]
    accounts = [account.address_from_private_key(pkey2)]
    noopTxn = noopCall(algod_client, pkey, app_id, app_args, accounts)
    print(noopTxn)
#line("approval of acc2 by acc1 (who is an admin)")
#adminApproveTest(algod_client, acc1_pkey, app_id, acc2_pkey)
# Test that admin can approve a DiD with the same id as sender (WORKING)
def regularApproveTest(algod_client, pkey2, app_id, pkey3):
    app_args = ["approveWallet"]
    accounts = [account.address_from_private_key(pkey3)]
    noopTxn = noopCall(algod_client, pkey2, app_id, app_args, accounts)
    print(noopTxn)
#line("approval of acc3 by acc2 (Who are same DiD org)")
#regularApproveTest(algod_client, acc2_pkey, app_id, acc3_pkey)


def adminApproveTest(algod_client, pkey, app_id, pkey2):
    app_args = ["approveWallet"]
    accounts = [account.address_from_private_key(pkey2)]
    noopTxn = noopCall(algod_client, pkey, app_id, app_args, accounts)
    print(noopTxn)
# First approve acc2
#line("approval of acc2 by acc1 (who is an admin)")
#adminApproveTest(algod_client, acc1_pkey, app_id, acc2_pkey)

#line("get state for acc2")
#state = read_local_state(algod_client, acc2_pkey, app_id)
#print(read_key_all(state))
#working

#line("get state for acc3")
#state = read_local_state(algod_client, acc3_pkey, app_id)
#print(read_key_all(state))
#working


def adminRemoveTest(algod_client, pkey, app_id, pkey2, pkey3):
    app_args = ["removeWallet"]
    accounts = [account.address_from_private_key(pkey2), account.address_from_private_key(pkey3)]
    noopTxn = noopCall(algod_client, pkey, app_id, app_args, accounts)
    print(noopTxn)
# Then unapprove acc2 by admin (acc1)
#line("unapproval of acc2 by acc1 (who is an admin)")
#adminRemoveTest(algod_client, acc1_pkey, app_id, acc2_pkey, acc3_pkey)

def regularRemoveTest(algod_client, pkey2, app_id, pkey3):
    app_args = ["removeWallet"]
    accounts = [account.address_from_private_key(pkey3)]
    noopTxn = noopCall(algod_client, pkey2, app_id, app_args, accounts)
    print(noopTxn)
#line("Remove acc3 by acc2 using regular remove test")
#regularRemoveTest(algod_client, acc2_pkey, app_id, acc3_pkey)

#line("get state for acc2")
#state = read_local_state(algod_client, acc2_pkey, app_id)
#print(read_key_all(state))
#working

#line("get state for acc3")
#state = read_local_state(algod_client, acc3_pkey, app_id)
#print(read_key_all(state))
#working














#line("All accounts optout")

#optout(algod_client, acc1_pkey, app_id)
#optout(algod_client, acc2_pkey, app_id)
#optout(algod_client, acc3_pkey, app_id)





