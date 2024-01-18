from imaplib import Int2AP
from pyteal import *
from pyteal.ast.bytes import Bytes

# Generate and Store Warning Tokens

# Need a way to delete warning tokens

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
        App.globalPut(Bytes("warning_counter"), Int(0)),
        Approve(),
    ])

    # Asset customisable creation variables
    asset_unit_name = ScratchVar(TealType.bytes)
    asset_details = ScratchVar(TealType.bytes)
    asset_url = ScratchVar(TealType.bytes)
    asset_hash = ScratchVar(TealType.bytes)

    input_method = ScratchVar(TealType.bytes)

    # Breaks down base10 int into base64 int
    to_convert = (App.globalGet(Bytes("warning_counter")))
    a2 = to_convert%Int(4096)
    a = (to_convert-a2)/Int(4096)
    c = a2%Int(64)
    b = (a2-c)/Int(64)

    get_asset_unit_name = Seq([
        # Generates asset_unit_name using SpaceDAO id standard
        Assert(Len(Txn.application_args[1]) == Int(4)),
        # Create token id
        asset_unit_name.store(Concat(
            Bytes("A"),                             # The token type (Warning)
            Extract(alphabet, a, Int(1)), 
            Extract(alphabet, b, Int(1)), 
            Extract(alphabet, c, Int(1)),           # The unique warning number
            Txn.application_args[1],                # This should be satellite token id
        )),
        # Increment warning_counter by 1 - NEED TO IMPLEMENT OVERFLOW (RESET TO 0)
        App.globalPut(Bytes("warning_counter"), (App.globalGet(Bytes("warning_counter")) + Int(1))),
    ])

    # Format requirements for asset_name data
    time_1 = (Btoi(Extract(input_method.load(), Int(0), Int(1))) - Int(48)) *Int(1000000000)
    time_2 = (Btoi(Extract(input_method.load(), Int(1), Int(1))) - Int(48)) *Int(100000000)
    time_3 = (Btoi(Extract(input_method.load(), Int(2), Int(1))) - Int(48)) *Int(10000000)
    time_4 = (Btoi(Extract(input_method.load(), Int(3), Int(1))) - Int(48)) *Int(1000000)
    time_5 = (Btoi(Extract(input_method.load(), Int(4), Int(1))) - Int(48)) *Int(100000)
    time_6 = (Btoi(Extract(input_method.load(), Int(5), Int(1))) - Int(48)) *Int(10000)
    time_7 = (Btoi(Extract(input_method.load(), Int(6), Int(1))) - Int(48)) *Int(1000)
    time_8 = (Btoi(Extract(input_method.load(), Int(7), Int(1))) - Int(48)) *Int(100)
    time_9 = (Btoi(Extract(input_method.load(), Int(8), Int(1))) - Int(48)) *Int(10)
    time_10 = (Btoi(Extract(input_method.load(), Int(9), Int(1))) - Int(48))
    time = time_1+time_2+time_3+time_4+time_5+time_6+time_7+time_8+time_9+time_10
    disaster_type = Extract(input_method.load(), Int(10), Int(2))
    lat_a = (Btoi(Extract(input_method.load(), Int(12), Int(1))) - Int(48)) *Int(10000)
    lat_b = (Btoi(Extract(input_method.load(), Int(13), Int(1))) - Int(48)) *Int(1000)
    lat_c = (Btoi(Extract(input_method.load(), Int(14), Int(1))) - Int(48)) *Int(100)
    lat_d = (Btoi(Extract(input_method.load(), Int(15), Int(1))) - Int(48)) *Int(10)
    lat_e = (Btoi(Extract(input_method.load(), Int(16), Int(1))) - Int(48))
    lat = lat_a+lat_b+lat_c+lat_d+lat_e
    lon_a = (Btoi(Extract(input_method.load(), Int(17), Int(1))) - Int(48)) *Int(10000)
    lon_b = (Btoi(Extract(input_method.load(), Int(18), Int(1))) - Int(48)) *Int(1000)
    lon_c = (Btoi(Extract(input_method.load(), Int(19), Int(1))) - Int(48)) *Int(100)
    lon_d = (Btoi(Extract(input_method.load(), Int(20), Int(1))) - Int(48)) *Int(10)
    lon_e = (Btoi(Extract(input_method.load(), Int(21), Int(1))) - Int(48))
    lon = lon_a+lon_b+lon_c+lon_d+lon_e

    check_asset_details = Seq([
        # Check that asset_details scratch var has valid and complete information
        # Check is correct length
        Assert( Len(Txn.application_args[2]) == Int(22) ),
        input_method.store(Txn.application_args[2]),
        # Check input timestamp is correct
        Assert( And(Global.latest_timestamp() - VALID_TIME <= time,
                    time <= Global.latest_timestamp() + VALID_TIME)),
        # Check input disaster type is a real disaster type
        Assert( Or( disaster_type == Bytes("EQ"),    # Earthquake
                    disaster_type == Bytes("TC"),    # Tropical Cyclone/Storm
                    disaster_type == Bytes("FL"),    # Flood
                    disaster_type == Bytes("VO"),    # Volcanic Eruption/Activity
                    disaster_type == Bytes("DR"),    # Drought
                    disaster_type == Bytes("WF"))),  # Wild fire
        # Check input latitude and longitude are valid
        Assert( lat <= Int(18000) ),
        Assert( lon <= Int(36000) ),
        # NEED TO IMPLEMENT confidence and severity
    ])
       
    create_warning_token = Seq([
        # Create token for warning
        # Generate asset unit name
        get_asset_unit_name,
        # Gets all other required asset data
        check_asset_details,
        asset_details.store(Txn.application_args[2]),
        asset_url.store(Txn.application_args[3]),
        asset_hash.store(Txn.application_args[4]),
        # Create asset
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.fee: Int(0),
            TxnField.config_asset_total: Int(1),
            TxnField.config_asset_decimals: Int(0),
            TxnField.config_asset_unit_name: asset_unit_name.load(),
            TxnField.config_asset_name: asset_details.load(),
            TxnField.config_asset_url: asset_url.load(),
            TxnField.config_asset_manager: Global.current_application_address(),
            TxnField.config_asset_reserve: Global.zero_address(),
            TxnField.config_asset_freeze: Global.zero_address(),
            TxnField.config_asset_clawback: Global.zero_address(),
            TxnField.config_asset_metadata_hash: asset_hash.load(),
        }),
        InnerTxnBuilder.Submit(),
        Approve(),
    ])


    i = ScratchVar(TealType.uint64)
    il = ScratchVar(TealType.uint64)

    # PROBLEM - COULD USER PUT DIFFERENT ACCOUNT IN A BREAK VALIDATION
    asset_exist = AssetHolding.balance(Txn.accounts[1], Txn.assets[i.load()])
    asset_name = AssetParam.name(Txn.assets[i.load()])


    asset_time = Seq([
        asset_name,
        input_method.store(asset_name.value()),
    ])    

    check_timed_out = Seq([
        # Check if any warnings have timed out
        il.store(Txn.assets.length()),
        For(i.store(Int(0)), i.load() < il.load(), i.store(i.load() + Int(1)))
        .Do(
            asset_exist,
            If(asset_exist.hasValue())
            .Then(
                asset_time,
                # CHANGE MINUS TO PLUS ------------- TESTING PURPOSE ONLY
                If(time - TIMEOUT < Global.latest_timestamp())
                .Then(
                    InnerTxnBuilder.Begin(),
                    InnerTxnBuilder.SetFields({
                        TxnField.type_enum: TxnType.AssetConfig,
                        TxnField.config_asset: Txn.assets[i.load()],
                    }),
                    InnerTxnBuilder.Submit(),
                ),
            ),
        ),
        Approve(),
    ])



    # Main condition inputs
    handle_noop = Cond(
        [Txn.application_args[0] == Bytes("new_warning"), create_warning_token],
        [Txn.application_args[0] == Bytes("timed_out"), check_timed_out],
        #[Txn.application_args[0] == Bytes("part_of_disaster"), check_part_disaster],
        #[Txn.application_args[0] == Bytes("new_disaster"), check_new_disaster],
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
