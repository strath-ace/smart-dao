# SMART DAO

Decentralised Autonomous Organisation (DAO) and other Distributed Ledger Technologies (DLT) for Satellite-based Emergency Mapping

### Projects

This repository contains the code for many different projects and scientific articles. The following is a list of these projects and the link to the repository:

- [:newspaper:](https://ieeexplore.ieee.org/abstract/document/10338847) - [:computer:](/sem_analysis/) - Automating and Decentralising Satellite-based Emergency Mapping
- [:newspaper:](https://www.researchgate.net/publication/379723426_Decentralized_And_Neutral_Consensus_Mechanisms_in_Space_Conjunctions_Assessment_and_Mitigation_Space_DAO_STM) - [:computer:](https://gitlab.com/spacedao) - SpaceDAO Project
- [:newspaper:](https://pureportal.strath.ac.uk/en/publications/proof-of-optimality-for-a-decentralised-eo-data-processing-archit) - [:computer:](/smart_contracts/) - Proof of Optimality for a Decentralised EO Data Processing Architecture
- [:newspaper:](https://ieeexplore.ieee.org/abstract/document/10612025) - [:computer:](/orbit_consensus_propagation/) - Multi-objective optimisation strategy for on-orbit fault-tolerant decision making
- [:newspaper:](https://ieeexplore.ieee.org/abstract/document/10678934) - [:computer:](/orbit_consensus_propagation/) - Optimizing participant selection for fault-tolerant decision making in orbit using mixed integer linear programming
- :no_entry: - [:computer:](/orbit_consensus_propagation/SIM_SAT/) - Advancing Satellite Network Consensus through Optimal Orbital Configurations (Coming Soon)
- :no_entry: - :no_entry: - Federated learning paper (Coming Soon)

Read more overviews about the work below


### Automating and Decentralising Satellite-based Emergency Mapping

The quantity and diversity of stakeholders in space is increasing and centralised management of their assets is becoming more complex. New technologies in Web3 such as Decentralised Autonomous Organisations (DAOs) can bridge the communication gap with neutral and automated systems, and distribute currently centralised processes that are inherently decentralised by nature. One of these processes is Satellite-based Emergency Mapping (SEM) for Disaster Response Management (DRM). With automated decision strategies and transparent ledgers, a fairer and more accessible system can be built to handle the increase in stakeholders as well as the increasing number of natural disasters occurring. A DAO also address' the key issue with the current SEM process, such as decreasing the current three days wait, required to produce the necessary processed and analysed data for end users, after the disaster occurs. Moreover, with fleets of satellites belonging to different governmental and private organisations, a specific central authority cannot be identified to manage the process in an efficient and equitable way. The paper discusses the need for a more decentralised and automated system for DRM by presenting evidence of current bottlenecks and lays the foundations of the first DAO for on-orbit assets management and demonstrates which Web3 technologies could further improve SEM in this first phase of charter activation.

The work was produced by Robert Cowlishaw of the Intelligent Computational Engineering Laboratory (ICE Lab) of the University of Strathclyde, UK.

This repository `sem_analysis` contains the code of the [paper](https://ieeexplore.ieee.org/abstract/document/10338847) published in the [2023 Fifth International Conference on Blockchain Computing and Applications (BCCA)](https://ieeexplore.ieee.org/servlet/opac?punumber=10338825).

If you are using this code in full or in part, please cite our work as:
```bibtex
@inproceedings{cowlishaw2023automating,
    title={Automating and decentralising satellite-based emergency mapping},
    author={Cowlishaw, Robert and Boumghar, Red and Arulselvan, Ashwin and Riccardi, Annalisa},
    booktitle={2023 Fifth International Conference on Blockchain Computing and Applications (BCCA)},
    pages={76--81},
    year={2023},
    organization={IEEE}
}
```


###  Proof of Optimality for a Decentralised EO Data Processing Architecture

Earth Observation (EO) data is large and often processed in a very centralised manner. Through the decentralisation and distribution of data processing, a more neutral and automated system can be created, while incentivising a more diverse set of data sources. This can help lower the initial barrier for new data providers and help with decreasing the time it takes for data to be created for systems such as Satellite-based Emergency Mapping. Building such architecture on a decentralised network comes with difficulties, such as merging centralised data sources together, building trust or reputation on a trustless system, and building processes and methods that require low enough computational cost to be executable on distributed networks. This paper discusses how to offload and on-load data onto a distributed network to overcome these computational challenges.

The work was produced by Robert Cowlishaw of the Intelligent Computational Engineering Laboratory (ICE Lab) of the University of Strathclyde, UK.

This repository `smart_contracts` contains the code of the [paper](https://pureportal.strath.ac.uk/en/publications/proof-of-optimality-for-a-decentralised-eo-data-processing-archit) published in the [Proceedings of the 2023 conference on Big Data from Space (BiDS’23)](https://op.europa.eu/en/publication-detail/-/publication/10ba86b1-7c63-11ee-99ba-01aa75ed71a1/language-en).

If you are using this code in full or in part, please cite our work as:
```bibtex
@inproceedings{cowlishaw2023proof,
  title={Proof of optimality for a decentralised EO data processing architecture},
  author={Cowlishaw, Robert and Riccardi, Annalisa and Arulselvan, Ashwin},
  booktitle={2023 conference on Big Data from Space (BiDS’23)},
  year={2023}
}
```


### Multi-Objective Optimisation strategy for On-Orbit Fault-Tolerant Decision Making

With an increasing number of satellites in orbit, consensus across a heterogeneous group of satellites can lead to a more neutral, unbiased, and accurate decisions. Fault tolerant consensus algorithms such as Practical Byzantine Fault Tolerance (pBFT) require communication with all other network members up to 4 times. In a network with thousands of satellites in space on different trajectories, this time can approach millennia. There-fore, identifying a subset of satellites that can form a sub-network able to converge to a consensus decision in a useful time window, while maximising the number of members to increase consensus accuracy and trustworthiness, can be formulated as a multi-objective combinatorial optimisation problem. The problem is explained and defined with the optimisation method and the consensus algorithm steps described. Metrics for measuring the output of the optimal pareto front are considered and applied to the front computed. The real satellite positions used generate a non-fixed topology and high latency scenario such as that of a real on-orbit decision being made. The trend shown over 100 days of satellite positions propagation with up to 82 International Charter: Space and Major Disasters satellites shows up to 22 satellites can be used in a subset with a near linear increase in consensus time along the optimal pareto front and exponential trend for the mean values computed over 100 runs of the NSGA-II algorithm. The minimum consensus time is found to be 47 minutes for a subset of 4 satellites for the given time frame.

The work was produced by Robert Cowlishaw of the Intelligent Computational Engineering Laboratory (ICE Lab) of the University of Strathclyde, UK.

This repository `orbit_consensus_propagation` contains the code of the [paper](https://ieeexplore.ieee.org/abstract/document/10612025) published in the [Proceedings of the 2024 Congress on Evolutionary Computation (WCCI'24)](https://ieeexplore.ieee.org/xpl/conhome/10609966/proceeding).

```bibtex
@inproceedings{cowlishaw2024multi,
  author={Cowlishaw, Robert and Arulselvan, Ashwin and Riccardi, Annalisa},
  booktitle={2024 IEEE Congress on Evolutionary Computation (CEC)}, 
  title={Multi-Objective Optimisation strategy for On-Orbit Fault-Tolerant Decision Making}, 
  year={2024},
  pages={1-7},
  keywords={Space vehicles;Fault tolerance;Satellites;Accuracy;Fault tolerant systems;Decision making;Consensus algorithm;Consensus;decentralised network;satellites;combinatorial optimisation;multi-objective optimisation;prac-tical byzantine fault tolerance},
  doi={10.1109/CEC60901.2024.10612025}
}
```


### Optimizing Participant Selection for Fault-Tolerant Decision Making in Orbit Using Mixed Integer Linear Programming

In challenging environments such as space, where decisions made by a network of satellites can be prone to inaccuracies or biases, leveraging smarter systems for onboard data processing, decision making is becoming increasingly common. To ensure fault tolerance within the network, consensus mechanisms play a crucial role. However, in a dynamically changing network topology, achieving consensus among all satellites can become excessively time consuming. To address this issue, the practical Byzantine fault-tolerance algorithm is employed, utilizing satellite trajectories as input to determine the time required for achieving consensus across a subnetwork of satellites. To optimize the selection of subsets for consensus, a mixed integer linear programming approach is developed. This method is then applied to analyze the characteristics of optimal subsets using satellites from the International Charter: Space and Major Disasters (ICSMD) over a predefined maximum time horizon. Results indicate that consensus within these satellites can be reached in less than 3.3 h in half of cases studied. Two satellites that are within the maximum communication range at all times are oversubscribed for taking part in the subnetwork. A further analysis has been completed to analyze which are the best set of orbital parameters for taking part in a consensus network as part of the ICSMD.

The work was produced by Robert Cowlishaw of the Intelligent Computational Engineering Laboratory (ICE Lab) of the University of Strathclyde, UK.

This repository `orbit_consensus_propagation` contains the code of the [paper](https://ieeexplore.ieee.org/abstract/document/10678934) published in the [IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing](https://www.grss-ieee.org/publications/journal-of-selected-topics-in-applied-earth-observations-and-remote-sensing/).

```bibtex
@ARTICLE{cowlishaw2024optimizing,
  author={Cowlishaw, Robert and Riccardi, Annalisa and Arulselvan, Ashwin},
  journal={IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing}, 
  title={Optimizing Participant Selection for Fault-Tolerant Decision Making in Orbit Using Mixed Integer Linear Programming}, 
  year={2024},
  volume={17},
  pages={16961-16969},
  keywords={Satellites;Consensus protocol;Space vehicles;Network topology;Fault tolerant systems;Fault tolerance;Topology;Consensus algorithm;fault-tolerant decision making;mixed integer linear programming (MILP);on-orbit decision making;practical Byzantine fault tolerance (pBFT);satellite communication},
  doi={10.1109/JSTARS.2024.3459630}
}
```


### Advancing Satellite Network Consensus through Optimal Orbital Configurations (Coming Soon)
This will be published in the International Astronautical Congress (IAC) proceedings soon.

### Federated Learning Paper
This journal article will be published soon.