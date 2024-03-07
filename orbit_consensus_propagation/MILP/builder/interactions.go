package main

import (
	"math"
	"os"
	"strconv"

	"github.com/schollz/progressbar/v3"
)

func getInteractionsBinary(sat_coords [][]Coord) (interactions [][][]bool) {
	os.Mkdir("data", 0755)
	os.Mkdir("data/interactions", 0755)
	bar := progressbar.Default(int64(len(sat_coords) * len(sat_coords)))
	var i int
	var j int
	var t int
	shape_i := len(sat_coords)
	shape_t := len(sat_coords[0])
	var t_li []bool
	var temp [][]bool
	for i = 0; i < shape_i; i++ {
		temp = nil
		for j = 0; j < shape_i; j++ {
			t_li = nil
			if i != j {
				for t = 0; t < shape_t; t++ {
					if checkDistance(sat_coords[i][t], sat_coords[j][t]) {
						t_li = append(t_li, true)
					} else {
						t_li = append(t_li, false)
					}
				}
			} else {
				for t = 0; t < len(sat_coords[0]); t++ {
					t_li = append(t_li, false)
				}
			}
			temp = append(temp, t_li)
			bar.Add(1)
		}
		interactions = append(interactions, temp)
		// writeFile(temp)
	}
	return interactions
}

func getInteractionsSmall(sat_coords [][]Coord, sat_id int) (temp [][]bool) {
	// bar := progressbar.Default(int64(len(sat_coords) * len(sat_coords)))
	var j int
	var t int
	shape_i := len(sat_coords)
	shape_t := len(sat_coords[0])
	var t_li []bool
	temp = nil
	for j = 0; j < shape_i; j++ {
		t_li = nil
		if sat_id != j {
			for t = 0; t < shape_t; t++ {
				if checkDistance(sat_coords[sat_id][t], sat_coords[j][t]) {
					t_li = append(t_li, true)
				} else {
					t_li = append(t_li, false)
				}
			}
		} else {
			for t = 0; t < len(sat_coords[0]); t++ {
				t_li = append(t_li, false)
			}
		}
		temp = append(temp, t_li)
		// bar.Add(1)
	}
	return temp
}

func saveInteractions(sat_coords [][]Coord) {
	os.Mkdir("data", 0755)
	os.Mkdir("data/interactions", 0755)
	bar := progressbar.Default(int64(len(sat_coords) * len(sat_coords)))
	var i int
	var j int
	var t int
	shape_i := len(sat_coords)
	shape_t := len(sat_coords[0])
	var t_li []string
	var temp [][]string
	for i = 0; i < shape_i; i++ {
		temp = nil
		for j = 0; j < shape_i; j++ {
			t_li = nil
			if i != j {
				for t = 0; t < shape_t; t++ {
					if checkDistance(sat_coords[i][t], sat_coords[j][t]) {
						t_li = append(t_li, "1")
					} else {
						t_li = append(t_li, "0")
					}
				}
			} else {
				for t = 0; t < len(sat_coords[0]); t++ {
					t_li = append(t_li, "0")
				}
			}
			temp = append(temp, t_li)
			bar.Add(1)
		}
		// interactions = append(interactions, temp)
		writeFile2D(temp, "data/interactions/"+strconv.Itoa(i)+".csv")
	}
}

func checkDistance(sat1 Coord, sat2 Coord) bool {
	if math.Pow(sat1.X-sat2.X, 2)+math.Pow(sat1.Y-sat2.Y, 2)+math.Pow(sat1.Z-sat2.Z, 2) <= DIS_SQ {
		return true
	} else {
		return false
	}
}
