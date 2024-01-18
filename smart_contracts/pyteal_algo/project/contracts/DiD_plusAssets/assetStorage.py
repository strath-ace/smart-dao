from imaplib import Int2AP
from nturl2path import url2pathname
from unicodedata import name
from pyteal import *
from pyteal.ast.bytes import Bytes
# from pyteal_helpers import *

# A contract that creates, destroys and stores assets, which is linked to a single DiD

# Need to add local variables within DiD contract. That saves the assetStorage deployed app id.

def approval_assetStorage():
    
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
        # Assert DiD has data inside it
        Assert(DiD_id.hasValue()),
        Assert(DiD_approved.hasValue()),
        Assert(DiD_role.hasValue()),
        Assert(DiD_approver.hasValue()),
        Assert(DiD_org.hasValue()),
    ])


    unitName = ScratchVar(TealType.bytes)
    name = ScratchVar(TealType.bytes)
    _url = ScratchVar(TealType.bytes)
    _hash = ScratchVar(TealType.bytes)

    # Get data about input asset
    assetUnitName = AssetParam.unitName(Txn.assets[0])
    assetName = AssetParam.name(Txn.assets[0])
    assetURL = AssetParam.url(Txn.assets[0])
    assetHash = AssetParam.metadataHash(Txn.assets[0])
    # Assert data exists and compute about input asset
    getAssetData = Seq([
        assetUnitName,
        assetName,
        assetURL,
        assetHash,
        Assert(assetUnitName.hasValue()),
        #unitName.store(assetUnitName.value()),
        #name.store(assetName.value()),
        #_url.store(assetURL.value()),
        #_hash.store(assetHash.value()),
    ])


    # On deployment of the contract
    onCreation = Seq([
        # Add creators DiD id to CreatorID variable
        App.globalPut( Bytes("owner"), DiD_id.value() ),
        Approve(),
    ])


    duplicateAsset = Seq([
        # Compute previous asset data
        getAssetData,

        # Create new asset with same parameters as the input asset txn
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.fee: Int(0),
            TxnField.config_asset_total: Int(1),                    # Create unique ASA
            TxnField.config_asset_decimals: Int(0),                 # Not a currency so no need for decimals
            TxnField.config_asset_unit_name: assetUnitName.value(),           # Asset id (Satellite id (Unique))
            
            TxnField.config_asset_name: assetName.value(),              # Asset Name (Satellite Name)
            
            TxnField.config_asset_url: assetURL.value(),      # IPFS Link
            TxnField.config_asset_manager: Global.current_application_address(),    # Allows destroy to occur
            TxnField.config_asset_reserve: Bytes(""),
            TxnField.config_asset_freeze: Bytes(""),
            TxnField.config_asset_clawback: Bytes(""),
            TxnField.config_asset_metadata_hash: assetHash.value(),      # Hash of IPFS data for verification
        }),
        InnerTxnBuilder.Submit(),
        Approve(),

    ])


    # Creates new Asset
    # Args( function, BLANK DATA? MISSION ID? (unit_name 64bit), Asset Name (name 256bit), IPFS URL (URL 768 bytes), Data Hash (MetadataHash 256bit)  )
    createAsset = Seq([
        # Assert all items are filled out in asset (ie, not missing ipfs link etc)
        # Other assertions

        # Check correct amount of args
        Assert( Txn.application_args.length() == Int(5) ),
        
        # Make sure asset id is of correct length
        #Assert( Len(Txn.application_args[1]) == Int(8) ),


        # ID needs some sort of incrementer so duplicate asset IDs dont occur

        # Create new asset txn
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.fee: Int(0),
            TxnField.config_asset_total: Int(1),                    # Create unique ASA
            TxnField.config_asset_decimals: Int(0),                 # Not a currency so no need for decimals
            TxnField.config_asset_unit_name: Txn.application_args[1],           # Asset unit name (BLANK DATA?)
            TxnField.config_asset_name: Txn.application_args[2],              # Asset Name (Satellite Name)
            TxnField.config_asset_url: Txn.application_args[3],      # IPFS Link
            TxnField.config_asset_manager: Global.current_application_address(),    # Allows destroy to occur
            TxnField.config_asset_reserve: Bytes(""),
            TxnField.config_asset_freeze: Bytes(""),
            TxnField.config_asset_clawback: Bytes(""),
            TxnField.config_asset_metadata_hash: Txn.application_args[4],      # Hash of IPFS data for verification
        }),
        InnerTxnBuilder.Submit(),
        Approve(),
    ])


    # Destroys Asset
    destroyAsset = Seq([
        
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetConfig,
            # POTENTIAL ERROR Asset 0 or 1
            TxnField.config_asset: Txn.assets[1],
        }),
        InnerTxnBuilder.Submit(),

        Approve(),
    ])

    




    # Main condition inputs

    # Check owner is correct DiD then create, duplicate or destroy asset
    handle_noop = Seq([
        Cond(
            [Txn.application_args[0] == Bytes("createAsset"), createAsset],
            [Txn.application_args[0] == Bytes("duplicateAsset"), duplicateAsset],
            [Txn.application_args[0] == Bytes("destroyAsset"), destroyAsset],
        ),
        Approve(),
    ])

    # Maybe remove optin ability
    handle_optin = Seq([
        Approve(), # Return(Int(1))
    ])

    # Maybe remove closeout ability
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

            # Check that DiD is approved to continue
            [DiD_approved.value() != Int(1), Err()],
            # Check DiD id matches owner to continue
            [DiD_id.value() != App.globalGet(Bytes("owner")), Err()],

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

    return compileTeal(program, Mode.Application, version=7)

def clear_assetStorage():
    return compileTeal(Approve(), Mode.Application, version=7)

