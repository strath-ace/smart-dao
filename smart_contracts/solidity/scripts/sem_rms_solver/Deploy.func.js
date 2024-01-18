// Function that deploy smart contract SocialActivation.sol
const hre = require("hardhat");

const path = require("path");
const { Signer, Wallet } = require("ethers");
const fs = require('fs');
const { receiveMessageOnPort } = require("worker_threads");
const prompt = require('prompt-sync')();

// Converts private key to a signer
async function key_to_signer(priv) {
    const provider = hre.ethers.provider;
    const signer_wallet = new Wallet(priv);
    const signer = signer_wallet.connect(provider);
    return signer;
}

const accounts = config.networks.auto.accounts;

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

function askYesNo(question) {
    let answer = prompt(question + " (y/n) ");
    if (answer.toLowerCase() === "y") {
        return true;
    } else if (answer.toLowerCase() === "n") {
        return false;
    } else {
        // If the user enters an invalid response, prompt again
        alert("Please enter 'y' or 'n'");
        return askYesNoQuestion(question);
    }
}

async function main() {

    const contract_name = "ValidateAlphaBetaTest";

    const save_file_name = contract_name+".dapp_data.json"

    const dir_dapps = path.join(__dirname, "..", "..", "dapps");
    const file_dapp_data = path.join(dir_dapps, save_file_name)
    if (!fs.existsSync(dir_dapps)) {
        fs.mkdirSync(dir_dapps);
    }
    
    if (fs.existsSync(file_dapp_data)) {
        if (askYesNo("Dapp address for this contract already exists, do you want to overwrite this?")) {
            console.log("Deploying Contract");
            const dapp_address = await deployContract(contract_name);
            var data = {
                deployed_address: dapp_address
            }
            console.log("Contract Deployed");
            console.log("Saving Dapp Address");
            fs.writeFileSync(
                file_dapp_data,
                JSON.stringify(data, undefined, 2)
            );
        } else {
            console.log("Quitting Contract Deploy");
        }
    } else {
        console.log("Deploying Contract");
        const dapp_address = await deployContract(contract_name);
        var data = {
            deployed_address: dapp_address
        }
        console.log("Contract Deployed");
        console.log("Saving Dapp Address");
        fs.writeFileSync(
            file_dapp_data,
            JSON.stringify(data, undefined, 2)
        );
    }
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
