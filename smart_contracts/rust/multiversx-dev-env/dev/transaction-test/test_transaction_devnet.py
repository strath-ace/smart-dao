from multiversx_sdk_core import Address, TokenPayment, Transaction, AccountNonceHolder
from multiversx_sdk_wallet import UserPEM
from pathlib import Path
from multiversx_sdk_wallet import UserSigner
from multiversx_sdk_network_providers import ApiNetworkProvider
from multiversx_sdk_network_providers import ProxyNetworkProvider

#provider = ApiNetworkProvider("https://devnet-gateway.multiversx.com");
provider = ProxyNetworkProvider("https://devnet-gateway.multiversx.com");

config = provider.get_network_config()
print("Chain ID", config.chain_id)
print("Min gas price:", config.min_gas_price)

# Need to add address
account_address = Address.from_bech32("")
account_on_network = provider.get_account(account_address)
print("Nonce", account_on_network.nonce)
print("Balance", account_on_network.balance)

def transaction():
    
    # Need to add key.pem file
    signer = UserSigner.from_pem_file(Path("./key.pem"))
    #signer = UserPEM.from_file(Path("./key.pem"))
    tx = Transaction(
        nonce=90,
        # Need to add address
        sender=Address.from_bech32(""),
        receiver=Address.from_bech32(""),
        value=TokenPayment.egld_from_amount("1.0"),
        gas_limit=50000,
        gas_price=1000000000,
        chain_id="D",
        version=1
    )

    #print(tx.to_dictionary())
    nonce_holder = AccountNonceHolder(account_on_network.nonce)

    tx.nonce = nonce_holder.get_nonce_then_increment()
    tx.signature = signer.sign(tx)
    #print("Signature", tx.signature.hex())
    return tx


tx = transaction()


hash = provider.send_transaction(tx)

print(hash)