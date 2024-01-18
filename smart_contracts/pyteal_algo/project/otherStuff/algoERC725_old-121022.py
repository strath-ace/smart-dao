from pyteal import *
from pyteal.ast.bytes import Bytes
#from pyteal_helpers import program

# Handle each possible OnCompletion type. We don't have to worry about
# handling ClearState, because the ClearStateProgram will execute in that
# case, not the ApprovalProgram.

# This contract is deployed for every DiD instance.
# Therefore each DiD has a different app application ID.

# Current Issues:
# - Argument Passing to other contracts is not workings
# - Add validation that address' are real address'
# - Need assert for bytesslices for contract deployment
# - No validation for Role
# - Not sure if opt-in works
# - Do I need to add code for other major operation inputs, close-out, opt-in, etc...


def approval():
    # On creation of the DiD instance
    # ? Args(bytes ("role"), bytes ("name"), bytes ("organisation"), bytes ("country"), bytes ("email"),)
    onCreation = Seq([
        App.localPut(Int(0), Bytes("owner"), Int(1)),

        # Can change what information needs stored
        Assert(Txn.application_args.length() == Int(5)),
        App.globalPut(Bytes("role"), Txn.application_args[0]),
        App.globalPut(Bytes("name"), Txn.application_args[1]),
        App.globalPut(Bytes("organisation"), Txn.application_args[2]),
        App.globalPut(Bytes("country"), Txn.application_args[3]),
        App.globalPut(Bytes("email"), Txn.application_args[4]),
        Approve(),
    ])

    #global_owner = Bytes("owner")  # byteslice
    #global_counter = Bytes("counter")  # uint64
    # App.globalPut(Bytes("Mykey"), Int(50)),

    isOwner = Int(1) == App.localGet(Int(0), Bytes("owner"))

    op_executeCall = Bytes("execute")
    op_deployCreate = Bytes("deploy")
    op_addWallet = Bytes("addWallet")
    op_removeWallet = Bytes("removeWallet")
    op_changeData = Bytes("data")

    scratch_appId = ScratchVar(TealType.uint64)
    scratchAddress = ScratchVar(TealType.bytes)

    # Give new wallet address ownership rights to DiD
    # Noop Args(addWallet, address (address to add))
    addWallet = Seq(
        [
            scratchAddress.store(Txn.application_args[1]),
            # ADD VALIDATION - scratchAddress.load() == real address format
            Assert(Int(1) == Int(1)),
            # Add address to local owner - MUST HAVE OPTED IN BEFORE
            App.localPut(scratchAddress.load(), Bytes("owner"), Int(1)),
            Approve(),
        ]
    )

    # Removes wallet address from DiD instance
    # Noop Args(removeWallet, address (address to remove))
    removeWallet = Seq(
        [
            scratchAddress.store(Txn.application_args[1]),
            # ADD VALIDATION - scratchAddress.load() == real address format
            Assert(Int(1) == Int(1)),
            # Add address to local owner - MUST HAVE OPTED IN BEFORE
            App.localPut(scratchAddress.load(), Bytes("owner"), Int(0)),
            Approve(),
        ]
    )

    # Sets data within DiD
    # Noop Args(data, bytes ("role"), bytes ("name"), bytes ("organisation"), bytes ("country"), bytes ("email"))
    changeData = Seq(
        [
            Assert(Txn.application_args.length() == Int(6)),
            App.globalPut(Bytes("role"), Txn.application_args[1]),
            App.globalPut(Bytes("name"), Txn.application_args[2]),
            App.globalPut(Bytes("organisation"), Txn.application_args[3]),
            App.globalPut(Bytes("country"), Txn.application_args[4]),
            App.globalPut(Bytes("email"), Txn.application_args[5]),
            Approve(),
        ]
    )

    # Executes other smart contracts
    # Noop Args(execute, int (appID), Args(?))
    executeCall = Seq(
        [
            scratch_appId.store(Btoi(Txn.application_args[1])),
            Assert(scratch_appId.load() > Int(0)),
            ## Contract Executer
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.application_id: scratch_appId.load(),
                # Change this application_args[2] to a list of all values except 0 and 1                
                TxnField.application_args: [Txn.application_args[1], Txn.application_args[2]],
                TxnField.on_completion: OnComplete.NoOp,
            }),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )

    # Deploys other smart contracts
    # Noop Args(deploy, bytes[] (approvalScript), bytes[] (clearScript))
    deployCreate = Seq(
        [
            ## Contract Deployer
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.application_id: Int(0),
                # Takes two byte values for approval and clear programs
                # Need to add validation that these are bytes
                TxnField.application_args: [Txn.application_args[1], Txn.application_args[2]],
                TxnField.on_completion: OnComplete.NoOp,
            }),
            InnerTxnBuilder.Submit(),
            Approve(),
        ]
    )

    handle_noop = Cond(
        [Txn.application_args[0] == op_executeCall, executeCall],
        [Txn.application_args[0] == op_deployCreate, deployCreate],
        [Txn.application_args[0] == op_addWallet, addWallet],
        [Txn.application_args[0] == op_removeWallet, removeWallet],
        [Txn.application_args[0] == op_changeData, changeData],
        # If none of these evaluate as true, then Err() occurs
    )

    handle_optin = Seq([
        Approve(), # Return(Int(1))
    ])

    handle_closeout = Seq([
        Approve(), # Return(Int(1))
    ])

    handle_updateapp = Err()

    handle_deleteapp = Err()

    program = Cond(
        # If appID is zero create new contract
        [Txn.application_id() == Int(0), onCreation],
        # If not owner of app, return zero, end program
        [isOwner != Int(1), Return(isOwner)],
        # If no operation called, run main code
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        # If opt-in called,
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        # If close-out called,
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        # If update app called, error
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        # If delete app called, error
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp]
    )

    return program

