# Server Instructions

ssh connect to server
```
ssh -i ~/esa-server.txt -p 8080 rcowlishaw@91.234.10.110
```

Transfer files from server to local
```
mkdir data-vm
scp -i ~/esa-server.txt -r rcowlishaw@91.234.10.110:workspace/esa-federated-learning/data/* data-vm/

scp -i ~/esa-server.txt -r rcowlishaw@91.234.10.110:workspace/esa-federated-learning/model/*.png model/images/
```

Setup to run python forever (on server)
```
source venv/bin/activate
chmod +x src/sim.py
nohup python src/sim.py > output.log &
ps ax | grep sim.py
kill PID
```


```
pip3 install torch==2.0.0+cu117 torchvision==0.15.0+cu117 -f https://download.pytorch.org/whl/torch_stable.html
```



Server pip list
```
Package                   Version
------------------------- ------------
aiohttp                   3.9.5
aiosignal                 1.3.1
async-timeout             4.0.3
attrs                     23.2.0
certifi                   2024.2.2
cffi                      1.16.0
charset-normalizer        3.3.2
click                     8.1.7
cmake                     3.29.3
colorama                  0.4.6
cryptography              42.0.7
datasets                  2.19.1
dill                      0.3.8
filelock                  3.14.0
flwr                      1.9.0
flwr-datasets             0.1.0
frozenlist                1.4.1
fsspec                    2024.3.1
grpcio                    1.63.0
huggingface-hub           0.23.0
idna                      3.7
iterators                 0.0.2
Jinja2                    3.1.4
jsonschema                4.22.0
jsonschema-specifications 2023.12.1
lit                       18.1.4
markdown-it-py            3.0.0
MarkupSafe                2.1.5
mdurl                     0.1.2
mpmath                    1.3.0
msgpack                   1.0.8
multidict                 6.0.5
multiprocess              0.70.16
networkx                  3.3
numpy                     1.26.4
nvidia-cublas-cu12        12.1.3.1
nvidia-cuda-cupti-cu12    12.1.105
nvidia-cuda-nvrtc-cu12    12.1.105
nvidia-cuda-runtime-cu12  12.1.105
nvidia-cudnn-cu12         8.9.2.26
nvidia-cufft-cu12         11.0.2.54
nvidia-curand-cu12        10.3.2.106
nvidia-cusolver-cu12      11.4.5.107
nvidia-cusparse-cu12      12.1.0.106
nvidia-nccl-cu12          2.18.1
nvidia-nvjitlink-cu12     12.4.127
nvidia-nvtx-cu12          12.1.105
packaging                 24.0
pandas                    2.2.2
pathspec                  0.12.1
pillow                    10.3.0
pip                       23.0.1
protobuf                  4.25.3
pyarrow                   16.1.0
pyarrow-hotfix            0.6
pycparser                 2.22
pycryptodome              3.20.0
Pygments                  2.18.0
python-dateutil           2.9.0.post0
pytz                      2024.1
PyYAML                    6.0.1
ray                       2.6.3
referencing               0.35.1
requests                  2.31.0
rich                      13.7.1
rpds-py                   0.18.1
setuptools                65.5.0
shellingham               1.5.4
six                       1.16.0
sympy                     1.12
tomli                     2.0.1
torch                     2.0.0+cu117
torchaudio                2.1.1+cu118
torchvision               0.15.0+cu117
tqdm                      4.66.4
triton                    2.0.0
typer                     0.9.4
typing_extensions         4.11.0
tzdata                    2024.1
urllib3                   2.2.1
xxhash                    3.4.1
yarl                      1.9.4
```

## Setup and Run

1. Current version tested and developed on python v3.10, ubuntu v24.04. All other pip dependencies are given at bottom of README

2. Run setup file
```
source ./setup.sh
```

3. Configure params.yml for required test

4. Run simulation and output data will be in `./data`
```
source venv/bin/activate
python ./src/sim.py
```

5. Run plotter and output file will be in `./data`
```
source venv/bin/activate
ptyhon ./src/plot.py
```

## Compatible pip packages for python3.10
```bash
Package                   Version
------------------------- -----------
aiohttp                   3.9.5
aiosignal                 1.3.1
async-timeout             4.0.3
attrs                     23.2.0
certifi                   2024.2.2
cffi                      1.16.0
charset-normalizer        3.3.2
click                     8.1.7
colorama                  0.4.6
contourpy                 1.2.1
cryptography              42.0.7
cycler                    0.12.1
datasets                  2.19.1
dill                      0.3.8
filelock                  3.14.0
flwr                      1.9.0
flwr-datasets             0.1.0
fonttools                 4.51.0
frozenlist                1.4.1
fsspec                    2024.3.1
grpcio                    1.63.0
huggingface-hub           0.23.0
idna                      3.7
iterators                 0.0.2
Jinja2                    3.1.4
jsonschema                4.22.0
jsonschema-specifications 2023.12.1
kiwisolver                1.4.5
markdown-it-py            3.0.0
MarkupSafe                2.1.5
matplotlib                3.8.4
mdurl                     0.1.2
mpmath                    1.3.0
msgpack                   1.0.8
multidict                 6.0.5
multiprocess              0.70.16
networkx                  3.3
numpy                     1.26.4
nvidia-cublas-cu12        12.1.3.1
nvidia-cuda-cupti-cu12    12.1.105
nvidia-cuda-nvrtc-cu12    12.1.105
nvidia-cuda-runtime-cu12  12.1.105
nvidia-cudnn-cu12         8.9.2.26
nvidia-cufft-cu12         11.0.2.54
nvidia-curand-cu12        10.3.2.106
nvidia-cusolver-cu12      11.4.5.107
nvidia-cusparse-cu12      12.1.0.106
nvidia-nccl-cu12          2.18.1
nvidia-nvjitlink-cu12     12.4.127
nvidia-nvtx-cu12          12.1.105
packaging                 24.0
pandas                    2.2.2
pathspec                  0.12.1
pillow                    10.3.0
pip                       23.0.1
protobuf                  4.25.3
pyarrow                   16.0.0
pyarrow-hotfix            0.6
pycparser                 2.22
pycryptodome              3.20.0
pydantic                  1.10.15
Pygments                  2.18.0
pyparsing                 3.1.2
python-dateutil           2.9.0.post0
pytz                      2024.1
PyYAML                    6.0.1
ray                       2.6.3
referencing               0.35.1
requests                  2.31.0
rich                      13.7.1
rpds-py                   0.18.1
setuptools                65.5.0
shellingham               1.5.4
six                       1.16.0
sympy                     1.12
tomli                     2.0.1
torch                     2.1.1
torchvision               0.16.1
tqdm                      4.66.4
triton                    2.1.0
typer                     0.9.4
typing_extensions         4.11.0
tzdata                    2024.1
urllib3                   2.2.1
xxhash                    3.4.1
yarl                      1.9.4
```
