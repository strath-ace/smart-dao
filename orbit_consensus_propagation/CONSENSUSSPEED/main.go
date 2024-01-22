// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

import (
   "C"
   "encoding/json"
   "unsafe"
   "fmt"
)

func main() {}



//export consensus_time4
func consensus_time4(documentPtr *C.char, outPtr *float64, n int64) {

	documentString := C.GoString(documentPtr)
	var jsonDocument map[string][][]int
	_ = json.Unmarshal([]byte(documentString), &jsonDocument)
	bin_li := jsonDocument["ids"]

	out_res := unsafe.Slice(outPtr, n)

	var LAG_TIME int
	_, _, LAG_TIME = load_config()

	primary := 0

	var pass bool
	var max_time, num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int
	fmt.Println("test1")
	for spl:=0;spl<len(bin_li);spl++{
		
		pass, t_local, num_sats, sat_data_big = get_initial(bin_li[spl])
		if ! pass {
			out_res[spl] = 1
			continue
		}
		// ################# Start Consensus
		fmt.Println(pass, t_local, num_sats, len(sat_data_big))
		pass, _, t_local, _ = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
		if ! pass {
			out_res[spl] = 1
			continue
		}
		// Decision Lag
		for i:=0;i<num_sats;i++{
			t_local[i] += LAG_TIME
		}
		pass, _, t_local, _ = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
		if ! pass {
			out_res[spl] = 2
			continue
		}
		pass, _, t_local, _ = consensus_commit(t_local, sat_data_big, num_sats, completeness)
		if ! pass {
			out_res[spl] = 3
			continue
		}
		pass, max_time, _ = consensus_reply(t_local, sat_data_big, num_sats, primary, completeness)
		if pass {
			out_res[spl] = float64(max_time)
		} else {
			out_res[spl] = 4
		}
		
	}
	fmt.Println("test2")
}


//export consensus_completeness_per
func consensus_completeness_per(documentPtr *C.char, outPtr *float64, n int64) {

	documentString := C.GoString(documentPtr)
	var jsonDocument map[string][][]int
	_ = json.Unmarshal([]byte(documentString), &jsonDocument)
	bin_li := jsonDocument["ids"]

	out_res := unsafe.Slice(outPtr, n)

	var LAG_TIME int
	_, _, LAG_TIME = load_config()

	primary := 0

	var pass bool
	var num_sats, completeness int
	var t_local []int
	var sat_data_big [][][]int

	for spl:=0;spl<len(bin_li);spl++{
		completeness = 1

		pass, t_local, num_sats, sat_data_big = get_initial(bin_li[spl])
		if ! pass {
			out_res[spl] = 1
			continue
		}
			
		completeness_divider := ((2*num_sats*num_sats) - num_sats) - 1
		// ################# Start Consensus
		
		pass, _, t_local, completeness = consensus_pre_prepare(t_local, sat_data_big, num_sats, primary, completeness)
		if ! pass {
			out_res[spl] = float64((10000*completeness)/completeness_divider)
			continue
		}

		// Decision Lag
		for i:=0;i<num_sats;i++{
			t_local[i] += LAG_TIME
		}

		pass, _, t_local, completeness = consensus_prepare(t_local, sat_data_big, num_sats, primary, completeness)
		if ! pass {
			out_res[spl] = float64((10000*completeness)/completeness_divider)
			continue
		}

		pass, _, t_local, completeness = consensus_commit(t_local, sat_data_big, num_sats, completeness)
		if ! pass {
			out_res[spl] = float64((10000*completeness)/completeness_divider)
			continue
		}

		pass, _, completeness = consensus_reply(t_local, sat_data_big, num_sats, primary, completeness)
		if ! pass {
			out_res[spl] = float64((10000*completeness)/completeness_divider)
		} else {
			out_res[spl] = float64(10000)
		}
	}

}







