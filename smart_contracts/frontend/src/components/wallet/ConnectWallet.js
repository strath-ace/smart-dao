import React from "react";

// We'll use ethers to interact with the Ethereum network and our contract
//import { ethers } from "ethers";

import { ConnectWalletInterface } from "./ConnectWalletInterface";

import { UnavaibleWalletInterface } from "./UnavaibleWalletInterface";

import { Link } from "react-router-dom";


//import {networkError} from "./NetworkErrorMessage";



export function ConnectWallet({params}) {
    
    // console.log("Params", params)

    if (!params.user_address) {
      return (
      <ConnectWalletInterface 
          connectWallet={() => _connectWallet()} 
          //networkError={this.ntate.networkError}
          //dismiss={() => _dismissNetworkError()}
      />
      );
    }
    if (params.user_address && (!params.network_id || !params.dapp1_data)) {
        _set_network();
        // somehow reload page
    }
    if (params.dapp1_data) {
        //console.log(params.dapp1);
        _checkNetwork();
        return (
            <Link to="/wallet_info">
            <button id="always-btn" className="btn btn-warning" type="button">
                Wallet Details
            </button>
        </Link>
        );
    }
    else {
        return (
            <UnavaibleWalletInterface />
        );
    }
    

    //
    async function _connectWallet() {
        const [selectedAddress] = await window.ethereum.request({ method: 'eth_requestAccounts' });
        _checkNetwork();
        _initialize(selectedAddress);
        // We reinitialize it whenever the user changes their account.
        window.ethereum.on("accountsChanged", ([newAddress]) => {
            if (newAddress === undefined) {
            //return _resetState();
            }
            
            _initialize(newAddress);
            console.log(newAddress);
        });
    }
    
    //
    async function _initialize(currentUserAddress) {
        //console.log(await handler(currentUserAddress));
        await params.handler_address(currentUserAddress);
        //_initializeEthers();
        
    }
    

    //
    async function _set_network() {
        const response = await fetch('./data/dapp-data.json',{
            headers : { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        var out = await response.json();
        // this.setState({
        //     network_id: await out["network_chain_id"],
        // })
        await params.handler_network(await out["network_chain_id"]);
        await params.handler_dapp1_data(await out);
        await _checkNetwork();
    }
    

    async function _switchChain() {
        try {
            const chainIdHex = `0x${await params.network_id.toString(16)}`
            await window.ethereum.request({
                method: "wallet_switchEthereumChain",
                params: [{ chainId: chainIdHex }],
            });
        }
        catch (err) {
            console.log(err)
        }
    }

    // This method checks if the selected network is Localhost:8545
    function _checkNetwork() {
        try {
            if (window.ethereum.networkVersion !== params.network_id) {
                _switchChain();
            }
        }
        catch (err) {
            console.log(err);
        }
    }

}


