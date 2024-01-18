// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

import (
   "C"
)

func main() {}


//export consensus_time1
func consensus_time1(documentPtr *C.char) (C.int) {

	primary := 0

	var pass bool
	var max_time, num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	pass, t_local, num_sats, sat_data_big = get_initial(documentPtr)
	if ! pass {
		return C.int(1)
	}
	
	// ################# Start Consensus

	pass, max_time, _, _ = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if pass {
		return C.int(max_time)
	} else {
		return C.int(1)
	}
	
}


//export consensus_time2
func consensus_time2(documentPtr *C.char) (C.int) {

	var LAG_TIME int
	_, _, LAG_TIME = load_config()

	primary := 0

	var pass bool
	var max_time, num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	pass, t_local, num_sats, sat_data_big = get_initial(documentPtr)
	if ! pass {
		return C.int(1)
	}

	// ################# Start Consensus
	
	pass, _, t_local, _ = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int(1)
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	pass, max_time, _, _ = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if pass {
		return C.int(max_time)	
	} else {
		return C.int(2)
	}
	
}


//export consensus_time3
func consensus_time3(documentPtr *C.char) (C.int) {

	var LAG_TIME int
	_, _, LAG_TIME = load_config()

	primary := 0

	var pass bool
	var max_time, num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	pass, t_local, num_sats, sat_data_big = get_initial(documentPtr)
	if ! pass {
		return C.int(1)
	}

	// ################# Start Consensus
	
	pass, _, t_local, _ = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int(1)
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	pass, _, t_local, _ = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int(2)
	}

	pass, max_time, _, _ = consensus_commit(t_local, sat_data_big, num_sats, completeness)
	if pass {
		return C.int(max_time)	
	} else {
		return C.int(3)
	}
}


//export consensus_time4
func consensus_time4(documentPtr *C.char) (C.int) {

	var LAG_TIME int
	_, _, LAG_TIME = load_config()

	primary := 0

	var pass bool
	var max_time, num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	pass, t_local, num_sats, sat_data_big = get_initial(documentPtr)
	if ! pass {
		return C.int(1)
	}

	// ################# Start Consensus
	
	pass, _, t_local, _ = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int(1)
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	pass, _, t_local, _ = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int(2)
	}

	pass, _, t_local, _ = consensus_commit(t_local, sat_data_big, num_sats, completeness)
	if ! pass {
		return C.int(3)
	}

	pass, max_time, _ = consensus_reply(t_local, sat_data_big, num_sats, primary, completeness)
	if pass {
		return C.int(max_time)	
	} else {
		return C.int(4)
	}
}


//export consensus_completeness_abs
func consensus_completeness_abs(documentPtr *C.char) (C.int) {

	var LAG_TIME int
	_, _, LAG_TIME = load_config()

	primary := 0

	var pass bool
	var num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	completeness = 1

	pass, t_local, num_sats, sat_data_big = get_initial(documentPtr)
	if ! pass {
		return C.int(completeness)
	}

	// ################# Start Consensus
	
	pass, _, t_local, completeness = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int(completeness)
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	pass, _, t_local, completeness = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int(completeness)
	}

	pass, _, t_local, completeness = consensus_commit(t_local, sat_data_big, num_sats, completeness)
	if ! pass {
		return C.int(completeness)
	}

	pass, _, completeness = consensus_reply(t_local, sat_data_big, num_sats, primary, completeness)
	return C.int(completeness)
}


//export consensus_completeness_per
func consensus_completeness_per(documentPtr *C.char) (C.int) {

	var LAG_TIME int
	_, _, LAG_TIME = load_config()

	primary := 0

	var pass bool
	var num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	completeness = 1

	

	pass, t_local, num_sats, sat_data_big = get_initial(documentPtr)
	if ! pass {
		return C.int(completeness)
	}

	completeness_divider := ((2*num_sats*num_sats) - num_sats) - 1

	// ################# Start Consensus
	
	pass, _, t_local, completeness = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int((10000*completeness)/completeness_divider)
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	pass, _, t_local, completeness = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int((10000*completeness)/completeness_divider)
	}

	pass, _, t_local, completeness = consensus_commit(t_local, sat_data_big, num_sats, completeness)
	if ! pass {
		return C.int((10000*completeness)/completeness_divider)
	}

	pass, _, completeness = consensus_reply(t_local, sat_data_big, num_sats, primary, completeness)
	if ! pass {
		return C.int((10000*completeness)/completeness_divider)
	} else {
		return C.int(10000)
	}
}







