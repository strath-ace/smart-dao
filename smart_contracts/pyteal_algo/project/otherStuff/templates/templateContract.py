from imaplib import Int2AP
from pyteal import *
from pyteal.ast.bytes import Bytes
# from pyteal_helpers import *



def approval():

    #App.globalPut(Bytes("key"), Bytes("Value"))
    #i = ScratchVar(TealType.uint64)
    #il = ScratchVar(TealType.uint64)
    #i2 = ScratchVar(TealType.uint64)
    #il2 = ScratchVar(TealType.uint64)

    onCreation = Seq([

        Approve(),
    ])
       

    # Main condition inputs

    #op_executeCall = Bytes("execute")
    #op_deployCreate = Bytes("deploy")

    handle_noop = Cond(
        #[Txn.application_args[0] == op_executeCall, executeCall],
        #[Txn.application_args[0] == op_deployCreate, deployCreate],
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

    return compileTeal(program, Mode.Application, version=6)

def clear():
    return compileTeal(Approve(), Mode.Application, version=6)

