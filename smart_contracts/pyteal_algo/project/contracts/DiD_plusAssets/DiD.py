from imaplib import Int2AP
from types import NoneType
from pyteal import *
from pyteal.ast.bytes import Bytes

# Current Issues:
# - Argument Passing to other contracts is not working/finished (multi value arrays need implemented into app_args)
# - Need assert for bytesslices for contract deployment
# - Do I need to add code for other major operation inputs, close-out, opt-in, etc...
# - Maybe add a local variable counter for how many users are connected to each DiD.

def approval_DiD():

    # Counter variables
    i = ScratchVar(TealType.uint64)
    il = ScratchVar(TealType.uint64)
    i2 = ScratchVar(TealType.uint64)
    il2 = ScratchVar(TealType.uint64)

    # On creation of the DiD instance
    # ? Args(bytes ("role"), bytes ("name"), bytes ("organisation"), bytes ("country"), bytes ("email"),)
    onCreation = Seq([
        App.globalPut(Bytes("creator"), Txn.sender()),
        App.globalPut(Bytes("lastDiD"), Int(1)),
        App.globalPut(Bytes("assetStorageTemplate"), Int(0)),
        Approve(),
    ])

    appr_prog = ScratchVar(TealType.anytype)
    clear_prog = ScratchVar(TealType.anytype)

    gl_bytes = ScratchVar(TealType.uint64)
    gl_uint = ScratchVar(TealType.uint64)
    lo_bytes = ScratchVar(TealType.uint64)
    lo_uint = ScratchVar(TealType.uint64)

    #Btoi(App.globalGet( Bytes("assetStorageTemplate") ))
    number = Btoi(App.globalGet(Bytes("assetStorageTemplate")))

    appr_prog_var = AppParam.approvalProgram(number)
    clear_prog_var = AppParam.clearStateProgram(number)
    gl_bytes_var = AppParam.globalNumByteSlice(number)
    gl_uint_var = AppParam.globalNumUint(number)
    lo_bytes_var = AppParam.localNumByteSlice(number)
    lo_uint_var = AppParam.localNumUint(number)

    assetStorageVar = Seq([
        appr_prog_var,
        clear_prog_var,
        gl_bytes_var,
        gl_uint_var,
        lo_bytes_var,
        lo_uint_var,
        appr_prog.store( appr_prog_var.value() ),
        clear_prog.store( clear_prog_var.value() ),
        gl_bytes.store( gl_bytes_var.value() ),
        gl_uint.store( gl_uint_var.value() ),
        lo_bytes.store( lo_bytes_var.value() ),
        lo_uint.store( lo_uint_var.value() ),
    ])

    newDeploy = Seq([
        appr_prog.store(Gtxn[1].application_args[1]),
        clear_prog.store(Gtxn[1].application_args[2]),
        gl_bytes.store(Btoi(Gtxn[1].application_args[3])),
        gl_uint.store(Btoi(Gtxn[1].application_args[4])),
        lo_bytes.store(Btoi(Gtxn[1].application_args[5])),
        lo_uint.store(Btoi(Gtxn[1].application_args[6])),
    ])

    # Deploys other smart contracts
    # Noop Args("deploy", approval_program, clear_program, global_bytes, global_ints, local_bytes, local_ints)
    deployCreate = Seq([
            Assert(App.localGet(Int(0), Bytes("approved")) == Int(1)),  # Checks if sender is approved

            # Assert that payment to DiD contract has been made
            Assert(Global.group_size() == Int(2)),
            Assert(Gtxn[0].type_enum() == TxnType.Payment),
            Assert(Gtxn[0].receiver() == Global.current_application_address()),
            Assert(Gtxn[0].amount() > Int(0)),
            Assert(Gtxn[0].sender() == Gtxn[1].sender()),

            # MAYBE ADD BACK IN ------------------ Assert that there are application arguments length is correct
            #Assert(Or(Txn.application_args.length() == Int(8), Txn.application_args.length() == Int(2))),

            # Allows for pre-built deployment of certain contracts
            Cond(
                # Deploy AssetStorage Contract
                [Txn.sender() == Global.creator_address(), newDeploy],
                [Txn.application_args[0] == Bytes("new"), assetStorageVar],
                #[Or( Txn.sender() == App.globalGet(Bytes("creator")), Txn.application_args[0] == Bytes("new") ), assetStorageVar],
                #[Btoi(App.globalGet(Bytes("assetStorageTemplate"))) != Int(0) , assetStorageVar],
                # Deploy Custom Contract
                [Int(1), newDeploy],
            ),

            # Contract Deployer
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.fee: Int(0),
                #TxnField.application_id: Int(0),
                #TxnField.on_completion: OnComplete.OptIn,
                TxnField.approval_program: appr_prog.load(),
                TxnField.clear_state_program: clear_prog.load(),
                TxnField.global_num_byte_slices: gl_bytes.load(),
                TxnField.global_num_uints: gl_uint.load(),
                TxnField.local_num_byte_slices: lo_bytes.load(),
                TxnField.local_num_uints: lo_uint.load(),
                #TxnField.application_args: [Gtxn[1].application_args[7]],
                TxnField.accounts: [ Txn.sender() ],
                TxnField.applications: [Global.current_application_id()],
            }),
            InnerTxnBuilder.Submit(),
            App.localPut(Int(0), Bytes("lastContract"), InnerTxn.created_application_id()),
    ])
    
    # Only called if creator address opts in
    firstDiD = Seq([
        App.localPut(Int(0), Bytes("id"), Int(1)),                  # creates first id
        App.localPut(Int(0), Bytes("approved"), Int(1)),            # approves first id
        App.localPut(Int(0), Bytes("role"), Bytes("ADM")),          # sets role name (Admin)
        App.localPut(Int(0), Bytes("approver"), Bytes("aaaa")),     # sets DiD to approver of all with special class aaaa
        App.localPut(Int(0), Bytes("org"), Bytes("robc")),          # sets organisation name (robc example)

        
        If((App.globalGet(Bytes("assetStorageTemplate"))) == Int(0))
        .Then(
            deployCreate,
            App.globalPut( Bytes("assetStorageTemplate"), (App.localGet(Int(0), Bytes("lastContract"))) ),
            Assert( (App.globalGet(Bytes("assetStorageTemplate"))) > Int(0) )
        ),
        App.localPut( Int(0), Bytes("assetStorageID"), (App.globalGet(Bytes("assetStorageTemplate"))) ),

        # Other data can be set here
        #App.globalPut(Bytes("creator"), Int(0)),
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
        deployCreate,
        App.localPut(Int(0), Bytes("assetStorageID"), Btoi(App.localGet(Int(0), Bytes("lastContract")))),
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

        App.localPut(Int(0), Bytes("assetStorageID"), App.localGet(Txn.accounts[1], Bytes("assetStorageID")))   # sets assetStorageID
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

            # Probably gonna need to change this code for double transaction code.
            # Maybe tripple to pay for asset creation on the other contract. (Check recieve funds, send funds, call contract)
            
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
    ])


    # Main condition inputs

    handle_noop = Seq([
        Cond(
            #[Txn.application_args[0] == op_changeData, changeData],

            [Txn.application_args[0] == Bytes("approveWallet"), approveDiD],
            [Txn.application_args[0] == Bytes("removeWallet"), removeDiD],

            [Txn.application_args[0] == Bytes("execute"), executeCall],
            [Txn.application_args[0] == Bytes("deploy"), deployCreate],
        ),
        Approve(),
    ])

    handle_optin = Seq([
        newDiD,
        Approve(),
    ])

    handle_closeout = Seq([
        # Call delete of assetStorage contract if not firstDiD
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

    return compileTeal(program, Mode.Application, version=7)

def clear_DiD():
    return compileTeal(Approve(), Mode.Application, version=7)