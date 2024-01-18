# Install mxpy Development Environment

This installation guide is for Linux. For other OS use the tutorials set out on [MultiversX Docs](docs.multiversx.com).

## Dependencies

- [Python 3.8 or later](https://www.python.org/)

- For smart contract written in C ncurses compiler library can be installed using:
```
sudo apt install libncurses5
```

## Install
1. **Clone Repository**
Navigate to /Home and clone repository. In terminal:
```
cd
git clone --recurse-submodules https://gitlab.com/parametry-ai/space-dao/multiversx-dev-env multiversx-sdk
```

## Install mxpy
2. ****Run installer**
```
cd ~/multiversx-sdk/sdk-install
python3 mxpy-up.py
```
3. **Check path variable has been set correct**
In file ~/.profile at Home check the following exists (or add if doesnt):
```
export PATH="${HOME}/multiversx-sdk:$PATH"	# multiversx-sdk
```

Then load the profile if it is not sourced when opening a new terminal (no
reboot necessary):
```
source ~/.profile
```

At this stage mxpy can be used for building smart contracts and deploying them on the public mainnet/devnet/testnet. Continue for steps on how to install the testnet and indexer.

## Install Testnet and Indexer

4. **Install dependencies**
```
mxpy testnet prerequisites
```

5. **Clean previous testnet occurances**
```
mxpy testnet clean
```

6. **Configure chainID and Proxy**
```
mxpy config set chainID local-testnet
mxpy config set proxy http://localhost:7950
```


7. **Quick code changes**
If this step is run without errors **you can skip steps 8, 9 and 10**. However if there are errors you may have to manually make the changes covered in steps 8, 9 and 10.

Add observer node to testnet (Do include the dot on the end of line 2):
```
cd ~/multiversx-sdk
cp sdk-install/replacements/testnet.toml .
```
Replace python library file (Same as step 9):
```
cd ~/multiversx-sdk
cp sdk-install/replacements/config.py  ~/multiversx-sdk/mxpy-venv/lib/python3.10/site-packages/multiversx_sdk_cli/testnet/
```
Open observer node port for indexer:
```
cd ~/multiversx-sdk
cp sdk-install/replacements/external.toml ~/multiversx-sdk/mx_chain_go/v1.3.50/mx-chain-go-1.3.50/cmd/node/config/
```
If all of this step executed succefully you have completed the install.

8. **Add observer node for indexer**
Add observer node generation by changing the testnet.toml file. In the replacements directory a copy of the changed file exists. This change can also be done manually.
Navigate to:
```
~/multiversx-sdk/testnet.toml
```
Navigate to line 13. The old line should look like this:
```
observers = 0
```
Update this line to have 1 observer:
```
observers = 1
```

9. **Change python library code**
To fix a later error a change has to be made to the python library. In the replacements directory a copy of the changed file exists. This change can also be done manually. Navigate to:
```
~/multiversx-sdk/mxpy-venv/lib/python3.10/site-packages/multiversx_sdk_cli/testnet/config.py
```
Navigate to line 248. The old code looks like this:
```python
def _get_shard_of_observer(self, observer_index: int):
    shard = int(observer_index // self.num_observers_per_shard())
    return shard if shard < self.num_shards() else self.metashard['metashardID']
```
Update this function too:
```python
def _get_shard_of_observer(self, observer_index: int):
    shard = int(0)
    return shard if shard < self.num_shards() else self.metashard['metashardID']
```
This is a temporary fix and may cause issues down the line (This could also pose an unknown security risk).



10. **Open new observer nodes port for indexer connection**
Open the observer nodes indexer port by changing the external.toml file. In the replacements directory a copy of the changed file exists. This change can also be done manually.
Navigate to:
```
~/multiversx-sdk/mx_chain_go/v1.3.50/mx-chain-go-1.3.50/cmd/node/config/external.toml
```
Navigate to line 7 through 13. The old lines should look like this:
```
Enabled           = false
IndexerCacheSize  = 0
BulkRequestMaxSizeInBytes = 4194304 # 4MB
URL               = "http://localhost:9200"
UseKibana         = false
Username          = ""
Password          = ""
```
Update this line to have enabled true and make sure the URL is the same as the indexer is looking for (by default this is http://localhost:9200). A username and password can also be added but by default these are empty.
```
Enabled           = true
IndexerCacheSize  = 0
BulkRequestMaxSizeInBytes = 4194304 # 4MB
URL               = "http://localhost:9200"
UseKibana         = false
Username          = ""
Password          = ""
```

## Install Completed

You can now run the [testnet launch code instructions](../testnet_execution.md)
