from pydantic import BaseModel
from typing import Union


class SenderKey(BaseModel):
    mnemonic: str

class Warning(BaseModel):
    data_provider_code: str = "0000"
    event_type: str = "VO"
    lat: int = 12345
    lon: int = 12345
    url: str = "example.com"
    url_hash: str = "11111111111111111111111111111111"






# Old API stuff

class Transaction(BaseModel):
    sender_address: str
    receiver_address: str
    passphrase: str
    amount: int
    note: str

class ApplicationSendData(BaseModel):
    sender: str
    passphrase: str
    app_id: int
    method_call: str
    timestamp: str
    data: str

class SearchTransaction(BaseModel):
    txn_parameters: list = [-1, '', '', '', '', '', -1, -1, -1, -1, '', '', -1, -1, '', '', False, -1, False, -1]
    search_parameters: list
    search_value: str
    search_value_convert_b64: bool = False
    
class SearchVariable(BaseModel):
    app_id: int
    is_global: bool
    local_address: str
    variable_name: str
    variable_value: str
    variable_change: str

class SearchWeb(BaseModel):
    url: str
    search_parameters: list


