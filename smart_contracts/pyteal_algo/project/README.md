# A page for Smart Contracts and other stuff that is On-Chain



## Setup test environment and install packages
To setup a test environment for Algorand Smart Contracts, the following youtube video can be used:
https://www.youtube.com/watch?v=V3d3VTlgMo8&list=WL&index=6
The following is a walkthrough of what is in this video for Windows OS however better functionality might come from Linux.

### Install Docker
First install Docker. The link for Docker Desktop is:
https://www.docker.com/products/docker-desktop/

### Get Sandbox


### Get Project workspace template






# Setup

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Install [Algorand sandbox](https://github.com/algorand/sandbox)
3. Add this project folder as bind volume in sandbox `docker-compose.yml` under key `services.algod`:
    ```yml
    volumes:
      - type: bind
        source: <path>
        target: /data
    ```
4. Start sandbox:
    ```txt
    $ ./sandbox up
    ```
5. Install Python virtual environment in project folder:
    ```txt
    $ python -m venv venv
    $ source ./venv/Scripts/activate # Windows
    $ source ./venv/bin/activate # Linux
    ```
6. Use Python interpreter: `./venv/Scripts/python.exe`
    VSCode: `Python: Select Interpreter`

# Links
- [Youtube Pyteal Course](https://youtube.com/playlist?list=PLpAdAjL5F75CNnmGbz9Dm_k-z5I6Sv9_x)
- [Official Algorand Smart Contract Guidelines](https://developer.algorand.org/docs/get-details/dapps/avm/teal/guidelines/)
- [PyTeal Documentation](https://pyteal.readthedocs.io/en/latest/index.html)
- [Algorand DevRel Example Contracts](https://github.com/algorand/smart-contracts)















DiD.py is the current Smart Contract in developement for Digital Identities required for the Space DAO project. It is based upon the Etheruem Standard ERC725.

The following version changes are required in the requirements.txt file when downloading the system

## Make sure venv is active
In python terminal make sure that the venv is active either by seeing (venv) in the command window or by typing:
```
source ./venv/Scripts/activate
```

## Setup Sandbox Network
In the bash terminal, start by moving into the path Algorand/sandbox.
Start the network with:
```
./sandbox up
```
Stop the network with
```
./sandbox down
```
Wipe the network with:
```
./sandbox reset
```
Enter the network with:
```
./sandbox enter algod
```
Exit the network with:
```
exit
```

## To compile pyteal files into approval.teal and clear.teal
The following code in the python terminal will compile DiD.py into two seperate teal files
```
./build.sh contracts.erc725.DiD
```

## To quickly launch the compiled program onto a test network
On bash terminal inside the algod client
```
goal account list
$ONE=address
$TWO=address
$THREE=address
goal app create --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-ints 3 --global-byteslices 3 --local-ints 5 --local-byteslices 5 --creator $ONE
goal app optin --app-id 1 --from $ONE
goal app optin --app-id 1 --from $TWO --app-arg "str:new" --app-arg "str:REQ" --app-arg "str:appl" --app-arg "str:appl"
goal app optin --app-id 1 --from $THREE --app-arg "str:join" --app-account $TWO
```

## How to uninstall Docker when it inevitably stops working
Before uninstalling, try to put the following line into an ADMIN CMD.
```
"C:\Program Files\Docker\Docker\DockerCli.exe" -SwitchDaemon
```
Then kind of jiggle it around a bit by quitting when it errors and open it again and then maybe put the line above back into the ADMIN CMD again. This might fix it, probably not, but you never know.

To uninstall docker you have to delete the registry key from the registry editor.
Search registry editor in windows search bar then navigate too and delete:
```
.Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Docker
```
After this is completed docker can be reinstalled and it might work this time.



## Various other code
View variable values:
```
echo $variable_name
```
View local variables associated with wallet address
```
goal app read --app-id 1 --guess-format --local --from $ONE
```
View global variables contract
```
goal app read --global --app-id 1 --guess-format
```
Debugging
```
previous +
--dryrun-dump -o tx.dr
```



