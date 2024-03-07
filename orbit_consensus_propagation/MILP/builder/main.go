package main

import (
	"fmt"
	"os"

	"github.com/schollz/progressbar/v3"
)

const ITERATIONS = 2880 // 3600 * 24
const APPLY_SUBSET = true
const START_TIME = 1709222233
const DIS_SQ = 500 * 500
const LAG_TIME = 0

type TLE struct {
	name string
	l1   string
	l2   string
}

type Coord struct {
	X float64
	Y float64
	Z float64
}

func main() {

	os.Mkdir("data", 0755)
	// os.Mkdir("data/interactions", 0755)

	var interactions [][][]bool

	fmt.Println("Creating real satellites")
	sat_coords_real := generateRealSats()
	fmt.Println("Generated", len(sat_coords_real), "real satellites")

	fmt.Println("Building Combinations")
	max_val := len(sat_coords_real)

	fmt.Println("Generating bulk of interactions")
	interactions = getInteractionsBinary(sat_coords_real)
	// fmt.Println(interactions[0][0])

	max_time := len(interactions[0][0])

	var temp []bool

	var stuff bool
	var stuff_li []bool
	var temp2 [][]bool
	var interactions2 [][][]bool

	var i, j, t1, t2, k int

	bar := progressbar.Default(int64(max_val * max_val))
	for i = 0; i < max_val; i++ {
		for j = 0; j < max_val; j++ {
			for t1 = 0; t1 < max_time; t1++ {
				for t2 = t1 + 1; t2 < max_time; t2++ {
					temp = interactions[i][j][t1:t2]
					stuff = false
					for k = 0; k < t2-t1; k++ {
						if temp[k] {
							stuff = true
							break
						}
					}
					stuff_li = append(stuff_li, stuff)
				}
			}
			temp2 = append(temp2, stuff_li)
			bar.Add(1)
		}
		interactions2 = append(interactions2, temp2)
	}
	fmt.Println(interactions2)
}
