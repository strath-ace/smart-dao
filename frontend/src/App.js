import React, { useState } from "react";
import "./index.css";

import { Home } from "./routes/Home";
import { InformationConsensus } from "./routes/information_consensus";
import { AutomaticTasking } from "./routes/automatic_tasking";
import { SocialActivation } from "./routes/social_activation";
import { WalletInfo } from "./routes/wallet_info";
import { Route, Routes } from "react-router-dom";

export function App() {

  let [user_address, setAddressState] = useState(undefined);
  function handler_address(input_user) {
    setAddressState(input_user);
  }
  let [network_id, setNetworkId] = useState(undefined);
  function handler_network(input_id) {
    setNetworkId(input_id);
  }
  let [dapp1_data, setDapp1Data] = useState(undefined);
  function handler_dapp1_data(input_dapp) {
    setDapp1Data(input_dapp);
  }
  
  var params = {
    user_address: user_address,
    handler_address: handler_address,
    network_id: network_id,
    handler_network: handler_network,
    dapp1_data: dapp1_data,
    handler_dapp1_data: handler_dapp1_data
  }

  return (
    <>
      <Routes>
        <Route path="/" element={
          <Home 
            params={params}
          />
        } />
        <Route path="social_activation" element={
          <SocialActivation 
            params={params}
          />
        } />
        <Route path="automatic_tasking" element={
          <AutomaticTasking 
            params={params}
          />
        } />
        <Route path="information_consensus" element={
          <InformationConsensus 
            params={params}
          />
        } />
        <Route path="wallet_info" element={
          <WalletInfo 
            params={params}
          />
        } />
      </Routes>
    </>
  );
}
