// Function that deploy smart contract SocialActivation.sol
const hre = require("hardhat");

const path = require("path");
const { Signer, Wallet } = require("ethers");
const fs = require('fs');
const { receiveMessageOnPort } = require("worker_threads");
const prompt = require('prompt-sync')();

const accounts = config.networks.auto.accounts;

// Converts private key to a signer
async function key_to_signer(priv) {
    const provider = hre.ethers.provider;
    const signer_wallet = new Wallet(priv);
    const signer = signer_wallet.connect(provider);
    return signer;
}

let h = 7;
let j = 0;
const sample = JSON.parse(fs.readFileSync('../../datasets/' + h + 'x' + h + '/' + j + '.json', { encoding: 'utf-8' }));
const solution = JSON.parse(fs.readFileSync('../../datasets/' + h + 'x' + h + '/' + j + 'solve.json', { encoding: 'utf-8' }));

async function dapp_from_address(name, address) {
    const abi = await ethers.getContractFactory(name);
    const dapp = await abi.attach(address);
    return dapp
}

async function main() {

    var matrix = [];
    var alpha = [];
    const multiplier = Math.pow(10, 18);
    k1 = sample.length;
    k2 = sample[0].length;
    var matrix = []
    for (let y = 0; y < k1; y++) {
        var temp = [];
        for (let x = 0; x < k2; x++) {
            temp.push(String(Math.round((sample[y][x]) * multiplier)));
        }
        matrix.push(temp);
        alpha.push(String(Math.round(solution[y] * multiplier)));
    }

    tx_params = {
        gasLimit: 30000000
    }

    const contract_name = "ValidateAlphaBetaTest";

    const save_file_name = contract_name+".dapp_data.json"

    const dir_dapps = path.join(__dirname, "..", "..", "dapps");
    const file_dapp_data = path.join(dir_dapps, save_file_name)
    console.log(file_dapp_data);
    if (!fs.existsSync(file_dapp_data)) {
        console.log("No dapp exists (Have you deployed the contract?)");
    } else {
        const dapp_data = JSON.parse(fs.readFileSync(file_dapp_data, { encoding: 'utf-8' }));
        const dapp = await dapp_from_address(contract_name, dapp_data.deployed_address)
        console.log(matrix);
        console.log(alpha);
        var result = await dapp.connect(await key_to_signer(accounts[0]))._validate_alpha(matrix, alpha, tx_params);
        console.log(result);
    }

}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
