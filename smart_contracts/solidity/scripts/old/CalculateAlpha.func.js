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
const max_dim = 49;   // Increase for full test
const num_items = 1;

const contract_name = "DevCalculateAlpha";

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

  cost_li1 = [];
  cost_li2 = [];
  cost_li3 = [];
  cost_li4 = [];
  cost_li5 = [];

  try_1 = true;
  try_2 = true;
  try_3 = true;
  try_4 = true;
  try_5 = true;

  const Token = await ethers.getContractFactory(contract_name);
  const token = await Token.attach(dapp.address);

  var end = false;

  for (let h = min_dim; h <= max_dim; h++) {
    console.log("Starting", h+"x"+h)
    for (let j = 0; j < num_items; j++) {
      const sample = JSON.parse(fs.readFileSync('../../datasets/'+h+'x'+h+'/'+j+'.json', {encoding: 'utf-8'}));
      const solution = JSON.parse(fs.readFileSync('../../datasets/'+h+'x'+h+'/'+j+'solve.json', {encoding: 'utf-8'}));
      
      const in_matrix = sample;
      const DECIMALS = 18
      const multiplier = Math.pow(10, DECIMALS);
      k1 = in_matrix.length;
      k2 = in_matrix[0].length;
      var B = []
      var matrix = []
      for (let y = 0; y < k1; y++) {
          var temp = [];
          for (let x = 0; x < k2; x++) {
              temp.push(String(Math.round((in_matrix[y][x]) * multiplier)));
          }
          matrix.push(temp);
          B.push(String(multiplier));
          solution[y] = solution[y] * multiplier;
      }
      
      // balance_before = await hre.ethers.provider.getBalance(pub);

      // Run method, compute alpha from S matrix
      task = 0
      if (try_1) {
        try{
          var result = await token.connect(await key_to_signer(accounts[0]))._compute_alpha_1(matrix, B, tx_params);
          reciept = await result.wait();
          cost_li1.push(parseInt(reciept.gasUsed));
        } catch {
          task += 1
          try_1 = false;
        }
      }
      if (try_2) {
        try{
          var result = await token.connect(await key_to_signer(accounts[0]))._compute_alpha_2(matrix, B, tx_params);
          reciept = await result.wait();
          cost_li2.push(parseInt(reciept.gasUsed));
        } catch {
          task += 1
          try_2 = false;
        }
      }
      if (try_3) {
        try{
          var result = await token.connect(await key_to_signer(accounts[0]))._compute_alpha_3(matrix, B, tx_params);
          reciept = await result.wait();
          cost_li3.push(parseInt(reciept.gasUsed));
        } catch {
          task += 1
          try_3 = false;
        }
      }
      if (try_4) {
        try{
          var result = await token.connect(await key_to_signer(accounts[0]))._compute_alpha_4(matrix, B, tx_params);
          reciept = await result.wait();
          cost_li4.push(parseInt(reciept.gasUsed));
        } catch {
          task += 1
          try_4 = false;
        }
      }
      if (try_5) {
        try{
          var result = await token.connect(await key_to_signer(accounts[0]))._compute_alpha_5(matrix, B, tx_params);
          reciept = await result.wait();
          cost_li5.push(parseInt(reciept.gasUsed));
        } catch {
          task += 1
          try_5 = false;
        }
      }
      if (task == 5) {
        end = true;
      }     
    }
    if (end) {
      break;
    }
  }

  var data = {
    mat1: cost_li1,
    mat2: cost_li2,
    mat3: cost_li3,
    mat4: cost_li4,
    mat5: cost_li5
  }

  var jsonData = JSON.stringify(data);
  fs.writeFile("results.big_test_calc_alphas.txt", jsonData, function(err) {
    if (err) {
        console.log(err);
    }
  }); 

  console.log(cost_li1, cost_li2, cost_li3, cost_li4, cost_li5);
  
}


// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
