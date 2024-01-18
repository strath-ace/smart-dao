package main

import (
   "C"
   "encoding/json"
   "math"
   "strconv"
   "encoding/csv"
   "os"
   "io/ioutil"
)

const r_earth = 6371

const data_file = "../data2"
const csv_store string = data_file+"/all_conns/"


//export fromJSON
func fromJSON(documentPtr *C.char) {
   documentString := C.GoString(documentPtr)
   var jsonDocument map[string][][]float64
   _ = json.Unmarshal([]byte(documentString), &jsonDocument)
   delta_sat_coords := convert_pos_to_coords(jsonDocument["delta_sat_pos"])

   file_sats, _ := ioutil.ReadDir(csv_store)

   for i:=0;i<len(delta_sat_coords);i++{
      var connections []string
      for j:=0;j<len(delta_sat_coords);j++{
         if i != j {
            // If sat i and sat j are within 100km add 1 to csv of sat i at position j
            if get_norm_squared(delta_sat_coords[i], delta_sat_coords[j]) {
               if connections == nil {
                  connections = read_data_string(csv_store+file_sats[i].Name())
               }
               adder, _ := strconv.Atoi(connections[j])
               connections[j] = strconv.Itoa(adder + 1)
            }
         }
      }
      if connections != nil {
         save_data_string(connections, csv_store+file_sats[i].Name())
      }
   }  
}

func get_norm_squared(sat1, sat2 []float64) (bool) {
   x_diff := sat1[0]-sat2[0]
   y_diff := sat1[1]-sat2[1]
   z_diff := sat1[2]-sat2[2]
   if x_diff >= 100 || y_diff >= 100 || z_diff >= 100 {
      return false
   } else {
      return math.Sqrt(x_diff*x_diff + y_diff*y_diff + z_diff*z_diff) <= 100
   }  
}

func convert_pos_to_coords(delta_sat_pos[][]float64) (delta_sat_coords [][]float64) {
   for i:=0;i<len(delta_sat_pos);i++{
      x,y,z := position_to_coords(delta_sat_pos[i][0], delta_sat_pos[i][1], delta_sat_pos[i][2])
      var temp []float64
      temp = append(temp, x)
      temp = append(temp, y)
      temp = append(temp, z)
      delta_sat_coords = append(delta_sat_coords, temp)
   }
   return delta_sat_coords
}

func save_data_string(out_data []string, file_name string) {
	file, _ := os.Create(file_name)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
   w.Write(out_data[:])
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

func position_to_coords(lat, lon, elev float64) (x,y,z float64) {
	r := elev/1000 + r_earth;
	x = r*math.Cos(lat)*math.Cos(lon)
	y = r*math.Cos(lat)*math.Sin(lon)
	z = r*math.Sin(lat)
	return x,y,z
}


func main(){

}