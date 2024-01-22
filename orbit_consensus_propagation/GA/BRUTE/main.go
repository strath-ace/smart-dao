// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

import (
   // "encoding/csv"
   // "os"
   "fmt"
   // "strconv"
   "encoding/json"
   "io/ioutil"
   "github.com/schollz/progressbar/v3"
)

const LAG_TIME = 0

const MAX_VAL = 82

const STARTING_SAT = 11

const START_TIME = 1705065251

const DATA_FILE = "../DATA/data_icsmd_10day"

const BIG_DATA = DATA_FILE+"/close_times"

const OUT_FILE = DATA_FILE+"/brute_results.json"

type ASET struct {
   ConsensusTime int
	Set []int
}

type OutStuff struct {
   Best ASET
   Rest []ASET
}

func main () {

   fmt.Println("Building initial combinations")
   bar := progressbar.Default(int64(MAX_VAL*MAX_VAL*MAX_VAL*MAX_VAL))
   // Generate first set
   var future_set [][]int
   for i1:=0;i1<MAX_VAL;i1++ {
      for i2:=0;i2<MAX_VAL;i2++ {
         for i3:=0;i3<MAX_VAL;i3++ {
            for i4:=0;i4<MAX_VAL;i4++ {
            	//if STARTING_SAT != i1 && STARTING_SAT != i2 && STARTING_SAT != i3 && i1 != i2 && i1 != i3 && i2 != i3 {
            	if i4 != i1 && i4 != i2 && i4 != i3 && i1 != i2 && i1 != i3 && i2 != i3 {
               		future_set = append(future_set, []int{i1, i2, i3, i4})
       		}
            }
         }
      }  
      bar.Add(MAX_VAL*MAX_VAL*MAX_VAL)
   }
   fmt.Println(" ")

   // Get all valid times
   var bin_all [][]int
   var trend_min_time []int
   var trend_best_set [][]int
   var trend_next_set [][][]int
   var trend_all_times [][]int
   
   c := 4
   var min_time int
   var occurs bool
   var bin_c []int
   var time int
   for len(future_set) > 0 {
      var best_set []int
      bin_all = future_set
      future_set = nil
      fmt.Println("Length",c,"- Checking", len(bin_all), "combinations")
      bar := progressbar.Default(int64(len(bin_all)))
      var next_set [][]int
      var times []int
      min_time = 9999999999
      occurs = false
      for i:=0;i<len(bin_all);i++{
         bin_c = bin_all[i]
         time = consensus_time3(bin_c, LAG_TIME)
         if time > 4 {
            time = time - START_TIME
            if time < min_time {
               min_time = time
               best_set = bin_c
               occurs = true
            }
            next_set = append(next_set, bin_c)
            times = append(times, time)
         }
         // Update progress bar
         if i % 100 == 0 {
            bar.Add(100)
         }
      }

      if occurs {
         trend_min_time = append(trend_min_time, min_time)
         trend_best_set = append(trend_best_set, best_set)
         trend_next_set = append(trend_next_set, next_set)
         trend_all_times = append(trend_all_times, times)
      }
      save_to_json(trend_best_set, trend_min_time, trend_next_set, trend_all_times)
      fmt.Println(" ")
      var jump bool
      for i:=0;i<len(next_set);i++{
         for j:=0;j<MAX_VAL;j++{
            jump = false
            for k:=0;k<len(next_set[i]);k++{
               if next_set[i][k] == j {
                  jump = true
               }
            }
            if ! jump {
               future_set = append(future_set, append(next_set[i], j))
            }
         }
      }
   
      c += 1
   }

   fmt.Println("Done")
}



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





func save_to_json(trend_best_set [][]int, trend_min_time []int, trend_next_set [][][]int, trend_all_times [][]int) {
	var out_data []OutStuff

   for i:=0;i<len(trend_best_set);i++{
      best := ASET{ConsensusTime: trend_min_time[i], Set: trend_best_set[i]}
      var others []ASET
      for j:=0;j<len(trend_next_set[i]);j++{
         others = append(others, ASET{ConsensusTime: trend_all_times[i][j], Set: trend_next_set[i][j]})
      }
      out_data = append(out_data, OutStuff{Best: best, Rest: others})
   }
	json_bits, _ := json.Marshal(out_data)
	_ = ioutil.WriteFile(OUT_FILE, json_bits, 0644) // Check err
}
