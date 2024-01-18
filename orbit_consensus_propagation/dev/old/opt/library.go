package main

import (
   "C"
   "encoding/json"
   "encoding/csv"
   "os"
   "fmt"
   "strconv"
)

const START_TIME = 1701448313
const DIS = 500

const LAG_TIME = 30*60


//export consensus_time
func consensus_time(documentPtr *C.char) C.int {

	// ################# Load bin_li from python

	documentString := C.GoString(documentPtr)
	var jsonDocument map[string][]int
	_ = json.Unmarshal([]byte(documentString), &jsonDocument)
	bin_li := jsonDocument["ids"]

	num_sats := len(bin_li)

	// ################# Check input is okay

	if check_input(bin_li) {
		// fmt.Println("BAD INPUT EXITING")
		return C.int(-1)
	}

	// ################# Load specific sat files
	
	// Generate file names
	var file_sats []string
	for i:=0;i<num_sats;i++{
		file_sats = append(file_sats, strconv.Itoa(bin_li[i])+".csv")
	}
	// Get sat_data for sats in bin_li
	var sat_data [][][]float64
	for _, file := range file_sats {
		sat_data = append(sat_data, read_data_string("data/big/"+file))
	}
	
	// ################# Run consensus

	primary := 0
	var t_local []int

	// Get each array required
	array_primary := [][][]float64{sat_data[primary]}
	array_all := sat_data
	array_red := sat_data
	newLength := 0
	for index, _ := range array_red {
		// Remove other element
		if primary != index {
			array_red[newLength] = array_red[index]
			newLength++
		}
		// Set time
		t_local = append(t_local, 0)
	}
	array_red = array_red[:newLength]

	// Pre-prepare
	for _, sat1 := range array_primary {
		for j, sat2 := range array_all {
			if primary != j {
				conn_time := find_next_conn(0, sat1, sat2)
				if conn_time == -1 {
					return  C.int(10000000)
				}
				t_local[j] = conn_time
			}	
		}
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	// Prepare
	for j, sat2 := range array_all {
		var max_time int
		for i, sat1 := range array_all {
			if i != j && i != primary{
				conn_time := find_next_conn(t_local[i], sat1, sat2)
				if conn_time == -1 {
					return  C.int(10000000*0.75)
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}

	// Commit
	for j, sat2 := range array_all {
		var max_time int
		for i, sat1 := range array_all {
			if i != j {
				conn_time := find_next_conn(t_local[i], sat1, sat2)
				if conn_time == -1 {
					return  C.int(10000000*0.5)
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}

	// Reply
	for _, sat2 := range array_primary {
		var max_time int
		for i, sat1 := range array_all {
			if i != primary {
				conn_time := find_next_conn(t_local[i], sat1, sat2)
				if conn_time == -1 {
					return  C.int(10000000*0.25)
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		// fmt.Println("Success")
		return C.int(max_time)
	}

	// If it gets this far error has occurred

	return C.int(-1)
}


func find_next_conn(t_0 int, sat1 [][]float64, sat2 [][]float64) int {
	for t:=t_0;t<len(sat1);t++{
		x := sat1[t][0]-sat2[t][0]
		y := sat1[t][1]-sat2[t][1]
		z := sat1[t][2]-sat2[t][2]
		if (x*x+y*y+z*z) <= DIS*DIS {
			return t
		}
	}
	return -1
}


func read_data_string(file_name string) (out_data [][]float64) {
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
	for _, row := range data {
		out_data = append(out_data, []float64{atoi(row[0]), atoi(row[1]), atoi(row[2])})
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


func main() {}
