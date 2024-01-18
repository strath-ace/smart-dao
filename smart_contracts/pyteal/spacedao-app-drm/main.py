from typing import Union
from typing import Optional
from fastapi import  FastAPI

import csv

from algosdk import account, encoding, mnemonic
from algosdk.future.transaction import PaymentTxn, ApplicationNoOpTxn
from algosdk.future.transaction import AssetConfigTxn
from algosdk.error import WrongChecksumError, WrongMnemonicLengthError, WrongKeyLengthError, AlgodHTTPError
from algosdk.v2client import algod, indexer

# For data from web api
from urllib.request import urlopen
import json

from scripts.schemes import *

# API Functions
from scripts.blockchain_general import *
from scripts.blockchain_interaction import *
from scripts.data_process import *

# Smart Contracts
from contracts import disaster_warnings, disaster_consensus, disaster_basic_template

# Run script with:
# uvicorn main:app --reload

# Initialise algod client
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ALGOD_ADDRESS = "http://localhost:4001"
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# Initialise Indexer
indexer_client = indexer.IndexerClient("","http://localhost:8980")

# Create application instance
app = FastAPI()

disaster_types = ["EQ", "TC", "FL", "VO", "DR", "WF"]

# THESE ARE THE INTERFACE FUNCTIONS

def get_key(key):
    if key.mnemonic == "string":
        try:
            with open("my_key.txt") as f:
                txt_mnemonic = f.readlines()
            private_key = mnemonic.to_private_key(txt_mnemonic[0])
            return 1, private_key
        except:
            return 0, 0
    else:
        private_key = mnemonic.to_private_key(key.mnemonic)
        return 1, private_key


@app.get("/account/new")
def create_account():
    """ Creates a wallet account address
    """
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    return {"address": address, "passphrase": passphrase}


@app.post("/account/data")
def get_account_info(key:SenderKey):
    good_key, private_key = get_key(key)
    if good_key:
        info = algod_client.account_info(account.address_from_private_key(private_key))
        return {"Address": info}
    else:
        return {"Response": "Not valid key"}


@app.post("/setup/drm/new")
def drm_deploy(key:SenderKey):
    """ Deploy Smart Contracts for DRM and get corresponding app ids
    """
    if check_deployed():
        try:
            good_key, private_key = get_key(key)
            if good_key:
                txn_data1, txn_data2 = setup_drm(algod_client,
                                        private_key,
                                        [  disaster_warnings.approval(), 
                                            disaster_warnings.clear(), 
                                            3, 3, 5, 5],
                                        [  disaster_consensus.approval(), 
                                        disaster_consensus.clear(), 
                                        3, 3, 5, 5],
                                        [  disaster_basic_template.approval(), 
                                        disaster_basic_template.clear(), 
                                        5, 4, 5, 5])
                new_drm_app_id(txn_data1['application-index'], txn_data2['application-index'])
                return txn_data1, txn_data2
            else:
                return {"Response": "Input key producing error"}
        except:
            return {"Response": "DRM app failed to deploy"}
    else:
        return {"Response": "DRM app is alread deployed"}


@app.post("/setup/drm/reset")
def drm_reset():
    """ Removes stored app ids for DRM therefore allowing new drm apps
    """
    new_drm_app_id(0, 0)
    return {"Response": "DRM apps reset"}


@app.post("/setup/drm/optin")
def optin_drm(key:SenderKey):
    """ Optin to DRM Apps to use
    """
    no_exist, app_id_warnings, app_id_consensus = get_app_ids()
    if no_exist:
        return {"Response": "DRM not deployed or not correctly deployed"}
    good_key, private_key = get_key(key)
    if good_key:
        try:
            txn_data1 = optin(algod_client, private_key, app_id_warnings)
        except AlgodHTTPError:
            txn_data1 = {"Response1": "Already opted into warnings app"}
        try:
            txn_data2 = optin(algod_client, private_key, app_id_consensus)
        except AlgodHTTPError:
            txn_data2 = {"Response2": "Already opted into consensus app"}
        return txn_data1, txn_data2
    else:
        return {"Response": "Key Error"}


@app.post("/warning/new")
def create_warning(key:SenderKey, warning:Warning):
    """ Creates a new warning asset on disaster warnings app
    """
    no_exist, app_id_warnings, app_id_consensus = get_app_ids()
    if no_exist:
        return {"Response": "DRM not deployed or not correctly deployed"}
    good_key, private_key = get_key(key)
    if good_key:
        txn_data = new_warning(algod_client, private_key, app_id_warnings, warning)
        return txn_data
    else:
        return {"Response": "Key Error"}


@app.post("/warning/timed_out")
def timed_out_warnings(key:SenderKey):
    no_exist, app_id_warnings, app_id_consensus = get_app_ids()
    if no_exist:
        return {"Response": "DRM not deployed or not correctly deployed"}
    good_key, private_key = get_key(key)
    if good_key:
        txn_data = timed_out(algod_client, private_key, app_id_warnings)
        return txn_data
    else:
        return {"Response": "Key Error"}


