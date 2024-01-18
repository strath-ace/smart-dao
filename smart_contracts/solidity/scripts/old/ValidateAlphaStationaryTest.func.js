// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

// Function that deploy smart contract SocialActivation.sol
const hre = require("hardhat");

const path = require("path");
const { Signer, Wallet } = require("ethers");
const fs = require('fs');

// Converts private key to a signer
async function key_to_signer(priv) {
  const provider = hre.ethers.provider;
  const signer_wallet = new Wallet(priv);
  const signer = signer_wallet.connect(provider);
  return signer;
}

// Converts private key to a signer
async function priv_to_pub(priv) {
  const provider = hre.ethers.provider;
  const signer_wallet = new Wallet(priv);
  const pub = signer_wallet.privateKey(provider);
  return pub;
}

const accounts = config.networks.auto.accounts;

pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266";

const min_dim = 3;
const max_dim = 10;   // Increase for full test
const num_items = 5;

const contract_name = "DevValidateAlphaStationayTest";

async function main() {
  
  // Gets smart contract ABI
  const Contract = await hre.ethers.getContractFactory(contract_name);
  // Deploys smart contract
  tx_params = {
    gasLimit: 30000000
  }

  const dapp = await Contract.connect(await key_to_signer(accounts[0])).deploy(tx_params);
  // Waits until smart contract is deployed and returns tx
  const tx = await dapp.deployed();
  // console.log(tx);
  // Outputs transaction to console
  var display = tx.deployTransaction;

  display.data = "data...."
  // console.log(display);
  // console.log(dapp.address);
  
  console.log("App Deployed - Starting Test");
  console.log("-----------------------------------");

  cost_li = [];

  const Token = await ethers.getContractFactory(contract_name);
  const token = await Token.attach(dapp.address);

  var end = false;

  for (let h = min_dim; h <= max_dim; h++) {
    console.log("Starting", h+"x"+h)
    for (let j = 0; j < num_items; j++) {
      const sample = JSON.parse(fs.readFileSync('../../datasets/'+h+'x'+h+'/'+j+'.json', {encoding: 'utf-8'}));
      const solution = JSON.parse(fs.readFileSync('../../datasets/'+h+'x'+h+'/'+j+'solve.json', {encoding: 'utf-8'}));
      
      // Multiply S matrix values to remove decimals
      const in_matrix = sample;
      const DECIMALS = 18
      const multiplier = Math.pow(10, DECIMALS);
      k1 = in_matrix.length;
      k2 = in_matrix[0].length;
      var matrix = []
      var alpha = []
      for (let y = 0; y < k1; y++) {
          var temp = [];
          for (let x = 0; x < k2; x++) {
              temp.push(String(Math.round((in_matrix[y][x]) * multiplier)));
          }
          matrix.push(temp);
          alpha.push(String(solution[y]*multiplier));
      }
      
      // balance_before = await hre.ethers.provider.getBalance(pub);

      // Run method, compute alpha from S matrix
      try{
        const result = await token.connect(await key_to_signer(accounts[0]))._validate_alpha(matrix, alpha, tx_params);
        reciept = await result.wait();
        cost_li.push(parseInt(reciept.gasUsed));
      } catch {
        console.log("Broke on:", h+"x"+h,)
        end = true;
        break;
      }     
    }
    if (end) {
      break;
    }
  }

  var data = {
    all_data: cost_li
  }

  var jsonData = JSON.stringify(data);
  fs.writeFile("results.validate_alpha_stationary.txt", jsonData, function(err) {
    if (err) {
        console.log(err);
    }
  }); 

  console.log(cost_li);
  
}













// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
