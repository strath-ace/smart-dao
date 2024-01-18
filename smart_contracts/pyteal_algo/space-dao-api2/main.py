from typing import Union
from typing import Optional
from fastapi import  FastAPI


from algosdk import account, encoding, mnemonic
from algosdk.future.transaction import PaymentTxn
from algosdk.future.transaction import AssetConfigTxn
from algosdk.error import WrongChecksumError, WrongMnemonicLengthError
from algosdk.v2client import algod, indexer

from schemes import *

# Run script with:
# uvicorn main:app --reload

# Initialise algod client
algod_client = algod.AlgodClient("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "http://localhost:4001")

# Initialise Validator
indexer_client = indexer.IndexerClient("","http://localhost:8980")

# Create application instance
app = FastAPI()

@app.get("/account")
def create_account():
    """ Creates a wallet account address
    """
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    return {"address": address, "passphrase": passphrase}

@app.get("/account/{Address}")
def get_account_info(Address:str):
    info = algod_client.account_info(Address)
    return {"Address": info}













"""
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "Robert Cowlishaw"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
"""