@app.get("/warning/view/active")
def view_active_warnings():
    no_exist, app_id_warnings, app_id_consensus = get_app_ids()
    if no_exist:
        return {"Response": "DRM not deployed or not correctly deployed"}
    asset_ids = read_all_assets(algod_client, get_application_address(app_id_warnings))
    warnings = []
    for asset_id in asset_ids:
        warnings.append(algod_client.asset_info(asset_id))
    if len(warnings) == 0:
        return {"Response": "No active warnings"}
    else:
        return warnings


@app.post("/disaster/new")
def warning_checker(key:SenderKey):
    """ This functon will become an API that does the following
    - Get all warnings
    - Find consensus of warnings
    - Define Disaster
    - Create IPFS data (Get url)
    - Create disaster token on contract
    """

    no_exist, app_id_warnings, app_id_consensus = get_app_ids()
    if no_exist:
        return {"Response": "DRM not deployed or not correctly deployed"}
    good_key, private_key = get_key(key)
    if good_key:
        valid_time = 50000000
        timestamp = round(datetime.timestamp(datetime.now()))

        address_disaster_warnings = get_application_address(app_id_warnings)
        address_disaster_consensus = get_application_address(app_id_consensus)
        # Get all warnings
        asset_id_warnings = read_all_assets(algod_client, address_disaster_warnings)
        warnings = []
        for id in asset_id_warnings:
            warnings.append(algod_client.asset_info(id))
        #print(warnings) # Test line
        useable_warnings = []
        for warning in warnings:
            #print(warning['params']['name'][12:17])  # Test line
            #print(warning['params']['name'][17:22])  # Test line
            try:
                warning_time = int(warning['params']['name'][0:10])
                warning_type = warning['params']['name'][10:12]
                warning_lat = int(warning['params']['name'][12:17])
                warning_lon = int(warning['params']['name'][17:22])
            except:
                continue
            time_cond_1 = warning_time >= timestamp - valid_time
            time_cond_2 = warning_time <= timestamp
            type_cond = warning_type in disaster_types
            lat_cond = warning_lat <= 18000
            lon_cond = warning_lon <= 36000
            if time_cond_1 and time_cond_2 and type_cond and lat_cond and lon_cond:
                # Add warning to useable list
                useable_warnings.append([warning_time, warning_type, warning_lat, warning_lat, warning])
            
        # Categorise warnings by disaster type
        categorised_warnings = []
        for disaster_type in disaster_types:
            current_type = []
            for warning in useable_warnings:
                if disaster_type == warning[1]:
                    current_type.append(warning)
            categorised_warnings.append(current_type)

        # Get consensus of warnings
        category_consensus = []
        category_confirmed = []
        category_avg = []
        for category in categorised_warnings:
            # PLACE BAYES MATHS REPLACEMENT HERE
            # Currently this is a basic algorithm that determines if number(TOTAL_IN_RANGE) of warnings are within average + number(RANGE) 
            if len(category) > 0:
                RANGE = 5
                TOTAL_IN_RANGE = 3

                lat_sum = 0
                lon_sum = 0
                for warning in category:   
                    lat_sum += warning[2]
                    lon_sum += warning[3]
                lat_avg = lat_sum / len(category)
                lon_avg = lon_sum / len(category)
                confirmed = []
                for warning in category:
                    lat_within = (lat_avg-RANGE <= warning[2]) and (warning[2] <= lat_avg+RANGE)
                    lon_within = (lon_avg-RANGE <= warning[3]) and (warning[3] <= lon_avg+RANGE)
                    if lat_within and lon_within:
                        confirmed.append(warning)
                if len(confirmed) >= TOTAL_IN_RANGE:
                    category_consensus.append(1)
                    category_confirmed.append(confirmed)
                else:
                    category_consensus.append(0)
                category_avg.append([timestamp, lat_avg, lon_avg])
            else:
                category_consensus.append(0)
                category_confirmed.append([])
                category_avg.append([timestamp, -1, -1])
            # END BAYES MATHS REPLACEMENT

        #print(category_consensus)
        #print(category_confirmed)
        #print(category_avg)
        
        # Define Disaster
        for i in range(len(category_consensus)):
            if category_consensus[i]:


                # SEND DATA TO IPFS
                url = "http://ipfs/filler-link.com"
                hash = "11111111111111111111111111111111"
                
                disaster_app_args = [   category_avg[i][0],
                                        disaster_types[i],
                                        round(category_avg[i][1]),
                                        round(category_avg[i][2]),
                                        url,
                                        hash]
                
                txn_data = new_disaster(algod_client, 
                                        private_key, 
                                        app_id_consensus, 
                                        disaster_app_args)
        return txn_data
    else:
        return {"Response": "Key Error"}













