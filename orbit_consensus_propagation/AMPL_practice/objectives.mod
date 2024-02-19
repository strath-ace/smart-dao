
    option display_width 150;

    set TIMESTEPS ordered;
    set SATS_1 ordered;
    set SATS_2 ordered;

    param sat_max >= 4;
    param timestep_max >= 1;

    # If set more than or equal too do 0
    # If set more than do 1
    param ADD = 1;

    # param cost {SATS} > 0;
    # param f_min {SATS} >= 0;
    # param f_max {j in SATS} >= f_min[j];

    # param n_min {TIMESTEPS} >= 0;
    # param n_max {i in TIMESTEPS} >= n_min[i];

    param conns {SATS_1,SATS_2,TIMESTEPS} >= 0;

    param combs_num integer >= 4;

    # param combs = 6 * ( prod {i in 1..5} i ) / ( (prod {j in 1..3} j) * (prod {k in 1..(5-3)} k) ):

    var sats{1..combs_num} binary;
    # 1 2 3 4
    # 1 2 3 5
    # 1 2 4 5
    param c{1..combs_num,1..4} integer;

    # var time in {1..timestep_max};

    # ----------

    # t0
    param t0s12 {j in 1..combs_num} = min {i in 1..timestep_max} conns[c[j,1],c[j,2],i];
    param t0s13 {j in 1..combs_num} = min {i in 1..timestep_max} conns[c[j,1],c[j,3],i];
    param t0s14 {j in 1..combs_num} = min {i in 1..timestep_max} conns[c[j,1],c[j,4],i];
    # param t0s12 = min {i in 1..timestep_max} conns[1,2,i];
    # param t0s13 = min {i in 1..timestep_max} conns[1,3,i];
    # param t0s14 = min {i in 1..timestep_max} conns[1,4,i];

    # Group 1
    param t1s121 {j in 1..combs_num} = min {i in (t0s12[j]+ADD)..timestep_max} conns[c[j,2],c[j,1],i];
    param t1s131 {j in 1..combs_num} = min {i in (t0s13[j]+ADD)..timestep_max} conns[c[j,3],c[j,1],i];
    param t1s141 {j in 1..combs_num} = min {i in (t0s14[j]+ADD)..timestep_max} conns[c[j,4],c[j,1],i];
    param t1g1 {j in 1..combs_num} = max (t1s121[j], t1s131[j], t1s141[j]);     # This should be 2f+1 rather than max
    # param t1s121 = min {i in (t0s12[1]+ADD)..timestep_max} conns[2,1,i];
    # param t1s131 = min {i in (t0s13[1]+ADD)..timestep_max} conns[3,1,i];
    # param t1s141 = min {i in (t0s14[1]+ADD)..timestep_max} conns[4,1,i];
    # param t1g1 = max (t1s121, t1s131, t1s141);      # This should be 2f+1 rather than max

    # Group 2
    param t1s132 {j in 1..combs_num} = min {i in (t0s13[j]+ADD)..timestep_max} conns[c[j,3],c[j,2],i];
    param t1s142 {j in 1..combs_num} = min {i in (t0s14[j]+ADD)..timestep_max} conns[c[j,4],c[j,2],i];
    param t1g2 {j in 1..combs_num} = max (t0s12[j], t1s132[j], t1s142[j]);
    # param t0s12
    #param t1s132 = min {i in (t0s13[1]+ADD)..timestep_max} conns[3,2,i];
    #param t1s142 = min {i in (t0s14[1]+ADD)..timestep_max} conns[4,2,i];
    #param t1g2 = max (t0s12[1], t1s132, t1s142);     # This should be 2f+1 rather than max

    # Group 3
    # param t0s13
    param t1s123 = min {i in (t0s12[1]+ADD)..timestep_max} conns[2,3,i];
    param t1s143 = min {i in (t0s14[1]+ADD)..timestep_max} conns[4,3,i];
    param t1g3 = max (t0s13[1], t1s123, t1s143);     # This should be 2f+1 rather than max

    # Group 4
    # param t0s14
    param t1s124 = min {i in (t0s12[1]+ADD)..timestep_max} conns[2,4,i];
    param t1s134 = min {i in (t0s13[1]+ADD)..timestep_max} conns[3,4,i];
    param t1g4 = max (t0s14[1], t1s124, t1s134);     # This should be 2f+1 rather than max

    # ------------

    # Set 1
    param t2s21 = min {i in (t1g2[1]+ADD)..timestep_max} conns[2,1,i];
    param t2s31 = min {i in (t1g3+ADD)..timestep_max} conns[3,1,i];
    param t2s41 = min {i in (t1g4+ADD)..timestep_max} conns[4,1,i];

    # Set 2
    param t2s12 = min {i in (t1g1[1]+ADD)..timestep_max} conns[1,2,i];
    param t2s32 = min {i in (t1g3+ADD)..timestep_max} conns[3,2,i];
    param t2s42 = min {i in (t1g4+ADD)..timestep_max} conns[4,2,i];

    # Set 3
    param t2s13 = min {i in (t1g1[1]+ADD)..timestep_max} conns[1,3,i];
    param t2s23 = min {i in (t1g2[1]+ADD)..timestep_max} conns[2,3,i];
    param t2s43 = min {i in (t1g4+ADD)..timestep_max} conns[4,3,i];
 
    # Set 4
    param t2s14 = min {i in (t1g1[1]+ADD)..timestep_max} conns[1,4,i];
    param t2s24 = min {i in (t1g2[1]+ADD)..timestep_max} conns[2,4,i];
    param t2s34 = min {i in (t1g3+ADD)..timestep_max} conns[3,4,i];
    
    # ------------

    param set1 = max (t2s21, t2s31, t2s41);     # This should be 2f+1 rather than max
    param t3set1_s1 = set1;
    param set2 = max (t2s12, t2s32, t2s42);     # This should be 2f+1 rather than max
    param t3set2_s1 = min {i in (set2+ADD)..timestep_max} conns[2,1,i];
    param set3 = max (t2s13, t2s23, t2s43);     # This should be 2f+1 rather than max
    param t3set3_s1 = min {i in (set3+ADD)..timestep_max} conns[3,1,i];
    param set4 = max (t2s14, t2s24, t2s34);     # This should be 2f+1 rather than max
    param t3set4_s1 = min {i in (set4+ADD)..timestep_max} conns[4,1,i];

    # -------------

    param consensus_time1234_1 {j in 1..combs_num} = max(t3set1_s1, t3set2_s1, t3set3_s1, t3set4_s1);     # This should be 2f+1 rather than max

    # -------------

    maximize Total_Cost:
    sats[1] * consensus_time1234_1[1] + sats[2] + sats[3] + sats[4] + sats[5] + sats[6]
    ;

    # -------------

    s.t. c1 {j in 1..combs_num}:  t0s12[j] + ADD <= timestep_max;
    s.t. c2 {j in 1..combs_num}:  t0s13[j] + ADD <= timestep_max;
    s.t. c3 {j in 1..combs_num}:  t0s14[j] + ADD <= timestep_max;
    
    s.t. c4 {j in 1..combs_num}:  t1s121[j] + ADD <= timestep_max;
    s.t. c5 {j in 1..combs_num}:  t1s131[j] + ADD <= timestep_max;
    s.t. c6 {j in 1..combs_num}:  t1s141[j] + ADD <= timestep_max;
    
    s.t. c7 {j in 1..combs_num}:  t1s132[j] + ADD <= timestep_max;
    s.t. c8 {j in 1..combs_num}:  t1s142[j] + ADD <= timestep_max;
    
    s.t. c9:  t1s123 + ADD <= timestep_max;
    s.t. c10:  t1s143 + ADD <= timestep_max;
    
    s.t. c11:  t1s124 + ADD <= timestep_max;
    s.t. c12:  t1s134 + ADD <= timestep_max;
    
    s.t. c13:  t2s21 + ADD <= timestep_max;
    s.t. c14:  t2s31 + ADD <= timestep_max;
    s.t. c15:  t2s41 + ADD <= timestep_max;
    
    s.t. c16:  t2s12 + ADD <= timestep_max;
    s.t. c17:  t2s32 + ADD <= timestep_max;
    s.t. c18:  t2s42 + ADD <= timestep_max;
    
    s.t. c19:  t2s13 + ADD <= timestep_max;
    s.t. c20:  t2s23 + ADD <= timestep_max;
    s.t. c21:  t2s43 + ADD <= timestep_max;
    
    s.t. c22:  t2s14 + ADD <= timestep_max;
    s.t. c23:  t2s24 + ADD <= timestep_max;
    s.t. c24:  t2s34 + ADD <= timestep_max;
    
    # s.t. c25:  t3set2_s1 + ADD <= timestep_max;
    # s.t. c26:  t3set3_s1 + ADD <= timestep_max;
    # s.t. c27:  t3set4_s1 + ADD <= timestep_max;

    # ------------


    s.t. min_4_sats: sum {i in 1..sat_max} sats[i] >= 4;

    s.t. more_than_zero: consensus_time1234_1[1] >= 4;
