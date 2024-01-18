#!/bin/bash

HOMEPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

HOMEPATH=(cd .. && $HOMEPATH)

echo $HOMEPATH

echo "--------"
echo "Clean previous testnet occurances"
cd $HOMEPATH
mxpy testnet clean
echo "Occurances Cleaned"
echo "--------"

echo "--------"
echo "Configuring Testnet Ports"
cd $HOMEPATH
mxpy config set chainID local-testnet
mxpy config set proxy http://localhost:7950
echo "Ports Configured"
echo "--------"

#echo "--------"
#echo "Fixing python library"
#cp $HOMEPATH/sdk-install/replacements/config.py $HOMEPATH/mxpy-venv/lib/python3.10/site-packages/multiversx_sdk_cli
#echo "Python fixed"
#echo "--------"

echo "--------"
echo "Clean previous testnet occurances"
cd $HOMEPATH
mxpy testnet clean
echo "Occurances Cleaned"
echo "--------"

echo "--------"
echo "Configure Testnet Files"
cd $HOMEPATH
mxpy testnet config
echo "Files configured"
echo "--------"

echo "--------"
echo "Add Observer Node"
cp $HOMEPATH/sdk-install/replacements/testnet.toml $HOMEPATH
echo "Observer Node Added"
echo "--------"


echo "--------"
echo "Temporarily Start Testnet"
cd $HOMEPATH
mxpy testnet start
echo "Testnet started"
echo "--------"


echo "--------"
echo "Opening Node Port"
cp $HOMEPATH/sdk-install/replacements/external.toml $HOMEPATH/testnet/observer00/config
echo "Node Port Opened"
echo "--------"
