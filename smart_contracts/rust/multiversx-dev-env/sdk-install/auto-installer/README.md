# Install mxpy Development Environment

## Dependencies

- [Python 3.8 or later](https://www.python.org/)

- For smart contract written in C ncurses compiler library can be installed using:
```
sudo apt install libncurses5
```

## Install

This installation guide is for Linux. For other OS use the tutorials set out on [MultiversX Docs](docs.multiversx.com).

##### Clone Repository
Navigate to /Home and clone repository. In terminal:
```
cd
git clone --recurse-submodules https://gitlab.com/parametry-ai/space-dao/erdpy-dev-env multiversx-sdk
```

##### Install erdpy
Run installer. In terminal:
```
cd ~/multiversx-sdk/sdk-install
python3 mxpy-up.py
```
Check path variable has been set correct. In file .profile at Home check the following exists (or add if doesnt):
```
export PATH="${HOME}/multiversx-sdk:$PATH"	# multiversx-sdk
```
Replace "user" with the user on the computer.
A computer restart is now required to update the Path.


## Further Steps

[Configure for Local Private Testnet](./testnet_instructions.md)


