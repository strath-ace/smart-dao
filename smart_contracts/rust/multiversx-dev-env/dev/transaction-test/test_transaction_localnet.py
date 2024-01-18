from multiversx_sdk_core import Address, TokenPayment, Transaction, AccountNonceHolder
from multiversx_sdk_wallet import UserSigner
from multiversx_sdk_network_providers import ApiNetworkProvider, ProxyNetworkProvider
from pathlib import Path
from time import sleep
import json
import os

# ALICE Wallet is used in testnet setup and creation therefore can be avoided if a non-important account wants to be used.
# Although ALICE wallet can be used here, it was decided for ease and simplification that BOB and CAROL are used.

who_send = "bob"
who_recieve = "carol"


user = str(os.environ.get('USERNAME'))

pub_send = json.load(Path("/home/"+user+"/multiversx-sdk/testwallets/latest/users/"+who_send+".json").open())["bech32"]
pem_send = Path("~/multiversx-sdk/testwallets/latest/users/"+who_send+".pem")
pub_recieve = json.load(Path("/home/"+user+"/multiversx-sdk/testwallets/latest/users/"+who_recieve+".json").open())["bech32"]
# pem_recieve = Path("~/multiversx-sdk/testwallets/latest/users/"+who_recieve+".pem")   # Not required for current program setup


def exec_txn(proxy, signer, tx):
    try:
        
        tx.signature = signer.sign(tx)
        hash = proxy.send_transaction(tx)
        sent = False
        c = 0
        while sent == False and c <= 100:
            c += 1
            sleep(0.1)
            try:
                sent = proxy.get_transaction(hash).is_completed
            except:
                continue
        if sent == True:
            return sent, hash
        else:
            return sent, {"output": "too long"}
    except:
        return False, {"output": "bad proxy, tx or signer"}

def get_nonce(proxy, sender_address, tx):
    account_on_network = proxy.get_account(sender_address)
    nonce_holder = AccountNonceHolder(account_on_network.nonce)
    tx.nonce = nonce_holder.get_nonce_then_increment()
    return tx

def transaction(proxy, sender_address, reciever_address, amount):
    tx = Transaction(
        sender=sender_address,
        receiver=reciever_address,
        value=TokenPayment.egld_from_amount(amount),
        gas_limit=50000,
        gas_price=1000000000,
        chain_id=proxy.get_network_config().chain_id,
        version=1
    )
    return tx


proxy = ProxyNetworkProvider("http://localhost:7950")
signer = UserSigner.from_pem_file(pem_send)
sender_address = Address.from_bech32(pub_send)
reciever_address = Address.from_bech32(pub_recieve)

for i in range(10):
    tx = transaction(proxy, sender_address, reciever_address, "0.1")
    tx = get_nonce(proxy, sender_address, tx)
    sent, hash = exec_txn(proxy, signer, tx)
    print(sent)
    print(hash)

    