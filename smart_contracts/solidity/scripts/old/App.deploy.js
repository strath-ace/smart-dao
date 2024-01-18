// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

// Function that deploy smart contract SocialActivation.sol

const hre = require("hardhat");
const path = require("path");
const { Signer, Wallet } = require("ethers");

// Converts private key to a signer
async function key_to_signer(priv) {
  const provider = hre.ethers.provider;
  const signer_wallet = new Wallet(priv);
  const signer = signer_wallet.connect(provider);
  return signer;
}

const accounts = config.networks.auto.accounts;

const contract_name = "ValidateAlpha";

async function main() {
  
  // Gets smart contract ABI
  const Contract = await hre.ethers.getContractFactory(contract_name);
  // Deploys smart contract
  tx_params = {
    gasLimit: 10000000
  }
  //console.log(accounts[0]);
  //console.log(await key_to_signer(accounts[0]));
  //input_key = Wallet.fromMnemonic("feed pigeon security vote audit danger sense beef hub name prepare settle").privateKey
  //.connect(await key_to_signer(wallet["mnemonic"]))
  console.log("hey");
  const dapp = await Contract.connect(await key_to_signer(accounts[0])).deploy(tx_params);
  // Waits until smart contract is deployed and returns tx
  const tx = await dapp.deployed();
  // Outputs transaction to console
  var display = tx.deployTransaction;
  display.data = "data...."
  console.log(display);
  // Saves deployed smart contract details to artifacts folders
  save_artifacts(dapp, tx.deployTransaction.chainId);
}

function jsonConcat(o1, o2) {
  for (var key in o2) {
   o1[key] = o2[key];
  }
  return o1;
}
 
// Save deployed smart contract details to artifacts folders
function save_artifacts(dapp, chainId) {
  const fs = require("fs");

  const dapp_artifact = artifacts.readArtifactSync(contract_name);

  var output_artifacts = {};
  output_artifacts = jsonConcat({ dapp_address: dapp.address }, dapp_artifact);
  output_artifacts = jsonConcat({ network_chain_id: chainId }, output_artifacts);
  //console.log(output_artifacts);

  // Create contract artifacts for general use
  const dir_general_artifacts = path.join(__dirname, "..", "dapp");
  if (!fs.existsSync(dir_general_artifacts)) {
    fs.mkdirSync(dir_general_artifacts);
  }
  fs.writeFileSync(
    path.join(dir_general_artifacts, "dapp-data.json"),
    JSON.stringify(output_artifacts, undefined, 2)
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
