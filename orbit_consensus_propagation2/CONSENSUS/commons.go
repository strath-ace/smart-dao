package main

import(
	"os"
	"fmt"
	"encoding/csv"
	"strconv"
	"gopkg.in/yaml.v2"
)

type Config struct {
	Start_time int `yaml:"START_TIME"`
	Big_data string `yaml:"BIG_DATA"`
	Lag_time int `yaml:"LAG_TIME"`
}

func load_config() (int, string, int) {
	f, err := os.Open("./config.yml")
	if err != nil {
		fmt.Println("ERROR:", err)
		fmt.Println("Config file may not exist, make sure you are in correct dir")
		fmt.Println("You should be calling this inside a directory that has a config.yml file")
	}
	defer f.Close()

	var cfg Config
	decoder := yaml.NewDecoder(f)
	_ = decoder.Decode(&cfg)
	return cfg.Start_time, "../DATA/"+cfg.Big_data+"/close_times/", cfg.Lag_time
}


func get_max(input_array []int) (max_val int) {
	max_val = 0
	for i:=0;i<len(input_array);i++{
		if max_val < input_array[i] {
			max_val = input_array[i]
		}
	}
	return max_val
}


func delete_element(slice []int, index int) []int {
	return append(slice[:index], slice[index+1:]...)
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
