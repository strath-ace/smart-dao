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
import { NewNotification } from "./parts/NewNotification";
import { GetMyNotifications } from "./parts/GetMyNotifications";
import { RefreshNotifications } from "./parts/RefreshNotifications";
import {GetDisasters} from "./parts/GetDisasters";

import { TransactionErrorMessage } from "./parts/TransactionErrorMessage";
import { WaitingForTransactionMessage } from "./parts/WaitingForTransactionMessage";


import "./SocialActivationStyle.css"


// This is an error code that indicates that the user canceled a transaction
const ERROR_CODE_TX_REJECTED_BY_USER = 4001;

// NEEDS TO BE A CLASS AS DAPP MUST BE STORED IN this.state
export class SocialActivationApp extends React.Component {

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

      //this._set_vals();

      return (
        <div className="content-social-activation">
          <div>
              <div className="top-box">
                
                <div className="transaction-messages">
                  {this.state.txBeingSent && (
                    <WaitingForTransactionMessage txHash={this.state.txBeingSent} />
                  )}
                  
                  {this.state.transactionError && (
                    <TransactionErrorMessage
                      message={this._getRpcErrorMessage(this.state.transactionError)}
                      dismiss={() => this._dismissTransactionError()}
                    />
                  )}
                </div>

                <div className="add-data">
                  {(
                    <NewNotification 
                      new_notification={(_type, _regions) => this._s_new_notification(_type, _regions)}
                      confirm_consensus={(_type, _regions) => this._s_check_consensus(_type, _regions)}
                    />
                  )}
                </div>

                <div className="user-heading">
                  {/* <p><b>{(<GetAuthorisedStatus user_address={this.state.user_address} _func={(user_address) => this._get_authorised_status(user_address)} />)}</b> user:</p> */}
                  <h3><b>{this.state.status_authorised}</b> user:</h3>
                  <h5><b>{this.state.user_address}</b></h5>
                </div>
    
                <div className="refresh-button">
                {(
                    <RefreshNotifications 
                      userAddress={this.state.user_address} 
                      update_page={(user_address) => this._set_vals(this.state.user_address)} 
                    />
                  )}
                </div>
                
              </div>
  
              <div className="disasters-list">
                {(
                  <GetDisasters 
                    disasters={this.state.disasters_list}
                  />
                )}
                <h4>Confirmed Disasters List</h4>
                <table id="disasters-list">
                  <thead>
                      <tr>
                          <td><b>Disaster Type</b></td>
                          <td><b>Region</b></td>
                          <td><b>First Notification Timestamp</b></td>
                          <td><b>Consensus Timestamp</b></td>
                      </tr>
                  </thead>
                  <tbody id="disasters-table"></tbody>
                </table>
              </div>
  
              <div className="notifications-list">
                  {(
                    <GetMyNotifications
                      notifications={this.state.notifications_list}
                    />
                  )}
  
                  <h4>My Notifications List</h4>
                  <table id="notifications-list">
                    <thead>
                        <tr>
                            <td><b>Disaster Type</b></td>
                            <td><b>Region</b></td>
                            <td><b>Timestamp</b></td>
                        </tr>
                    </thead>
                    <tbody id="notifications-table"></tbody>
                  </table>          
              </div>
  
            </div>
          </div>   
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
      status_authorised: await this._get_authorised_status(this.state.user_address),
      notifications_list: await this._update_notifications(this.state.user_address),
      disasters_list: await this._update_disasters()
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
 

  async  _update_notifications(user_address) {
    console.log("Updating Notifications List");
    var notifications = await this._dapp._get_my_notification_list(user_address)
    return notifications.slice().reverse()
  }

  async _update_disasters() {
    console.log("Updating Disasters List");
    var counter = 0;
    var disasters_list_temp = [];
    try {
      counter = parseInt(await this._dapp._get_disaster_count());
    } 
    catch(err) {
      //console.log(err);
    }
    for (let i = 1; i < counter; i++) {
      disasters_list_temp.push(await this._dapp._get_disasters_list(i))
    }
    if (counter > 0) {
      return disasters_list_temp;
    } else {
      return undefined
    }
  }

  async _s_new_notification(_type, _regions) {
    console.log("Trigger");
    if (this.txBeingSent === undefined) {
      this.setState({txBeingSent: true})
      try{
        console.log(_regions.length);
        for (let i = 0; i < _regions.length; i++) {
          _regions[i] = parseInt(_regions[i], 10); // Explicitly include base as per Álvaro's comment
        }
        console.log("Trigger2");
        await this._dapp._new_notification(_regions, _type);
        console.log("Trigger3");
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
        this._set_vals();
      }
    }
    
  }

  async _s_check_consensus(_type, _regions) {
    console.log("Start Consensus Confirm");
    if (this.txBeingSent === undefined) {
      this.setState({txBeingSent: true})
      try{
        for (let i = 0; i < _regions.length; i++) {
          _regions[i] = parseInt(_regions[i], 10); // Explicitly include base as per Álvaro's comment
          await this._dapp._confirm_consensus(_regions[i], _type);
        }
        
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
        this._set_vals();
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
