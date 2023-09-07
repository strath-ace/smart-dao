require("@nomicfoundation/hardhat-toolbox");
require("hardhat-gas-reporter");
creds = require( './credentials.json');

//const { config } = require("hardhat");
const { Wallet } = require("ethers");
const path = require("path");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {

  solidity: "0.8.20",

  // defaultNetwork: "auto",
  
  networks: {
    auto: {
      url: creds.url,
      accounts: [creds.private_key]
    },
    hardhat: {
    },
    localhost: {
      url: "http://127.0.0.1:8545",
      // accounts: [creds.private_key]
    }
  },

  gasReporter: {
    enabled: true,
    currency: 'USD',
    gasPrice: 30,
    blockLimit: 30000000,
    coinmarketcap: creds.coinmarketcap_api
  },


  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }

};
