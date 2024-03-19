# How to do c++ stuff in gurobi

1. Have installed gurobi

2. Run code to build file.

Template:
```
g++ "filename" -Wall -std=c++11 -O3 -o "outputfilename" -I "path to the include folder of your gurobi" -L "path to the lib folder of your gurobi" -lgurobi_c++ "your gurobi version"
```

My version:
```
g++ test.cpp -Wall -std=c++11 -O3 -o test -I ~/GUROBI/gurobi1100/linux64/include -L ~/GUROBI/gurobi1100/linux64/lib -lgurobi_c++ -lgurobi110
```

