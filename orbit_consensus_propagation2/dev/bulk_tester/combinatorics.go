package main

import (
   "encoding/csv"
   "os"
   "strconv"
	"C"
	"encoding/json"
)

const DIR_NAME = "data_icsmd"

func main() {}

//export combinations
func combinations(documentPtr *C.char) {

	// ################# Load bin_li from python

	// MUST BE IN DECENDING ORDER
	DIS := 1000.0
	// ################# Load specific sat files

	documentString := C.GoString(documentPtr)
	var jsonDocument map[string][][][]float64
	_ = json.Unmarshal([]byte(documentString), &jsonDocument)
	counter := jsonDocument["counter"]
	real_sats := jsonDocument["real"]
	sim_sats := jsonDocument["sim"]
	
	// fmt.Println(counter)
	// fmt.Println(real_sats)
	// fmt.Println(sim_sats)

	// fmt.Println("Files loaded, starting calculations")
	
	// ################# Run consensus

	var c_li []int
	// bar := progressbar.Default(int64(len(sim_sats)))
	for _, sat1 := range sim_sats {
		var c int
		for _, sat2 := range real_sats {
			conn_return := find_next_conn(sat1, sat2, DIS)
			c += conn_return
		}
		c_li = append(c_li, c)
		// bar.Add(1)
	}
	// Save data to file
	save_data(c_li, DIR_NAME+"/results/"+strconv.Itoa(int(counter[0][0][0]))+".csv")
}

func save_data(out_data []int, file_name string) {
	
	file, _ := os.Create(file_name)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
	for i:=0;i<len(out_data);i++{
		w.Write([]string{strconv.Itoa(out_data[i])})
	}
}


func find_next_conn(sat1 [][]float64, sat2 [][]float64, DIS_li float64) (int) {
	squ := DIS_li*DIS_li
	var x float64
	var y float64
	var z float64
	for t:=0;t<len(sat1);t++{
		x = sat1[t][0]-sat2[t][0]
		y = sat1[t][1]-sat2[t][1]
		z = sat1[t][2]-sat2[t][2]
		tot := ((x*x)+(y*y)+(z*z))
		if tot <= squ {
			return 1
		} else if tot > 97200000 {
			t += 5
		}
	}
	return 0
}