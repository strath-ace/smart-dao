import React from "react";

// We'll use ethers to interact with the Ethereum network and our contract
import { ethers } from "ethers";

// We import the contract's artifacts and address here, as we are going to be
// using them with ethers
//import dappData from "../dapp-artifacts/dapp-data.json";

// All the logic of this dapp is contained in the Dapp component.
// These other components are just presentational ones: they don't have any
// logic. They just render HTML.
import { NoWalletDetected } from "./parts/NoWalletDetected";
import { WalletNotConnected } from "./parts/WalletNotConnected";
//import { Loading } from "./Loading";
import { AuthoriseInterface } from "./parts/AuthoriseInterface";
// import { GetMyNotifications } from "./parts/GetMyNotifications";
// import { RefreshNotifications } from "./parts/RefreshNotifications";
// import {GetDisasters} from "./parts/GetDisasters";

// import { TransactionErrorMessage } from "./parts/TransactionErrorMessage";
// import { WaitingForTransactionMessage } from "./parts/WaitingForTransactionMessage";

import "./AuthoriserStyle.css"


// This is an error code that indicates that the user canceled a transaction
const ERROR_CODE_TX_REJECTED_BY_USER = 4001;

// NEEDS TO BE A CLASS AS DAPP MUST BE STORED IN this.state
export class Authoriser extends React.Component {

  constructor(props) {

    super(props);

    this.initialState = {
      user_address: props.params.user_address,
      network_id: props.params.network_id,
      dapp_data: props.params.dapp1_data,
      configured: false,
      status_authorised: undefined,
      disasters_list: undefined,
      notifications_list: undefined
    };

    this.state = this.initialState;
  }

  //const user_address = params.user_address;

  

  render () {
    // If no wallet
    if (window.ethereum === undefined) {
      return (
        <NoWalletDetected />
      );
    }
    // If wallet not connected
    if (!this.state.user_address) {
      return (
        <WalletNotConnected />
      );
    }
    else if (!this.state.network_id) {
      return (<p>No Network ID</p>)
    }
    else if (!this.state.dapp_data) {
      return (<p>No dApp Connected (No dapp data file)</p>)
    }
    else if (this.state.user_address && this.state.network_id && this.state.dapp_data && !this.state.configured) {
      this._build_dapp();
    }
    if (this.state.configured && !this.state.status_authorised) {
      this._set_vals();
    }
    if (this.state.configured) {
      return (
         <>
            <div className="content-authoriser">
                <AuthoriseInterface 
                    func_authorise={(_address) => this._s_authorise(_address)}
                />
            </div>
         </> 
      );
    }
  }

  // Builds the dapp from dapp_data
  async _build_dapp() {
    this._provider = new ethers.providers.Web3Provider(window.ethereum);

    this._dapp = new ethers.Contract(
      this.state.dapp_data.dapp_address,
      this.state.dapp_data.abi,
      this._provider.getSigner(0)
    );
    this.setState({
      configured: true
    })
  }

  // Sets values for updating variables
  async _set_vals() {
    console.log("Setting Vals")
    this.setState({
      status_authorised: await this._get_authorised_status(this.state.user_address)
    });
  }


  // Finds if user is authorised to use the service or not based on smart contract
  async _get_authorised_status(user_address) {
    console.log("Updating Authorised Status")
    try {
      if (await this._dapp.get_authorised(user_address)) {
        return "Authorised";
      } else {
        return "Not Authorised";
      }
    }
    catch(err) {
      return "Not Authorised";
    }
  }

  async _s_authorise(_address) {
    console.log("Start Authorisation Process");
    if (this.txBeingSent === undefined) {
      this.setState({txBeingSent: true})
      try{
          await this._dapp._authorise_user(_address);
        //.then(() => {
        //   //this._get_notification();
        //   console.log("the");
        // });
      } catch (error) {
        // We check the error code to see if this error was produced because the
        // user rejected a tx. If that's the case, we do nothing.
        if (error.code === ERROR_CODE_TX_REJECTED_BY_USER) {
          return;
        }
        // Other errors are logged and stored in the Dapp's state. This is used to
        // show them to the user, and for debugging.
        console.error(error);
        //console.log(error["reason"])
        this.setState({ transactionError: error });
      } finally {
        // If we leave the try/catch, we aren't sending a tx anymore, so we clear
        // this part of the state.
        this.setState({ txBeingSent: undefined });
      }
    }
  }

  
  // This method just clears part of the state.
  _dismissTransactionError() {
    this.setState({ transactionError: undefined });
  }

  // This method just clears part of the state.
  _dismissNetworkError() {
    this.setState({ networkError: undefined });
  }

  // This is an utility method that turns an RPC error into a human readable
  // message.
  _getRpcErrorMessage(error) {
    if (error.data) {
      return error;
      //return error.data.message;
    }
    return error
    //return error.message;
  }

  // This method resets the state
  _resetState() {
    this.setState(this.initialState);
  }

  // This method asks the user to switch chain on metamask
  async _switchChain() {
    try {
      const chainIdHex = `0x${this.state.network_id.toString(16)}`
      await window.ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: chainIdHex }],
      });
      await this._initialize(this.state.selectedAddress, "ERORENADF");
    }
    catch (err) {
      console.log("Waiting to set chain id");
    }
  }

  // This method checks if the selected network is correct
  _checkNetwork() {
    try {
      if (window.ethereum.networkVersion !== this.state.network_id) {
        this._switchChain();
      }
    }
    catch (err) {
      console.log("Waiting to set chain id");
    }
  }

}
