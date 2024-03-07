package main

import (
	"encoding/csv"
	"log"
	"os"
)

func writeFile2D(data_2d [][]string, file_name string) {
	// Save data to csv
	file, _ := os.Create(file_name)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
	// w.Write(data_1d)
	w.WriteAll(data_2d)
}

func writeFile1D(data_1d []string, file_name string) {
	// Save data to csv
	file, _ := os.Create(file_name)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
	w.Write(data_1d)
	// w.WriteAll(data_2d)
}

func check(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
