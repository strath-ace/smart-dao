// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

import (
)


func consensus_time3(bin_li []int, LAG_TIME int) (int) {

	primary := 0

	var pass bool
	var max_time, num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	pass, t_local, num_sats, sat_data_big = get_initial(bin_li)
	if ! pass {
		return 1
	}

	// ################# Start Consensus
	
	pass, _, t_local, _ = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return 1
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	pass, _, t_local, _ = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return 2
	}

	pass, _, t_local, _ = consensus_commit(t_local, sat_data_big, num_sats, completeness)
	if ! pass {
		return 3
	}

	pass, max_time, _ = consensus_reply(t_local, sat_data_big, num_sats, primary, completeness)
	if pass {
		return max_time
	} else {
		return 4
	}
}