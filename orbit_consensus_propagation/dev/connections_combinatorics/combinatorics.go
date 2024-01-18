package main

import (
   "encoding/csv"
   "os"
   "fmt"
   "strconv"
   "io/ioutil"
)

const DIR_NAME = "data_icsmd"

func main() {

	// ################# Load bin_li from python

	// MUST BE IN DECENDING ORDER
	DIS_li := []float64{1000, 500, 100, 50, 10}

	// ################# Load specific sat files
	
	file_sats, _ := ioutil.ReadDir(DIR_NAME+"/big")

	fmt.Println("Loading", len(file_sats), "files")

	// Generate file names
	var sat_data [][][]float64
	for i, sat := range file_sats {
		sat_data = append(sat_data, read_data_string(DIR_NAME+"/big/"+sat.Name()))
		if i % 1000 == 0 {
			fmt.Println((100*i)/len(file_sats), "% loaded")
		}
	}

	fmt.Println("Files loaded, starting calculations")
	
	// ################# Run consensus

	var c_li [][]int
	for i, sat1 := range sat_data {
		var c []int
		for j:=0;j<len(DIS_li);j++{
			c = append(c, 0)
		}
		for j, sat2 := range sat_data {
			if i != j {
				conn_return := find_next_conn(sat1, sat2, DIS_li)
				for k, conn := range conn_return {
					c[k] += conn
				}
			}	
		}
		c_li = append(c_li, c)
		fmt.Println("Sat", i)
		if i % 1000 == 0 && i != 0 {
			save_data(c_li, DIR_NAME+"/all_combs.csv", len(DIS_li))
		}
	}
	// Save data to file
	save_data(c_li, DIR_NAME+"/all_combs.csv", len(DIS_li))
}

func save_data(out_data [][]int, file_name string, num_dis int) {
	file, _ := os.Create(file_name)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
	for i:=0;i<len(out_data);i++{
		var temp []string
		for j:=0;j<num_dis;j++{
			temp = append(temp, strconv.Itoa(out_data[i][j]))
		}
		w.Write(temp)
	}
}


func find_next_conn(sat1 [][]float64, sat2 [][]float64, DIS_li []float64) []int {
	var DIS_c []int
	for i:=0;i<len(DIS_li);i++{
		DIS_c = append(DIS_c, 0)
	}
	finish := true
	c := 0
	for t:=0;t<len(sat1)&&finish;t++{
		x := sat1[t][0]-sat2[t][0]
		y := sat1[t][1]-sat2[t][1]
		z := sat1[t][2]-sat2[t][2]
		tot := ((x*x)+(y*y)+(z*z))
		for i:=c;i<len(DIS_li);i++{
			if tot <= DIS_li[i]*DIS_li[i] {
				DIS_c[i] = 1
				c+=1
			} else {
				break
			}
			if i == len(DIS_li)-1 {
				finish = false
			}
		}
		// for i, DIS := range DIS_li {
		// 	if tot <= DIS*DIS {
		// 		DIS_c[i] = 1
		// 	} else {
		// 		break
		// 	}
		// 	if i == len(DIS_li)-1 {
		// 		finish = false
		// 	}
		// }
	}
	return DIS_c
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