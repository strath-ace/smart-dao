// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import React from "react";

export function NoWalletDetected() {
  return (
    <div>
      <div>
        <div >
          <p>
            No Ethereum wallet was detected. <br />
            Please install{" "}
            <a
              href="https://www.coinbase.com/wallet"
              target="_blank"
              rel="noopener noreferrer"
            >
              Coinbase Wallet
            </a>
            or{" "}
            <a href="http://metamask.io" target="_blank" rel="noopener noreferrer">
              MetaMask
            </a>
            .
          </p>
        </div>
      </div>
    </div>
  );
}
