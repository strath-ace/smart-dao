import React from "react";

// We'll use ethers to interact with the Ethereum network and our contract
//import { ethers } from "ethers";

import { ConnectWalletInterface } from "./ConnectWalletInterface";
import { Link, useNavigate } from "react-router-dom";

//import {networkError} from "./NetworkErrorMessage";



export class ConnectWallet extends React.Component {

    constructor(props) {
  
      super(props);
  
      this.initialState = {
        user_address: props.params.user_address,
        network_id: props.params.network_id,
        dapp_data: props.params.dapp1_data,
        handler_user_address: props.params.handler_address,
        handler_network_id: props.params.handler_network,
        handler_dapp_data: props.params.handler_dapp1_data
      };
  
      this.state = this.initialState;
    }
  
    
    render () {

        if (!this.state.user_address) {
            return (
            <ConnectWalletInterface 
                connectWallet={() => this._connectWallet()} 
                //networkError={this.ntate.networkError}
                //dismiss={() => _dismissNetworkError()}
            />
            );
        }
        console.log(this.state.network_id);
        if (this.state.user_address && (!this.state.network_id || !this.state.dapp_data)) {
            this._set_network();
            //this._checkNetwork();
            
            // somehow reload page
            //navigate(1);
        }
        if (this.state.dapp_data) {
            console.log("Try")
            //console.log(params.dapp1);
            return (
                <Link to="/wallet_info">
                    <button id="always-btn" className="btn btn-warning" type="button">
                        Wallet Details
                    </button>
                </Link>
            );
        }
    
    }

    //
    async _connectWallet() {
        const [selectedAddress] = await window.ethereum.request({ method: 'eth_requestAccounts' });
        // this._checkNetwork();
        this._initialize(selectedAddress);
        // We reinitialize it whenever the user changes their account.
        window.ethereum.on("accountsChanged", ([newAddress]) => {
            if (newAddress === undefined) {
            //return _resetState();
            }
            
            this._initialize(newAddress);
            console.log(newAddress);
        });
    }
    
    //
    async  _initialize(currentUserAddress) {
        //console.log(await handler(currentUserAddress));
        await this.state.handler_user_address(currentUserAddress);
        //_initializeEthers();
        
    }
    

    //
    async  _set_network() {
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
        await this.state.handler_network_id(await out["network_chain_id"]);
        await this.state.handler_dapp_data(await out);
        //this._checkNetwork();
    }
    

    async  _switchChain() {
        try {
            const chainIdHex = `0x${await this.state.network_id.toString(16)}`
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
    _checkNetwork() {
        try {
            if (window.ethereum.networkVersion !== this.state.network_id) {
                this._switchChain();
            }
        }
        catch (err) {
            console.log(err);
        }
    }

}


