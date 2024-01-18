from imaplib import Int2AP
from pyteal import *
from pyteal.ast.bytes import Bytes
# from pyteal_helpers import *



def approval_verifyTest():
    
    # Get DiD Information
    DiD_id = App.localGetEx( Txn.accounts[1] , [Global.caller_app_id()][0], Bytes("id") )
    DiD_approved = App.localGetEx( Txn.accounts[1] , [Global.caller_app_id()][0], Bytes("approved") )
    DiD_role = App.localGetEx( Txn.accounts[1] , [Global.caller_app_id()][0], Bytes("role") )
    DiD_approver = App.localGetEx( Txn.accounts[1] , [Global.caller_app_id()][0], Bytes("approver") )
    DiD_org = App.localGetEx( Txn.accounts[1] , [Global.caller_app_id()][0], Bytes("org") )

    # Checks DiD data exists and that DiD is approved
    checkDiD = Seq([
        # Get data from DiD sender
        DiD_id,
        DiD_approved,
        DiD_role,
        DiD_approver,
        DiD_org,
        # Assert DiD is approved
        Assert(DiD_approved.hasValue()),
        Assert(DiD_approved.value()),
        # Assert DiD has data inside it
        Assert(DiD_id.hasValue()),
        Assert(DiD_approved.hasValue()),
        Assert(DiD_role.hasValue()),
        Assert(DiD_approver.hasValue()),
        Assert(DiD_org.hasValue()),
    ])



    onCreation = Seq([
        # Add creators DiD id to CreatorID variable
        App.globalPut( Bytes("CreatorID"), DiD_id.value()),
        
        
        Approve(),
    ])




    # Main condition inputs

    handle_noop = Seq([
        #[Txn.application_args[0] == op_changeData, changeData],
        Approve(),
    ])

    handle_optin = Seq([
        Approve(), # Return(Int(1))
    ])

    handle_closeout = Seq([
        Approve(), # Return(Int(1))
    ])

    handle_updateapp = Err()

    handle_deleteapp = Err()



    

    program = Seq([
        # Assert this contract is called from a contract
        Assert(Global.caller_app_id() > Int(0)),
        # Assert that the DiD contract that is currently calling this contract is its creator
        Assert(Global.creator_address() == Global.caller_app_address()),
        # Checks DiD data exists and that DiD is approved
        checkDiD,

        # Run input conditions
        Cond(
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
            [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        )
    ])

    return compileTeal(program, Mode.Application, version=6)

def clear_verifyTest():
    return compileTeal(Approve(), Mode.Application, version=6)

