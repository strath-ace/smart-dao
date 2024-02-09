
param N;

param dim1{i in 1..3};
# param dim2;

param T{i in 1..dim1[1], j in 1..dim1[2], k in 1..dim1[3]};

var x0 integer >= 0 <= N;
var x1 integer >= 0 <= N;
var x2 integer >= 0 <= N;
var x3 integer >= 0 <= N;

# param T_sum = sum {i in 1..dim1[1]} (max {j in 1..dim1[2]} T[i,j]);

# var init_x0_x1 = ;

maximize total_time: T[x0, x1, 0]; #max {i in T} i;

# s.t. stuff1: T[x0, x1, 0] > 0;

# s.t. stuff1: x0 <= N;

# s.t. germanium: x2 <= 1500;
# s.t. plastic: x1 + x2 <= 1750;
# s.t. copper: 4.04 * x1 + 2.02 * x2 <= 4800;
