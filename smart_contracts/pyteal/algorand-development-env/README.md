# Algorand Development Environment

## About

This repository is to setup an easy to use, private test environment for Algorand pyteal based apps. It uses the Algorand sandbox for the blockchain network.

## Installing

#### Dependencies:
- [Docker](https://www.docker.com/products/docker-desktop) - Container for the sandbox
- [Python](https://www.python.org/) - For Python ;)
- [Pipenv](https://pipenv.pypa.io/en/latest/) - Python virtual environment creator
- [Git](https://github.com/) - To clone this repository

#### To install this Development Environment:
1. Clone this repository and its dependents:
```
cd install_location
git clone https://gitlab.com/parametry-ai/space-dao/space-dao-contracts
```

## Using the development Environment

#### Activating Development Environment:
1. Make sure that Docker is open and running
2. Place any other apps you wish to test in the /apps
3. Open Bash Terminal and run activate.sh
4. A browser window should open with the spacedao-app-drm running

#### Shutdown Development Environment for later use:
1. Ctrl+C or Close Bash Terminal to stop FastAPI
2. In a bash terminal, run deactivate.sh to close Algorand Sandbox
3. You may now close Docker (This avoids docker errors)

## Notes to Authors

Please be careful making updates to the main branch as this is meant to be a default template for any apps to use. Currently it auto-deploys spacedao-app-drm as this is setup for running.

## Links and tutorials
- How to use [Algorand Sandbox](https://github.com/algorand/sandbox)
- A course on [Pyteal Development](https://www.youtube.com/playlist?list=PLpAdAjL5F75CNnmGbz9Dm_k-z5I6Sv9_x)
- [Official Algorand Smart Contract Guidelines](https://developer.algorand.org/docs/get-details/dapps/avm/teal/guidelines/)
- [Pyteal Documentation](https://pyteal.readthedocs.io/en/latest/index.html)
- A few [example Pyteal Smart Contracts](https://github.com/algorand/smart-contracts)
