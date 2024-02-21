
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

    # -------- Shape Constraints --------
    
    # ----- General -----
    
    # Diagnols are clear in all phases
    s.t. c_diagnol: sum {i in 1..sat_max, k in 1..4} X[i,i,k] = 0;

    # Counts are correct
    s.t. c_total_1: tot_1 >= 3;
    s.t. c_total_2: tot_2 >= tot_1 * tot_1;
    s.t. c_total_3: tot_3 >= tot_1*(tot_1+1);
    s.t. c_total_4: tot_4 = tot_1;
    
    # ----- Phase 1 -----
    
    # Make sure first phase is in 1 line
    # CPLEX Solver does not work with exists (this line)
    s.t. c_single_line: exists {i in 1..sat_max} (sum {j in 1..sat_max} X[i,j,1]) == tot_1;
    
    # ----- Phase 2 -----
    
#     s.t. c_3: sum {i in 1..sat_max} (sum {j in 1..sat_max} X[j,i,1])*(sum {j in 1..sat_max} X[i,j,2]) == tot_1*tot_1;
#     s.t. c_4: sum {j in 1..sat_max} (sum {i in 1..sat_max} X[i,j,1])*(sum {i in 1..sat_max} X[i,j,2]) == tot_1*(tot_1-1);
        
    s.t. c_3: forall {i in 1..sat_max} tot_1*(sum {j in 1..sat_max} X[j,i,1]) == sum {j in 1..sat_max} X[i,j,2];
    s.t. c_4: forall {j in 1..sat_max} (tot_1-1)*(sum {i in 1..sat_max} X[i,j,1]) == sum {i in 1..sat_max} X[i,j,2];
    
    # ----- Phase 3 -----
    
    # Phase 1 and 2 added gives phase 3
    s.t. c_phase_3: forall {i in 1..sat_max, j in 1..sat_max} X[i,j,3] == X[i,j,1] + X[i,j,2];
    
    # ----- Phase 4 -----
    
    # Last phase is a transpose of the first phase
    s.t. c_phase_4: forall {i in 1..sat_max, j in 1..sat_max} X[j,i,1] == X[i,j,4];
    
    
