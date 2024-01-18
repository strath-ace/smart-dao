from imaplib import Int2AP
from pyteal import *
from pyteal.ast.bytes import Bytes
# from pyteal_helpers import *

# Handle each possible OnCompletion type. We don't have to worry about
# handling ClearState, because the ClearStateProgram will execute in that
# case, not the ApprovalProgram.

# This contract is deployed for every DiD instance.
# Therefore each DiD has a different app application ID.

# Current Issues:
# - Argument Passing to other contracts is not working/finished (multi value arrays need implemented into app_args)
# - Add validation that address' are real address'
# - Need assert for bytesslices for contract deployment
# - No validation for Role
# - Do I need to add code for other major operation inputs, close-out, opt-in, etc...
# - ------ If one user changes data, all other data for same id must change (Could make it so only way to join a id is if that id is approved (Dont know if this would fix problem, more thought required))


def approval_DiD():

    # Variables
    #App.globalPut(Bytes(""))
    #App.globalPut(Bytes("creator"), Int(1)),
    #isCreator = Txn.sender() == App.globalGet(Bytes("creator")),    # Checks if creator
    #hasDiD = App.localGet(Int(0), Bytes("id")) > Int(0) #Txn.sender() == Txn.accounts[0],                       # Checks if opted in    
    
    #hasDiD = Txn.sender() != Txn.accounts[0]

    i = ScratchVar(TealType.uint64)
    il = ScratchVar(TealType.uint64)
    i2 = ScratchVar(TealType.uint64)
    il2 = ScratchVar(TealType.uint64)









    # On creation of the DiD instance
    # ? Args(bytes ("role"), bytes ("name"), bytes ("organisation"), bytes ("country"), bytes ("email"),)
    onCreation = Seq([

        App.globalPut(Bytes("creator"), Txn.sender()),
        App.globalPut(Bytes("lastDiD"), Int(1)),

        Approve(),
    ])
    

    









    # Only called if creator address opts in
    firstDiD = Seq([
        App.localPut(Int(0), Bytes("id"), Int(1)),                  # creates first id
        App.localPut(Int(0), Bytes("approved"), Int(1)),            # approves first id
        App.localPut(Int(0), Bytes("role"), Bytes("ADM")),          # sets role name (Admin)
        App.localPut(Int(0), Bytes("approver"), Bytes("aaaa")),     # sets DiD to approver of all with special class aaaa
        App.localPut(Int(0), Bytes("org"), Bytes("robc")),          # sets organisation name (robc example)
        # Other data can be set here
        #App.globalPut(Bytes("creator"), Int(0)),
        Approve(),
    ])

    # Only called if new address opts in and asks for new DiD number
    createDiD = Seq([
        Assert(Txn.application_args.length() == Int(4)),

        # Check correct length of inputs
        Assert(Len(Txn.application_args[1]) == Int(3)),
        Assert(Len(Txn.application_args[2]) % Int(4) == Int(0)),
        Assert(Len(Txn.application_args[3]) == Int(4)),
        # Check organisation does not have aaaa or zzzz name
        Assert(Txn.application_args[3] != Bytes("aaaa")),
        Assert(Txn.application_args[3] != Bytes("zzzz")),

        App.globalPut(Bytes("lastDiD"), Btoi(App.globalGet(Bytes("lastDiD"))) + Int(1)),     # increments lastDiD by 1   NEED TO ADD OVERFLOW MATH
                    
        App.localPut(Int(0), Bytes("id"), Btoi(App.globalGet(Bytes("lastDiD")))),# creates new id
        App.localPut(Int(0), Bytes("approved"), Int(0)),            # sets approved to zero

        App.localPut(Int(0), Bytes("role"), Txn.application_args[1]),          # sets role name 3long
        App.localPut(Int(0), Bytes("approver"), Txn.application_args[2]),     # sets DiD approval 4multipleLong
        App.localPut(Int(0), Bytes("org"), Txn.application_args[3]),          # sets organisation name 4long
        Approve(),
    ])

    #addr = ScratchVar(TealType.bytes)

    # Only called if new address opts in and asks for old DiD number
    # Txn arg 0 should be the address of a target DiD to join
    joinDiD = Seq([
        Assert(Txn.application_args.length() == Int(1)),

        App.localPut(Int(0), Bytes("id"), App.localGet(Txn.accounts[1], Bytes("id"))),             # joins input id
        App.localPut(Int(0), Bytes("approved"), Int(0)),                        # sets approved to zero

        App.localPut(Int(0), Bytes("role"), App.localGet(Txn.accounts[1], Bytes("role"))),          # sets role name
        App.localPut(Int(0), Bytes("approver"), App.localGet(Txn.accounts[1], Bytes("approver"))),     # sets DiD approval
        App.localPut(Int(0), Bytes("org"), App.localGet(Txn.accounts[1], Bytes("org"))),          # sets organisation
        
        Approve(),
    ])

    # Called when opt in occurs
    newDiD = Cond(
        [Txn.sender() == App.globalGet(Bytes("creator")), firstDiD],
        [Txn.application_args[0] == Bytes("new"), createDiD],   # DONT LIKE THIS LINE (Means you need to input an DiD id when creating DiD, therefore have to guess the number....)
        [Txn.application_args[0] == Bytes("join"), joinDiD],
    )
    


    









    # CHANGE DATA POSES THREAT TO SECURITY
    # This problem occurs as a user can change their details and get approved accidently and they will have the same id as other people
    # using that DiD however the details will be mismatching.
    # Change data in DiD
    # Needs reapproval after data change
    #changeData = Seq([
    #    #Assert(hasDiD),             # assert that DiD exists
    #    Assert(Txn.application_args.length() == Int(4)),         #  assert that args is the correct length
    #    
    #    App.localPut(Int(0), Bytes("approved"), Int(0)),                        # sets approved to zero

        # Check correct length of inputs
    #    Assert(Len(Txn.application_args[1]) == Int(3)),
    #    Assert(Len(Txn.application_args[2]) % Int(4) == Int(0)),
    #    Assert(Len(Txn.application_args[3]) == Int(4)),
    #    # Check organisation does not have aaaa or zzzz name
    #    Assert(Txn.application_args[3] != Bytes("aaaa")),
    #    Assert(Txn.application_args[3] != Bytes("zzzz")),

    #    App.localPut(Int(0), Bytes("role"), Txn.application_args[1]),          # sets role name 3long
    #    App.localPut(Int(0), Bytes("approver"), Txn.application_args[2]),     # sets DiD approval 4multipleLong
    #    App.localPut(Int(0), Bytes("org"), Txn.application_args[3]),            # sets organisation name 4long
    #    Approve(),
    #])



    









    ## APPROVAL OF DiDs

    
    appr = ScratchVar(TealType.bytes)
    targetOrg = ScratchVar(TealType.bytes)

    # Approves new DiD without checks, as sender is admin
    adminApproveDiD = Seq([
        il.store( Txn.accounts.length() ),
        For(i.store(Int(1)), i.load() <= il.load(), i.store(i.load() + Int(1)))
        .Do(
            App.localPut(Txn.accounts[i.load()], Bytes("approved"), Int(1)),
        ),
        Approve(),
    ])

    # ---------- PROBLEM HERE - Need to make it so approvers cant become approvers for other organisations (FIXED)
    # Approves new DiD if the sender has organisation of new DiD in approver list
    regularApproveDiD = Seq([
        il.store( Txn.accounts.length() ),
        appr.store( App.localGet(Int(0), Bytes("approver")) ),    # Store approver variable in appr
        il2.store( Len(appr.load()) ),      # Store length of approver variable
        For(i.store(Int(1)), i.load() <= il.load(), i.store(i.load() + Int(1)))
        .Do(
            
            If( App.localGet(Int(0), Bytes("id")) == App.localGet(Txn.accounts[i.load()], Bytes("id")) )
            # If id of DiDs is the same as the senders
            .Then(
                # THESE IF STATEMENTS ARE NOT NECESSARY IF CHANGE DATA IS NOT A FUNCTIOn
                If(App.localGet(Int(0), Bytes("role")) != App.localGet(Txn.accounts[i.load()], Bytes("role"))).Then(Continue()),
                If(App.localGet(Int(0), Bytes("approver")) != App.localGet(Txn.accounts[i.load()], Bytes("approver"))).Then(Continue()),
                If(App.localGet(Int(0), Bytes("org")) != App.localGet(Txn.accounts[i.load()], Bytes("org"))).Then(Continue()),
                # Approve input account
                App.localPut(Txn.accounts[i.load()], Bytes("approved"), Int(1)),
            ).ElseIf(App.localGet(Int(0), Bytes("approver")) != Bytes("zzzz"))
            # Else run regular check
            .Then(
                If(App.localGet(Txn.accounts[i.load()], Bytes("approver")) == Bytes("aaaa")).Then(Continue()),  # A regular approver cannot approve a new admin
                targetOrg.store( App.localGet(Txn.accounts[i.load()], Bytes("org")) ),    # Store target organisation
                # Loops through approver list to find different organisations that sender can approve
                For(i2.store(Int(0)), i2.load() < il2.load(), i2.store(i2.load() + Int(4)))
                .Do(
                    # Assert input accounts organisation is within senders approval list
                    If( Extract(appr.load(), i2.load(), Int(4)) == targetOrg.load() )
                    .Then(
                        # Assert that input accounts approver and org variables match OR input accounts approver variable is zzzz (non approver)
                        If(Or( App.localGet(Txn.accounts[i.load()], Bytes("approver")) == targetOrg.load(),  App.localGet(Txn.accounts[i.load()], Bytes("approver")) == Bytes("zzzz") ))
                        .Then(
                            # Approve input account
                            App.localPut(Txn.accounts[i.load()], Bytes("approved"), Int(1)),
                        ),
                    ),
                ),
            ),
        ),
        Approve(),
    ])

    # Determine who is approving DiD and if they can approve the DiD
    approveDiD = Seq([
        #Assert(hasDiD),     # Checks if sender has DiD
        Assert(App.localGet(Int(0), Bytes("approved")) == Int(1)),  # Checks if sender is approved
        Cond(
            [App.localGet(Int(0), Bytes("approver")) == Bytes("aaaa"), adminApproveDiD],    # If sender is admin
            [Int(1), regularApproveDiD],     # Else
        ),
    ])


    
















    # REMOVAL OF DiDs (Unapproval)
    # Update for batch removals

    # Removes DiD without checks, as sender is admin
    adminRemoveDiD = Seq([
        il.store( Txn.accounts.length() ),
        For(i.store(Int(1)), i.load() <= il.load(), i.store(i.load() + Int(1)))
        .Do(
            App.localPut(Txn.accounts[i.load()], Bytes("approved"), Int(0)),
        ),
        Approve(),
    ])

    # Remove new DiD if the sender has organisation of new DiD in approver list
    regularRemoveDiD = Seq([
        il.store( Txn.accounts.length() ),
        appr.store( App.localGet(Int(0), Bytes("approver")) ),    # Store approver variable in appr
        il2.store( Len(appr.load()) ),      # Store length of approver variable
        For(i.store(Int(1)), i.load() <= il.load(), i.store(i.load() + Int(1)))
        .Do(
            If( App.localGet(Int(0), Bytes("id")) == App.localGet(Txn.accounts[i.load()], Bytes("id")) )
            # If id of DiDs is the same as the senders
            .Then(
                # Approve input account
                App.localPut(Txn.accounts[i.load()], Bytes("approved"), Int(0)),
            ).ElseIf(App.localGet(Int(0), Bytes("approver")) != Bytes("zzzz"))
            # Else run regular check
            .Then(
                If(App.localGet(Txn.accounts[i.load()], Bytes("approver")) == Bytes("aaaa")).Then(Continue()),  # A regular approver cannot remove an admin
                targetOrg.store( App.localGet(Txn.accounts[i.load()], Bytes("org")) ),    # Store target organisation
                # Loops through approver list to find different organisations that sender can remove
                For(i2.store(Int(0)), i2.load() < il2.load(), i2.store(i2.load() + Int(4)))
                .Do(
                    # Assert input accounts organisation is within senders approval list
                    If( Extract(appr.load(), i2.load(), Int(4)) == targetOrg.load() )
                    .Then(
                        # Unapprove input accounts DiD
                        App.localPut(Txn.accounts[i.load()], Bytes("approved"), Int(0)), 
                    ),
                ),
            ),
        ),
        Approve(),
    ])
    
    removeDiD = Seq([
        #Assert(hasDiD),     # Checks if sender has DiD
        Assert(App.localGet(Int(0), Bytes("approved")) == Int(1)),  # Checks if sender is approved
        Cond(
            [App.localGet(Int(0), Bytes("approver")) == Bytes("aaaa"), adminRemoveDiD],    # If sender is admin
            [Int(1), regularRemoveDiD],     # Else, regularRemoveDiD
        ),
    ])




    









    completionType = ScratchVar(TealType.anytype)




    ## DiD USAGE EXECUTE/CREATE CONTRACTS

    # Executes other smart contracts
    # Noop Args(execute, appID, Call Type, app2_args)
    executeCall = Seq([
            #Assert(hasDiD),     # Check sender has DiD
            Assert(App.localGet(Int(0), Bytes("approved")) == Int(1)),  # Checks if sender is approved
            Assert(Btoi(Txn.application_args[1]) > Int(0)),     # Check if Application to call is more than zero
            
            Assert(Txn.application_args.length() == Int(4)),
            ## Contract Executer
            # Determine contract call type
            Cond(
                [Txn.application_args[2] == Bytes("NoOp"), completionType.store(OnComplete.NoOp)],
                [Txn.application_args[2] == Bytes("OptIn"), completionType.store(OnComplete.OptIn)],
                [Txn.application_args[2] == Bytes("CloseOut"), completionType.store(OnComplete.CloseOut)],
                [Txn.application_args[2] == Bytes("UpdateApplication"), completionType.store(OnComplete.UpdateApplication)],
                [Txn.application_args[2] == Bytes("DeleteApplication"), completionType.store(OnComplete.DeleteApplication)],
            ),
            # Build txn
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.application_id: Txn.applications[1],
                TxnField.fee: Int(0),
                # Change this application_args[2] to a list of all values except 0,1,2               
                TxnField.application_args: [Txn.application_args[3]],
                TxnField.on_completion: completionType.load(),
                TxnField.accounts: [Txn.accounts[0]],
                TxnField.applications: [Global.current_application_id()],
            }),
            InnerTxnBuilder.Submit(),
            Approve(),
    ])



    # Deploys other smart contracts
    # Noop Args("deploy", approval_program, clear_program, global_bytes, global_ints, local_bytes, local_ints)
    deployCreate = Seq([
            Assert(App.localGet(Int(0), Bytes("approved")) == Int(1)),  # Checks if sender is approved

            # Assert that payment to DiD contract has been made
            Assert(Global.group_size() == Int(2)),
            Assert(Gtxn[0].type_enum() == TxnType.Payment),
            Assert(Gtxn[0].receiver() == Global.current_application_address()),
            Assert(Gtxn[0].amount() == Int(435500)),
            Assert(Gtxn[0].sender() == Gtxn[1].sender()),

            Assert(Txn.application_args.length() == Int(7)),

            # Contract Deployer
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.fee: Int(0),
                #TxnField.application_id: Int(0),
                #TxnField.on_completion: OnComplete.OptIn,
                TxnField.approval_program: Gtxn[1].application_args[1],
                TxnField.clear_state_program: Gtxn[1].application_args[2],
                TxnField.global_num_byte_slices: Btoi(Gtxn[1].application_args[3]),
                TxnField.global_num_uints: Btoi(Gtxn[1].application_args[4]),
                TxnField.local_num_byte_slices: Btoi(Gtxn[1].application_args[5]),
                TxnField.local_num_uints: Btoi(Gtxn[1].application_args[6]),
                # For the user id
                #Assert( App.localGet(Int(0), Bytes("id")) == Int(1) ),
                # ----------- NEED TO ADD THIS LINE BACK IN
                #TxnField.application_args: [ Txn.application_ ], #[Txn.application_args[6]],
                TxnField.accounts: [ Txn.sender() ],
                TxnField.applications: [Global.current_application_id()],
            }),
            InnerTxnBuilder.Submit(),
            App.localPut(Int(0), Bytes("lastContract"), InnerTxn.created_application_id()),
            Approve(),
    ])




    








    # Main condition inputs

    #op_changeData = Bytes("data")
    op_approveDiD = Bytes("approveWallet")
    op_removeDiD = Bytes("removeWallet")
    op_executeCall = Bytes("execute")
    op_deployCreate = Bytes("deploy")

    handle_noop = Cond(
        #[Txn.application_args[0] == op_changeData, changeData],

        [Txn.application_args[0] == op_approveDiD, approveDiD],
        [Txn.application_args[0] == op_removeDiD, removeDiD],

        [Txn.application_args[0] == op_executeCall, executeCall],
        [Txn.application_args[0] == op_deployCreate, deployCreate],
    )

    handle_optin = Seq([
        newDiD,
        Approve(),
    ])

    handle_closeout = Seq([
        Approve(),
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

def clear_DiD():
    return compileTeal(Approve(), Mode.Application, version=6)

