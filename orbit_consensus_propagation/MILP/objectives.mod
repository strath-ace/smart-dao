
    option display_width 150;

    param sat_max >= 4;
    param timestep_max >= 1;

    # If set more than or equal too do 0
    # If set more than do 1
    param ADD = 1;

    var X {1..sat_max,1..sat_max,1..4} binary;
    
    var tot_1 = sum {i in 1..sat_max, j in 1..sat_max} X[i,j,1];
    var tot_2 = sum {i in 1..sat_max, j in 1..sat_max} X[i,j,2];
    var tot_3 = sum {i in 1..sat_max, j in 1..sat_max} X[i,j,3];
    var tot_4 = sum {i in 1..sat_max, j in 1..sat_max} X[i,j,4];
    

    minimize X_grid:
    tot_1+tot_2+tot_3+tot_4
    ;

#     s.t. c1 {j in 1..combs_num}:  t0s12[j] + ADD <= timestep_max;
#     s.t. c2 {j in 1..combs_num}:  t0s13[j] + ADD <= timestep_max;

    s.t. c_diagnol: sum {i in 1..sat_max, k in 1..4} X[i,i,k] = 0;

    s.t. c_total_1: tot_1 >= 3;
    s.t. c_total_2: tot_2 >= tot_1 * tot_1;
    s.t. c_total_3: tot_3 >= tot_1*(tot_1+1);
    s.t. c_total_4: tot_4 = tot_1;
    
    s.t. c_1: (sum {j in 1..sat_max} X[1,j,1]) == tot_1;
    
#     param counter = if (sum {j in 1.._sat_max} X[i,j,0]) = ;
    
    # s.t. c25:  t3set2_s1 + ADD <= timestep_max;
    # s.t. c26:  t3set3_s1 + ADD <= timestep_max;
    # s.t. c27:  t3set4_s1 + ADD <= timestep_max;

    # ------------


#     s.t. min_4_sats: sum {i in 1..sat_max, j in 1..sat_max} X[i,j,1] >= 4;
