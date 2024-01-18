from imaplib import Int2AP
from pyteal import *
from pyteal.ast.bytes import Bytes



def approval():

    # The Base 64 Alphabet
    alphabet = Bytes("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")


    on_creation = Seq([
        # On contract deployment
        App.globalPut(Bytes("disaster_number"), Btoi(Txn.application_args[0])),
        App.globalPut(Bytes("disaster_creator"), Txn.accounts[1]),
        App.globalPut(Bytes("timestamp"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("disaster_type"), Txn.application_args[2]),
        App.globalPut(Bytes("lat"), Btoi(Txn.application_args[3])),
        App.globalPut(Bytes("lon"), Btoi(Txn.application_args[4])),
        App.globalPut(Bytes("ipfs_url"), Txn.application_args[5]),
        App.globalPut(Bytes("ipfs_hash"), Txn.application_args[6]),
        
        App.globalPut(Bytes("votes"), Int(0)),

        Approve(),
    ])




    # Main condition inputs
    handle_noop = Seq([
        #Assert(Btoi(App.globalGet(Bytes("votes"))) >= Int(3)),
        #[Txn.application_args[0] == Bytes("new_disaster"), create_disaster_token],
        Approve(),
    ])

    handle_optin = Seq([
        # Voting
        App.globalPut(Bytes("votes"), App.globalGet(Bytes("votes")) + Int(1)),
        Approve(),
    ])

    handle_closeout = Seq([
        # Unvoting
        If((App.globalGet(Bytes("votes")) >= Int(1)))
        .Then(App.globalPut(Bytes("votes"), App.globalGet(Bytes("votes")) + Int(1))),
        Approve(),
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