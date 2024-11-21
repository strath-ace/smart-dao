// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"

	//    "math"
	"github.com/schollz/progressbar/v3"
)

const DIR_NAME = "data_test"

func main() {

	// ################# Load bin_li from python

	// MUST BE IN DECENDING ORDER
	DIS := 500.0

	// ################# Load specific sat files

	// Generate real file names
	file_sats, _ := os.ReadDir(DIR_NAME + "/real_sats")
	fmt.Println(file_sats)
	var sat_data [][][]float64
	fmt.Println("Loading Real Sats")
	bar := progressbar.Default(int64(len(file_sats)))
	for i, sat := range file_sats {
		sat_data = append(sat_data, read_data_string(DIR_NAME+"/real_sats/"+sat.Name()))
		if i%100 == 0 {
			bar.Add(100)
		}
	}
	fmt.Println(" ")

	// Generate simulated file names
	sim_sats, _ := os.ReadDir(DIR_NAME + "/sim_sats")
	fmt.Println(sim_sats)

	fmt.Println("Files loaded, starting calculations")

	// ################# Run consensus

	var c_li []int
	var sat1 [][]float64
	bar = progressbar.Default(int64(len(sim_sats)))
	for i := 0; i < len(sim_sats); i++ {
		sat1 = read_data_string(DIR_NAME + "/sim_sats/" + strconv.Itoa(i) + ".csv")
		var c int
		for _, sat2 := range sat_data {
			conn_return := find_next_conn(sat1, sat2, DIS)
			c += conn_return
		}
		c_li = append(c_li, c)
		if i%100 == 0 && i != 0 {
			bar.Add(100)
		}
		if i%1000 == 0 && i != 0 {
			save_data(c_li, DIR_NAME+"/all_combs.csv")
		}
	}
	// Save data to file
	save_data(c_li, DIR_NAME+"/all_combs.csv")
}

func save_data(out_data []int, file_name string) {
	file, _ := os.Create(file_name)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
	for i := 0; i < len(out_data); i++ {
		w.Write([]string{strconv.Itoa(out_data[i])})
	}
}

func find_next_conn(sat1 [][]float64, sat2 [][]float64, DIS_li float64) int {
	squ := DIS_li * DIS_li
	var x float64
	var y float64
	var z float64
	for t := 0; t < len(sat1); t++ {
		x = sat1[t][0] - sat2[t][0]
		y = sat1[t][1] - sat2[t][1]
		z = sat1[t][2] - sat2[t][2]
		tot := ((x * x) + (y * y) + (z * z))
		if tot <= squ {
			return 1
		} else if tot > 97200000 {
			t += 5
		}
		// } else if tot > 162358564 {
		// 	t += 6 // If on other side of the planet skip 6minutes to calc next (8kms)
		// }
	}
	return 0
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
