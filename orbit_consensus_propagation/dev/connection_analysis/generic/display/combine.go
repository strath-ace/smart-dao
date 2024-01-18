package main

import (
   "C"
   "fmt"
//    "encoding/json"
//    "math"
   "strconv"
   "encoding/csv"
   "os"
   "io/ioutil"
)

const data_file = "../data2"
const csv_store string = data_file+"/all_conns/"
const graph_data_file = data_file+"/graph_data.csv"


//export combine
func combine(){
	fmt.Println("Start Combining Data")
	file_sats, _ := ioutil.ReadDir(csv_store)
	var unique_conns []string
	var total_conns []string
	for _, sat_file := range file_sats {
		unique_count := 0
		total_count := 0
		sat_conns := read_data_string(csv_store+sat_file.Name())
		for i:=0;i<len(sat_conns);i++{
			adder, _ := strconv.Atoi(sat_conns[i])
			total_count += adder
			if adder > 0 {
				unique_count += 1
			}
		}
		total_conns = append(total_conns, strconv.Itoa(total_count))
		unique_conns = append(unique_conns, strconv.Itoa(unique_count))
	}
	save_data(total_conns, unique_conns, graph_data_file)
}


func read_data_string(file_name string) (out_data []string) {
	// Open the CSV file
	file, _ := os.Open(file_name)
	defer file.Close()
	// Read the CSV data
	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1 // Allow variable number of fields
	data, _ := reader.ReadAll()
   out_data = data[:][0]
	return out_data
}


func save_data(out_data1, out_data2 []string, file_name string) {
	file, _ := os.Create(file_name)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
   	w.Write(out_data1[:])
	w.Write(out_data2[:])
}



func main(){

}