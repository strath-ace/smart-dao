# Solidity Dev Environment using Hardhat

## Setup

1. [Install prerequisites](install_req.md)
2. Clone Repository
3. Duplicate `credentials.template.json` as `credentials.json` and fill in details.


## Connect Local Network to metamask (or other key wallet)

The network details of the local network for metamask are:

```
Network Name: Whatever
RPC URL: http://127.0.0.1:8545
Chain ID: 31337
Currency Symbol: Whatever
```

The default asymettric keys for hardhat local testnet are [here](default_keys.md)

## Running a Hardhat Node

### Starting a node

1. Navigate into solidity/

2. Install npm modules

```bash
npm install
```

3. Deploy hardhat node

```bash
npx hardhat node
```

### Common commands

```bash
npx hardhat run scripts/.....
npx hardhat test
REPORT_GAS=true npx hardhat test
```

### Extra info

The app address is stored in `./dapp/dapp-data.json` as well as the contract ABI.

#### Stopping a node

Ctrl+C to kill

Otherwise use

```bash
kill %1
```

#### Resetting a node

Wipe all previous data from network (Doesnt change private keys).  
When node is not running.

```bash
npx hardhat clean
```
