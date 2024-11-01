// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import React from "react";

import { NetworkErrorMessage } from "./NetworkErrorMessage";

export function ConnectWalletInterface({ connectWallet }) {
  return (
    <div>
      <div>
            {/* Wallet network should be set to Localhost:8545.
            {networkError && (
              <NetworkErrorMessage 
                message={networkError} 
                dismiss={dismiss} 
              />
            )} */}
            <button
              id="always-btn"
              className="btn btn-warning"
              type="button"
              onClick={connectWallet}
            >
              Connect Wallet
            </button>
        </div>
    </div>
  );
}
