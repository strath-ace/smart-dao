# SpaceDAO Contract Drm

## About

This repository holds the smart contracts and other code for building and interacting with the smart contracts for Disaster Response Management deployed onto the MultiversX Network (Formerly Elrond Network).

The smart-contracts are built in Rust.

## Prerequisites

- Install and Setup [Erdpy Development Environment](https://gitlab.com/parametry-ai/space-dao/erdpy-dev-env)
- Clone this repository into /apps if not already there.

## Building

```
cd ~/erlondsdk/apps/contract-drm/contracts
erdpy contract build
```

## Testing

Test the newly built contract against the scenario tests.
```
cd ~/erlondsdk/apps/contract-drm/contracts
erdpy contract test
```

## Interaction

#### On devnet

Deploy & interact with contract:

```
python3 ./interaction/playground.py --pem=./testnet/wallets/users/alice.pem --proxy=http://localhost:7950
```

Interact with existing contract:

```
python3 ./interaction/playground.py --pem=./testnet/wallets/users/alice.pem --proxy=http://localhost:7950 --contract=erd1...
```

#### On testnet

Deploy & interact with contract:

```
python3 ./interaction/playground.py --pem=my.pem --proxy=https://testnet-gateway.elrond.com
```

Interact with existing contract:

```
python3 ./interaction/playground.py --pem=my.pem --proxy=https://testnet-gateway.elrond.com --contract=erd1...
```
