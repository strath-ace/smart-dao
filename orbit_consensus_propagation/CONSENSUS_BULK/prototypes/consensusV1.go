// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package consensus

// import (
//    "encoding/csv"
//    "os"
//    "fmt"
//    "strconv"
// )

// func consensus_time2(bin_li []int, LAG_TIME int, DIS float64) (bool, float64) {

// 	// ################# Load bin_li from python

// 	num_sats := len(bin_li)

// 	// ################# Check input is okay

// 	if check_input(bin_li) {
// 		// fmt.Println("BAD INPUT EXITING")
// 		return false, 0.0
// 	}
// 	// ################# Load specific sat files

// 	// Get sat_data for sats in bin_li
// 	var sat_data []string
// 	for i:=0;i<num_sats;i++ {
// 		sat_data = append(sat_data, strconv.Itoa(bin_li[i]))
// 	}

// 	// ################# Run consensus

// 	var sat_data_big [][][]float64
// 	for i, sat1 := range sat_data {
// 		var temp [][]float64
// 		for j, sat2 := range sat_data {
// 			if i!=j {
// 				temp = append(temp, read_data_string(BIG_DATA+"/"+sat1+"_"+sat2+".csv"))
// 			} else {
// 				temp = append(temp, []float64{0})
// 			}
// 		}
// 		sat_data_big = append(sat_data_big, temp)
// 	}


	

// 	primary := 0
// 	var t_local []int

// 	// Get each array required
// 	array_primary := []string{sat_data[primary]}
// 	// array_all := sat_data
// 	// array_red := sat_data
// 	array_all := make([]string, len(sat_data))
// 	copy(array_all, sat_data)
// 	array_red := make([]string, len(sat_data))
// 	copy(array_red, sat_data)
// 	newLength := 0
// 	for index, _ := range array_red {
// 		// Remove other element
// 		if primary != index {
// 			array_red[newLength] = array_red[index]
// 			newLength++
// 		}
// 		// Set time
// 		t_local = append(t_local, 0)
// 	}
// 	array_red = array_red[:newLength]

// 	// Pre-prepare
// 	var sat_data_temp []float64
// 	var conn_time int
// 	for _, _ = range array_primary {
// 		for j, _ := range array_all {
// 			if primary != j {
// 				sat_data_temp = sat_data_big[primary][j]
// 				conn_time = find_next_conn(0, sat_data_temp, DIS)
// 				if conn_time == -1 {
// 					return false, 0.0
// 				}
// 				t_local[j] = conn_time
// 			}	
// 		}
// 	}

// 	// Decision Lag
// 	for i:=0;i<num_sats;i++{
// 		t_local[i] += LAG_TIME
// 	}

// 	// Prepare
// 	for j, _ := range array_all {
// 		var max_time int
// 		for i, _ := range array_all {
// 			if i != j && i != primary{
// 				sat_data_temp = sat_data_big[j][i]
// 				conn_time = find_next_conn(t_local[i], sat_data_temp, DIS)
// 				if conn_time == -1 {
// 					return false, 0.0
// 				}
// 				if max_time < conn_time {
// 					max_time = conn_time
// 				}
// 			}	
// 		}
// 		t_local[j] = max_time
// 	}

// 	// Commit
// 	for j, _ := range array_all {
// 		var max_time int
// 		for i, _ := range array_all {
// 			if i != j {
// 				sat_data_temp = sat_data_big[j][i]
// 				conn_time = find_next_conn(t_local[i], sat_data_temp, DIS)
// 				if conn_time == -1 {
// 					return false, 0.0
// 				}
// 				if max_time < conn_time {
// 					max_time = conn_time
// 				}
// 			}	
// 		}
// 		t_local[j] = max_time
// 	}

// 	// Reply
// 	for _, _ = range array_primary {
// 		var max_time int
// 		for i, _ := range array_all {
// 			if i != primary {
// 				sat_data_temp = sat_data_big[i][primary]
// 				conn_time = find_next_conn(t_local[i], sat_data_temp, DIS)
// 				if conn_time == -1 {
// 					return false, 0.0
// 				}
// 				if max_time < conn_time {
// 					max_time = conn_time
// 				}
// 			}	
// 		}
// 		// fmt.Println("Success")
// 		return true, float64(max_time)
// 	}

// 	// If it gets this far error has occurred

// 	return false, 0.0
// }


// // func find_next_conn(t_0 int, sat_data []float64, DIS float64) int {
// // 	for t:=t_0;t<len(sat_data);t++{
// // 		if sat_data[t] <= DIS {
// // 			return t
// // 		}
// // 	}
// // 	return -1
// // }

// func find_next_conn(t_0 int, sat_data []float64, DIS float64) int {
// 	var fprime float64
// 	t := t_0
// 	for t<len(sat_data) {
// 		if sat_data[t] <= DIS {
// 			for sat_data[t] <= DIS {
// 				if t > 0 {
// 					t -= 1
// 				} else {
// 					return 0
// 				}
// 			}
// 			return t+1
// 		} else if t > 0 {
// 			fprime = sat_data[t]-sat_data[t-1]
// 			if fprime < 0 {
// 				t -= int((sat_data[t]-DIS)/fprime)	// Newton raphson
// 			}
// 		}
// 		t += 1 
// 	}
// 	return -1
// }


// func read_data_string(file_name string) (out_data []float64) {
// 	// Open the CSV file
// 	file, err := os.Open(file_name)
// 	if err != nil {
// 		fmt.Println("FILE NOT OPENING, MAY NOT EXIST")
// 	}
// 	defer file.Close()
// 	// Read the CSV data
// 	reader := csv.NewReader(file)
// 	reader.FieldsPerRecord = -1 // Allow variable number of fields
// 	data, _ := reader.ReadAll()
// 	for _, item := range data[0] {
// 		out_data = append(out_data, atoi(item))
// 	}
// 	return out_data
// }

// func atoi(in string) float64 {
// 	value, _ := strconv.ParseFloat(in, 64)
// 	return value
// }


// func check_input(bin_li []int) bool {
// 	// If input array is not long enough error
// 	if len(bin_li) < 4 {
// 		return true
// 	}
// 	// If bin_li is not unique
// 	for i:=0;i<len(bin_li);i++{
// 		for j:=0;j<len(bin_li);j++{
// 			if i != j {
// 				if bin_li[i]==bin_li[j]{
// 					return true
// 				}
// 			}
// 		}
// 	}
// 	// If passes checks
// 	return false
// }
