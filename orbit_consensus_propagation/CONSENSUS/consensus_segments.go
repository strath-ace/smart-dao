// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

// Consensus Segments

// This file contains:
// A. Initial data gatherer
// B. Consensus Segments
// C. Find next connection function

// STEPS:
// 0. Get initial data
// 1. Pre-Prepare
// 2. Prepare
// 3. Commit
// 4. Reply

// #########################

package main

import (
   "strconv"
   "C"
   "encoding/json"
)

// Get Initial Data for Consensus
func get_initial(documentPtr *C.char) (pass bool, t_local []int, num_sats int, sat_data_big [][][]int) {

	var START_TIME int
	var BIG_DATA string
	START_TIME, BIG_DATA, _ = load_config()

	documentString := C.GoString(documentPtr)
	var jsonDocument map[string][]int
	_ = json.Unmarshal([]byte(documentString), &jsonDocument)
	bin_li := jsonDocument["ids"]

	// ################# Check input is okay

	num_sats = len(bin_li)

	if check_input(bin_li) {
		// fmt.Println("BAD INPUT EXITING")
		return false, nil, 0, nil
	}

	for i:=0;i<num_sats;i++{
		t_local = append(t_local, START_TIME)
	}

	for i, sat1 := range bin_li {
		var temp [][]int
		for j, sat2 := range bin_li {
			if i!=j {
				temp = append(temp, read_data_string(BIG_DATA+"/"+strconv.Itoa(sat1)+"_"+strconv.Itoa(sat2)+".csv"))
			} else {
				temp = append(temp, []int{0})
			}
		}
		sat_data_big = append(sat_data_big, temp)
	}
	return true, t_local, num_sats, sat_data_big
}


// PRE-PREPARE
func consensus_pre_prepare(t_local []int, sat_data_big [][][]int, num_sats int, primary int, completeness int) (bool, int, []int, int) {
	var conn_time int
	var max_time int
	for j:=0;j<num_sats;j++ {
		if primary != j {
			conn_time = find_next_conn(t_local[primary], sat_data_big[primary][j])
			if conn_time == -1 {
				return false, 0, nil, completeness
			}
			t_local[j] = conn_time
			completeness += 1
			if max_time < conn_time {
				max_time = conn_time
			}
		}	
	}
	return true, max_time, t_local, completeness
}


// PREPARE
func consensus_prepare(t_local []int, sat_data_big [][][]int, num_sats int, primary int, completeness int) (bool, int, []int, int) {
	var conn_time int
	var max_time int
	for j:=0;j<num_sats;j++ {
		max_time = 0
		for i:=0;i<num_sats;i++ {
			if i != j && i != primary{
				conn_time = find_next_conn(t_local[i], sat_data_big[j][i])
				if conn_time == -1 {
					return false, 0, nil, completeness
				}
				completeness += 1
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}
	max_time = get_max(t_local)
	return true, max_time, t_local, completeness
}


// COMMIT
func consensus_commit(t_local []int, sat_data_big [][][]int, num_sats int, completeness int) (bool, int, []int, int) {
	var conn_time int
	var max_time int
	for j:=0;j<num_sats;j++ {
		max_time = 0
		for i:=0;i<num_sats;i++ {
			if i != j {
				conn_time = find_next_conn(t_local[i], sat_data_big[j][i])
				if conn_time == -1 {
					return false, 0, nil, completeness
				}
				completeness += 1
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}
	max_time = get_max(t_local)
	return true, max_time, t_local, completeness
}


// REPLY
func consensus_reply(t_local []int, sat_data_big [][][]int, num_sats int, primary int, completeness int) (bool, int, int) {
	var conn_time int
	var max_time int
	for i:=0;i<num_sats;i++ {
		if i != primary {
			conn_time = find_next_conn(t_local[i], sat_data_big[i][primary])
			if conn_time == -1 {
				return false, 0, completeness
			}
			completeness += 1
			if max_time < conn_time {
				max_time = conn_time
			}
		}	
	}
	return true, max_time, completeness
}



// Find next valid connection in sat_data
func find_next_conn(t_0 int, sat_data []int) int {
	for t:=0;t<len(sat_data);t++{
		if sat_data[t] >= t_0 {
			return sat_data[t]
		}
	}
	return -1
}
