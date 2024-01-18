from imaplib import Int2AP
from pyteal import *
from pyteal.ast.bytes import Bytes



def approval():

    # The Base 64 Alphabet
    alphabet = Bytes("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")

    # WARNING - Dont like how big this number is...
    # Maximum allowable asynchronusity between Blockchain network's time to input time
    VALID_TIME = Int(50000000)
    TIMEOUT = Int(1000000)
    RANGE = Int(500)

    on_creation = Seq([
        # On contract deployment
        App.globalPut(Bytes("disaster_counter"), Int(0)),
        App.globalPut(Bytes("default_disaster_contract"), Btoi(Txn.application_args[0])),
        Approve(),
    ])

    # Asset customisable creation variables
    #asset_unit_name = ScratchVar(TealType.bytes)
    #asset_details = ScratchVar(TealType.bytes)
    #asset_url = ScratchVar(TealType.bytes)
    #asset_hash = ScratchVar(TealType.bytes)

    #input_method = ScratchVar(TealType.bytes)

    # Breaks down base10 int into base64 int
    #to_convert = (App.globalGet(Bytes("disaster_counter")))
    #a2 = to_convert%Int(4096)
    #a = (to_convert-a2)/Int(4096)
    #c = a2%Int(64)
    #b = (a2-c)/Int(64)

    #get_asset_unit_name = Seq([
    #    # Generates asset_unit_name using SpaceDAO id standard
    #    Assert(Len(Txn.application_args[1]) == Int(4)),
    #    # Create token id
    #    asset_unit_name.store(Concat(
    #        Bytes("A"),                             # The token type (Warning)
    #        Extract(alphabet, a, Int(1)), 
    #        Extract(alphabet, b, Int(1)), 
    #        Extract(alphabet, c, Int(1)),           # The unique warning number
    #        Txn.application_args[1],                # This should be satellite token id
    #    )),
    #    # Increment warning_counter by 1 - NEED TO IMPLEMENT OVERFLOW (RESET TO 0)
    #    App.globalPut(Bytes("disaster_counter"), (App.globalGet(Bytes("disaster_counter")) + Int(1))),
    #])


    contract_id = ScratchVar(TealType.uint64)

    appr_prog = ScratchVar(TealType.anytype)
    clear_prog = ScratchVar(TealType.anytype)
    gl_bytes = ScratchVar(TealType.uint64)
    gl_uint = ScratchVar(TealType.uint64)
    lo_bytes = ScratchVar(TealType.uint64)
    lo_uint = ScratchVar(TealType.uint64)

    contract_id = App.globalGet(Bytes("default_disaster_contract"))
    appr_prog_var = AppParam.approvalProgram(contract_id)
    clear_prog_var = AppParam.clearStateProgram(contract_id)
    gl_bytes_var = AppParam.globalNumByteSlice(contract_id)
    gl_uint_var = AppParam.globalNumUint(contract_id)
    lo_bytes_var = AppParam.localNumByteSlice(contract_id)
    lo_uint_var = AppParam.localNumUint(contract_id)

    default_disaster = Seq([
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

    custom_disaster = Seq([
        appr_prog.store(Gtxn[1].application_args[8]),
        clear_prog.store(Gtxn[1].application_args[9]),
        gl_bytes.store(Btoi(Gtxn[1].application_args[10])),
        gl_uint.store(Btoi(Gtxn[1].application_args[11])),
        lo_bytes.store(Btoi(Gtxn[1].application_args[12])),
        lo_uint.store(Btoi(Gtxn[1].application_args[13])),
    ])
    
    create_disaster_contract = Seq([
        #Assert(Int(0)),
        Cond(
            [Txn.application_args[7] == Bytes("default"), default_disaster],
            [Txn.application_args[7] == Bytes("custom"), custom_disaster],
        ),
        
        # Increment warning_counter by 1 - NEED TO IMPLEMENT OVERFLOW (RESET TO 0)
        App.globalPut(Bytes("disaster_counter"), App.globalGet(Bytes("disaster_counter")) + Int(1)),
        # Create Contract
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.ApplicationCall,
            TxnField.fee: Int(0),
            TxnField.approval_program: appr_prog.load(),
            TxnField.clear_state_program: clear_prog.load(),
            TxnField.global_num_byte_slices: gl_bytes.load(),
            TxnField.global_num_uints: gl_uint.load(),
            TxnField.local_num_byte_slices: lo_bytes.load(),
            TxnField.local_num_uints: lo_uint.load(),
            TxnField.application_args: [App.globalGet(Bytes("disaster_counter")),    # Disaster Number
                                        Gtxn[1].application_args[1],    # Timestamp
                                        Gtxn[1].application_args[2],    # Disaster Type
                                        Gtxn[1].application_args[3],    # Disaster Lat
                                        Gtxn[1].application_args[4],    # Disaster Lon
                                        Gtxn[1].application_args[5],    # IPFS URL
                                        Gtxn[1].application_args[6]],   # IPFS Hash
            TxnField.accounts: [ Txn.sender() ],
            TxnField.applications: [Global.current_application_id()],
        }),
        InnerTxnBuilder.Submit(),
        Approve(),

    ])


    # Main condition inputs
    handle_noop = Cond(
        [Txn.application_args[0] == Bytes("new_disaster"), create_disaster_contract],
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
        [Txn.application_id() == Int(0), on_creation],
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

def clear():
    return compileTeal(Approve(), Mode.Application, version=7)








#i = ScratchVar(TealType.uint64)
    #il = ScratchVar(TealType.uint64)

    # PROBLEM - COULD USER PUT DIFFERENT ACCOUNT IN A BREAK VALIDATION
    #asset_exist = AssetHolding.balance(Txn.accounts[1], Txn.assets[i.load()])
    #asset_name = AssetParam.name(Txn.assets[i.load()])


    #asset_time = Seq([
    #    asset_name,
    #    input_method.store(asset_name.value()),
    #])    

    #check_timed_out = Seq([
    #    # Check if any warnings have timed out
    #    il.store(Txn.assets.length()),
    #    For(i.store(Int(0)), i.load() < il.load(), i.store(i.load() + Int(1)))
    #    .Do(
    #        asset_exist,
    #        If(asset_exist.hasValue())
    #        .Then(
    #            asset_time,
    #            # CHANGE MINUS TO PLUS ------------- TESTING PURPOSE ONLY
    #            If(time - TIMEOUT < Global.latest_timestamp())
    #            .Then(
    #                InnerTxnBuilder.Begin(),
    #                InnerTxnBuilder.SetFields({
    #                    TxnField.type_enum: TxnType.AssetConfig,
    #                    TxnField.config_asset: Txn.assets[i.load()],
    #                }),
    #                InnerTxnBuilder.Submit(),
    #            ),
    #        ),
    #    ),
    #    Approve(),
    #])


    #check_part_disaster = Seq([
        # Check if any warnings are in radius of disasters

    #    Approve(),
    #])

    #create_new_disaster = Seq([
        # Consensus gained, new disaster being created

    #])


    #lat_total = ScratchVar(TealType.uint64)
    #lon_total = ScratchVar(TealType.uint64)
    #time_1 = ScratchVar(TealType.uint64)
    #lat_1 = ScratchVar(TealType.uint64)
    #lon_1 = ScratchVar(TealType.uint64)

    #get_data = Seq([
    #    asset_name,
    #    input_method.store(asset_name.value()),
    #    time_1.store(time),
    #    lat_1.store(lat),
    #    lon_1.store(lon),
    #])

    #add_data = Seq([
    #    lat_total.store(lat_total.load() + lat_1.load()),
    #    lon_total.store(lon_total.load() + lon_1.load()),
    #])

    #method_1 = Seq([
    #    asset_exist,
    #    Assert(asset_exist.hasValue()),
    #    get_data,
    #    add_data,
    #    # CHANGE MINUS TO PLUS ------------- TESTING PURPOSE ONLY
    #    Assert(time_1.load() - TIMEOUT <  Global.latest_timestamp()),
    #])


    #method_2 = Seq([
    #    get_data,
    #    # THIS IS WHERE REDS FANCY MATHS COMES IN
    #    Assert(And( lat_total.load() - RANGE <= lat_1.load(),
    #                lat_1.load() <= lat_total.load() + RANGE )),
    #    Assert(And( lon_total.load() - RANGE <= lon_1.load(),
    #                lon_1.load() <= lon_total.load() + RANGE )),
    #])


    #check_new_disaster = Seq([
    #    # Check if the remaining warnings produce a disaster
    #    Assert(Txn.assets.length() == Int(5)),
    #    il.store(Txn.assets.length()),
    #    lat_total.store(Int(0)),
    #    lon_total.store(Int(0)),
    #    For(i.store(Int(0)), i.load() < il.load(), i.store(i.load() + Int(1)))
    #    .Do(
    #        method_1,    
    #    ),
    #    For(i.store(Int(0)), i.load() < il.load(), i.store(i.load() + Int(1)))
    #    .Do(
    #        method_2,
    #    ),
    #    create_new_disaster,
    #    Approve(),
    #])

    #check_new_disaster = Seq([
        # Need to change to DiD input person rather than key input

        # If first warning in disaster check
    #    If(App.localGet(Int(0), Bytes("num_warnings")) == Int(0))
    #    .Then(
    #        App.localPut(Int(0), Bytes("lat"), AssetLat),
    #        App.localPut(Int(0), Bytes("lon"), AssetLon),
    #        App.localPut(Int(0), Bytes("time_start"), AssetTime),
    #        App.localPut(Int(0), Bytes("used_assets"), AssetID),
    #    # If warning in disaster check meets minimum threshold for confirmed disaster
    #    ).ElseIf(App.localGet(Int(0), Bytes("num_warnings")) >= Int(5))
    #    .Then(
    #        App.localPut(Int(0), Bytes("num_warnings"), Int(0)),
    #    # If warning is being added to current disaster check
    #    ).Else(
    #        App.localPut(Int(0), Bytes("lat"), App.localGet(Int(0)))
    #    ),


    #    Approve(),
    #])