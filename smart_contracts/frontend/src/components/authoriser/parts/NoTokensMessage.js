// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import React from "react";

export function NoTokensMessage({ selectedAddress }) {
  return (
    <>
      <p>You don't have tokens to transfer</p>
      <p>
        To get some tokens, open a terminal in the root of the repository and run: 
        <br />
        <br />
        <code>npx hardhat --network localhost faucet {selectedAddress}</code>
      </p>
    </>
  );
}
