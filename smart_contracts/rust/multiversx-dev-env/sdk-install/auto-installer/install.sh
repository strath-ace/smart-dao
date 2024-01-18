#!/bin/bash

HOMEPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

HOMEPATH=../$HOMEPATH

echo $HOMEPATH

python3 $HOMEPATH/sdk-install/mxpy-up.py

echo "If this is the first time installing this library please restart your PC. Then proceed to run install2.sh"

echo "--------"
echo "Installing indexer"
cd $HOMEPATH
git clone https://github.com/multiversx/mx-chain-es-indexer-go
echo "Indexer installed"
echo "--------"

echo "--------"
echo "Installing testnet dependencies"
cd $HOMEPATH
mxpy testnet prerequisites
echo "Dependencies installed"
echo "--------"

echo "--------"
echo "Clean previous testnet occurances"
cd $HOMEPATH
mxpy testnet clean
echo "Occurances Cleaned"
echo "--------"
