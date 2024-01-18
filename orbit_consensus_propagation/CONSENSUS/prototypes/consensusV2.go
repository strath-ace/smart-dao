// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package consensus

import (
   "encoding/csv"
   "os"
   "fmt"
   "strconv"
)

func consensus_time3(bin_li []int, LAG_TIME int, DIS float64) (bool, int) {

	// ################# Check input is okay

	// if check_input(bin_li) {
	// 	fmt.Println("BAD INPUT EXITING")
	// 	return false, 0.0
	// }

	// ################# Set Vars

	num_sats := len(bin_li)
	
	primary := 0
	var t_local []int
	var conn_time int
	var max_time int

	for i:=0;i<num_sats;i++{
		t_local = append(t_local, START_TIME)
	}	

	// ################# Load data files

	var sat_data_big [][][]int
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

	// ################# Start Consensus
	
	// Pre-prepare
	for j:=0;j<num_sats;j++ {
		if primary != j {
			conn_time = find_next_conn(t_local[primary], sat_data_big[primary][j])
			if conn_time == -1 {
				return false, 0.0
			}
			t_local[j] = conn_time
		}	
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	// Prepare
	for j:=0;j<num_sats;j++ {
		max_time = 0
		for i:=0;i<num_sats;i++ {
			if i != j && i != primary{
				conn_time = find_next_conn(t_local[i], sat_data_big[j][i])
				if conn_time == -1 {
					return false, 0.0
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}

	// Commit
	for j:=0;j<num_sats;j++ {
		max_time = 0
		for i:=0;i<num_sats;i++ {
			if i != j {
				conn_time = find_next_conn(t_local[i], sat_data_big[j][i])
				if conn_time == -1 {
					return false, 0.0
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}

	// Reply
	max_time = 0
	for i:=0;i<num_sats;i++ {
		if i != primary {
			conn_time = find_next_conn(t_local[i], sat_data_big[i][primary])
			if conn_time == -1 {
				return false, 0.0
			}
			if max_time < conn_time {
				max_time = conn_time
			}
		}	
	}
	return true, max_time
}



func delete_element(slice []int, index int) []int {
	return append(slice[:index], slice[index+1:]...)
 }


func find_next_conn(t_0 int, sat_data []int) int {
	for t:=0;t<len(sat_data);t++{
		if sat_data[t] > t_0 {
			return sat_data[t]
		}
	}
	return -1
}


func read_data_string(file_name string) (out_data []int) {
	// Open the CSV file
	file, err := os.Open(file_name)
	if err != nil {
		fmt.Println("FILE NOT OPENING, MAY NOT EXIST")
	}
	defer file.Close()
	// Read the CSV data
	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1 // Allow variable number of fields
	data, _ := reader.ReadAll()
	for _, item := range data[0] {
		out_data = append(out_data, int(atoi(item)))
	}
	return out_data
}

func atoi(in string) float64 {
	value, _ := strconv.ParseFloat(in, 64)
	return value
}


func check_input(bin_li []int) bool {
	// If input array is not long enough error
	if len(bin_li) < 4 {
		return true
		
	}
	// If bin_li is not unique
	for i:=0;i<len(bin_li);i++{
		for j:=0;j<len(bin_li);j++{
			if i != j {
				if bin_li[i]==bin_li[j]{
					return true
				}
			}
		}
	}
	// If passes checks
	return false
}
