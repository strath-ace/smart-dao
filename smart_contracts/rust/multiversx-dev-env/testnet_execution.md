# Run Testnet

## Installer

Make sure that all steps in the [installer README](./sdk-install/README.md) have been followed.

## Setup

2 terminal windows are required to run the testnet. They will be reffered to as terminals A and B.

## Terminal A

Terminal A will run the indexer docker-compose script. In terminal A:
```
cd ~/multiversx-sdk/mx-chain-es-indexer-go
sudo docker-compose up
```
Wait until the output stops. You will not be able to input anything else into this terminal

When shutting down this terminal A, press Ctrl+C and then enter the following:
```
sudo docker-compose down
```

## Terminal B

Terminal B will run the testnet itself. In terminal B:
```
cd ~/multiversx-sdk
mxpy testnet clean
mxpy testnet config
mxpy testnet start
```
Wait until the output text starts to become blue (Turquoise if your being particular). Sometimes the clean and config lines arent required. This is more complicated and is not explained here.

When shutting down this terminal B, press Ctrl+C.


## Running Transactions

## Running Smart Contracts

## Running Indexer Search