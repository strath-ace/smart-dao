# Orbital Consensus Propagation Research

## About
With an increasing number of satellites in orbit consensus across a heterogeneous group of satellites can lead to more neutral, unbiased and accurate decisions. By looking at the topography of the satellites in orbit over a time period consensus algorithms can be run to determine group decisions (decisions such as: on orbit monitoring of the space environment, automatic detection of natural disaster, etc.). Fault tolerant consensus algorithms such as Practical Byzantine Fault Tolerance (PBFT) require communication with all other network members up to 3 times. In a network with thousands of satellites in space on different trajectories, this time can approach millennia. Therefore, identifying a subset of satellites that can form a sub-network able to converge to a consensus decision in a useful time window, while maximising the number of members to increase consensus accuracy and trustworthiness, can be formulated as a combinatorial optimsiation problem.

- Can we determine the minimum time window to reach consensus for different subsets of satellites?
- How do you optimise between a large enough subset of satellites to maintain security while minimising consensus time?
- How would such a system look for SEM?
- Do different Consensus Algorithms/Mechanisms (PBFT, PAXOS/RAFT, DAG) improve consensus (Consensus time vs security)?
- Can you design satellite constellations that are optimal for specific consensus mechanisms?

## Setup and Run

### Requirements

- Linux Operating System (Some functions may work on Windows)

- Tested with Python 3.7.13 (however other versions may also work)

### Creating virtual environment and installing requirements

##### (OPTION 1) Make new pyenv virtualenv with specific name
Requirements: [pyenv](https://github.com/pyenv/pyenv)
```
pyenv virtualenv 3.7.18 venv-orbit-consensus
cd $THIS_REPO$
pip install -r requirements.txt
```

##### (OPTION 2 - EASIER) Make new python venv manually
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Run

1. Make data with scripts in `MAKE_DATA` by following instructions in [Making Data README](./MAKE_DATA/README.md)

2. Enter one of the following directories to run the functions inside
- KEPLER
- GA
- MOO
- BRUTE 