def clear():
    return Approve()

#with open('algoERC725.teal', 'w') as f:
#    compiled = compileTeal(approval_program(), Mode.Application, version=6)
#    f.write(compiled)


# ERC725.sol brings ERC725XCore and ERC725YCore together
# ERC725X and ERC725Y are the ownership contracts of the core equivalent

# X Core
## Allows execution and deployement of other smart contracts

## executeCall
## (internal virtual)
## input
## - address to (The address on which call is executed)
## - uint256 value (The value to be sent with the call)
## - bytes memory data (The data to be sent with the call)
## process
## - Call smart contract @ address to with inputs data and value
## - Verify call result
## - emit executed(OPERATION_CALL, to, value, bytes4(data))
## output
## - bytes memory result (The data from the call)

## executeStaticCall
## (internal virtual)
## input
## - address to (The address on which staticCall is executed)
## - uint256 value (The value to be sent to the execute (MUST be 0)?)
## - bytes memory data (The data to be sent with the staticCall)
## process
## - require that value == 0 (SaticCall cannot transfer value)
## - call staticCall smart contract @ address to with input data
## - Verify call result
## - emit executed(OPERATION_STATICCALL, to, value, bytes4(data))
## output
## - bytes memory result (The data returned from staticCall)

## executeDelegateCall
## (internal virtual)
## input
## - address to (The address on which delegateCall is executed)
## - uint256 value (The value to be sent to the execute (MUST be 0)?)
## - bytes memory data (The data to be sent with the delegateCall)
## process
## - require that value == 0 (delegateCall cannot transfer value)
## - call delegateCall smart contract @ address to with input data
## - Verify call result
## - emit executed(OPERATION_STATICCALL, to, value, bytes4(data))
## output
## - bytes memory result (The data returned from delegateCall)

## deployCreate
## (internal virtual)
## input
## - address to (The address on which create is executed (Must be 0))
## - uint256 value (The value to be sent to the execute)
## - bytes memory data (The contract bytecode to deploy)
## process
## - require that address to == address(0)
## - require that bytecode does not have length 0 (check not empty)
## - create variable called contractAddress of type address
## - create smart contract returning the contractAddress
## - require contractAddress no longer == 0
## - abi encoded address of contractAddress variable
## - emit executed(OPERATION_STATICCALL, to, value, bytes4(data))
## output
## - bytes memory newContract (The address of the new contract as bytes)

## deployCreate2 - alternative deployment method
## (internal virtual)
## input
## - address to (The address on which create is executed (Must be 0))
## - uint256 value (The value to be sent to the execute)
## - bytes memory data (The contract bytecode to deploy)
## process
## - require that address to == address(0)
## - require that bytecode does not have length 0 (check not empty)
## - convert data from type 
## - create variable called contractAddress of type address
## - create smart contract returning the contractAddress
## - require contractAddress no longer == 0
## - abi encoded address of contractAddress variable
## - emit executed(OPERATION_STATICCALL, to, value, bytes4(data))
## output
## - bytes memory newContract (The address of the new contract as bytes)

# Y Core
## Allows storage of data

## https://pyteal.readthedocs.io/en/stable/state.html
## Relys on mapping between a key and data stored at that key

## getData single
## getData list
## setData single
## setData list
## uncheckedIncrement?

## ERC725.sol
# - Import Scripts
#       ERC165.sol
#       OwnableUnset.sol
#       ERC725XCore.sol
#       ERC725YCore.sol
# - Import Constants
#       _INTERFACEID_ERC725X
#       _INTERFACEID_ERC725Y
#       Both from constants.sol
# - Contract ERC725 is:
#       ERC725XCore
#       ERC725YCore
# - New Owner Function (Check owner address is real address (non-zero))
#       Set owner of ownableUnset to input newOnwer
# - Supports interface function (public, view, virtual, override, return bool)
#       if InterfaceId == _INTERFACEID_ERC725X OR
#       if InterfaceId == _INTERFACEID_ERC725Y OR
#       super.supportsInterface(interfaceId)

## ERC725XCore.sol
# - Import Scripts
#       IERC165.sol
#       IERC725X.sol
#       Create2.sol
#       Address.sol
#       BytesLib.sol  ???
#       ERC165.sol
#       OwnableUnset.sol
# - Import Constants
#       _INTERFACEID_ERC725X
#       OPERATION_CALL
#       OPERATION_DELEGATECALL
#       OPERATION_STATICCALL
#       OPERATION_CREATE
#       OPERATION_CREATE2
#       All from constants.sol
# - execute function (public payable virtual override onlyOwner returns(bytes memory)) (uint256 operation, address to, uint256 value, bytes memory data)
#       check "require" sender balance >= value, if not return insufficient balance message
#       if operation == OPERATION_CALL: return _executeCall(to, value, data)
#       if operation == OPERATION_CREATE: return _deployCreate(to, value, data)
#       if operation == OPERATION_CREATE: return _deployCreate2(to, value, data)
#       if operation == OPERATION_STATICCALL: return _executeStaticCall(to, value, data)
#       !HIGH RISK! Check sol doc if operation == OPERATION_DELEGATECALL: return _executeDelegateCall(to, value, data)
#       else: return "Unknown operation type"
# - Supports interface function (public, view, virtual, override, return bool) "Override function?"
#       if InterfaceId == _INTERFACEID_ERC725X OR
#       super.supportsInterface(interfaceId)
# - _executeCall function (internal vitural returns(bytes memory result)) (address to, uint256 value, bytes memory data)
#       ?? // solhint-disable avoid-low-level calls
#       to.call{}

## ERC725YCore.sol
