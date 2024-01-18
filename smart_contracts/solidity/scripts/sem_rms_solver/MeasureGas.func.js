// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

// Function that deploy smart contract SocialActivation.sol
const hre = require("hardhat");

const path = require("path");
const { Signer, Wallet } = require("ethers");
const fs = require('fs');
const { receiveMessageOnPort } = require("worker_threads");

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

pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266";0

const min_dim = 3;
const max_dim = 50;   // Increase for full test
const num_items = 5;

// const contract_name = "DevCalculateAlpha";

async function deployContract(contract_title) {
    const Contract = await hre.ethers.getContractFactory(contract_title);
    tx_params = {
        gasLimit: 30000000
    };
    const dapp = await Contract.connect(await key_to_signer(accounts[0])).deploy(tx_params);
    const tx = await dapp.deployed();
    // console.log(await dapp.wait());
    return dapp.address;
}

async function main() {

    // // Gets smart contract ABI
    // const Contract = await hre.ethers.getContractFactory(contract_name);
    // // Deploys smart contract
    tx_params = {
        gasLimit: 30000000
    }

    // const dapp = await Contract.connect(await key_to_signer(accounts[0])).deploy(tx_params);
    // // Waits until smart contract is deployed and returns tx
    // const tx = await dapp.deployed();
    // // console.log(tx);
    // // Outputs transaction to console
    // var display = tx.deployTransaction;

    // display.data = "data...."
    // // console.log(display);
    // // console.log(dapp.address);

    // console.log("App Deployed - Starting Test");
    // console.log("-----------------------------------");

    const calc_alpha_name = "DevCalculateAlpha";
    const calc_alpha_address = await deployContract(calc_alpha_name);
    const calc_alpha_ABI = await ethers.getContractFactory(calc_alpha_name);
    const calc_alpha_dapp = calc_alpha_ABI.attach(calc_alpha_address);

    const val_alpha_name = "DevValidateAlphaBetaTest";
    const val_alpha_address = await deployContract(val_alpha_name);
    const val_alpha_ABI = await ethers.getContractFactory(val_alpha_name);
    const val_alpha_dapp = val_alpha_ABI.attach(val_alpha_address);

    console.log("Deployed all required apps - Starting Test");
    console.log("------------------------------------------");

    gas_calc_1 = [];
    gas_calc_2 = [];
    gas_calc_5 = [];
    gas_validate = [];

    try_1 = true;
    try_2 = true;
    try_5 = true;
    try_val = true;

    // const Token = await ethers.getContractFactory(contract_name);
    // const token = await Token.attach(dapp.address);

    // CalcAlpha 1,2,5
    // DevValidateAlphaBetaTest _validate_alpha

    var end = false;
    alpha = [];

    for (let h = min_dim; h <= max_dim; h++) {
        console.log("Starting", h + "x" + h)
        for (let j = 0; j < num_items; j++) {
            const sample = JSON.parse(fs.readFileSync('../../datasets/' + h + 'x' + h + '/' + j + '.json', { encoding: 'utf-8' }));
            const solution = JSON.parse(fs.readFileSync('../../datasets/' + h + 'x' + h + '/' + j + 'solve.json', { encoding: 'utf-8' }));

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
                alpha.push(String(solution[y] * multiplier));
            }

            // balance_before = await hre.ethers.provider.getBalance(pub);

            // Run method, compute alpha from S matrix
            task = 0
            if (try_1) {
                try {
                    var result = await calc_alpha_dapp.connect(await key_to_signer(accounts[0]))._compute_alpha_1(matrix, B, tx_params);
                    reciept = await result.wait();
                    gas_calc_1.push(parseInt(reciept.gasUsed));
                } catch {
                    task += 1
                    try_1 = false;
                }
            }
            if (try_2) {
                try {
                    var result = await calc_alpha_dapp.connect(await key_to_signer(accounts[0]))._compute_alpha_2(matrix, B, tx_params);
                    reciept = await result.wait();
                    gas_calc_2.push(parseInt(reciept.gasUsed));
                } catch {
                    task += 1
                    try_2 = false;
                }
            }
            if (try_5) {
                try {
                    var result = await calc_alpha_dapp.connect(await key_to_signer(accounts[0]))._compute_alpha_5(matrix, B, tx_params);
                    reciept = await result.wait();
                    gas_calc_5.push(parseInt(reciept.gasUsed));
                } catch {
                    task += 1
                    try_5 = false;
                }
            }
            if (try_val) {
                try {
                    var result = await val_alpha_dapp.connect(await key_to_signer(accounts[0]))._validate_alpha(matrix, alpha, tx_params);
                    reciept = await result.wait();
                    gas_validate.push(parseInt(reciept.gasUsed));
                } catch {
                    task += 1
                    try_val = false;
                }
            }
            if (task == 4) {
                end = true;
            }
        }
        if (end) {
            break;
        }
    }

    var data = {
        calc_1: gas_calc_1,
        calc_2: gas_calc_2,
        calc_5: gas_calc_5,
        validate: gas_validate
    }

    const dir_test_data = path.join(__dirname, "..", "..", "test-data");
    if (!fs.existsSync(dir_test_data)) {
        fs.mkdirSync(dir_test_data);
    }
    fs.writeFileSync(
        path.join(dir_test_data, "sem_rms_solver.gas_results.json"),
        JSON.stringify(data, undefined, 2)
    );

    console.log(gas_calc_1, gas_calc_2, gas_calc_5, gas_validate);

}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
