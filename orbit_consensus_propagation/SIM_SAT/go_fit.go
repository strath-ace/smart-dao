// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

/*
#include <stdlib.h>  // For malloc and free
*/
import (
	"C"
)
import (
	"math"
	"unsafe"
)

func main() {}

func convert_to_n_by_rest(grid []float64, n_div int) [][]int {

	var depth int
	// // Calculate the number of rows (n) based on the length of the flat grid
	depth = int(math.Ceil(float64(len(grid)) / float64(n_div)))

	// Create the 2D slice
	result := make([][]int, depth)

	// Fill the 2D slice
	for i := 0; i < depth; i++ {
		// Determine the starting and ending index for the row
		start := i * n_div
		end := start + n_div
		if end > len(grid) {
			end = len(grid) // Handle the case where we exceed the grid length
		}
		// Slice the grid and append to result
		result[i] = make([]int, end-start)
		// Convert float64 to int and fill the inner slice
		for j := start; j < end; j++ {
			result[i][j-start] = int(grid[j]) // Convert and assign
		}
	}

	return result
}

func convert_to_n_by_n_by_rest(grid []float64, n int) [][][]float64 {

	var depth int
	var i, j, k int

	depth = len(grid) / (n * n)

	// Create a 3D slice with dimensions [cols][rows][depth]
	var temp []float64
	var temp2 [][]float64
	var result [][][]float64

	for i = 0; i < n; i++ {
		temp2 = [][]float64{}
		for j = 0; j < n; j++ {
			temp = []float64{}
			for k = 0; k < depth; k++ {
				temp = append(temp, grid[k+(i*n*depth)+(j*depth)])
			}
			temp2 = append(temp2, temp)
		}
		result = append(result, temp2)
	}

	return result
}

type YourStructure struct {
	c  C.int
	c2 C.int
}

func consensus(comm [][][]int, ec []int, grid [][][]float64, num_participants int) (bool, int) {
	var i int
	var j int
	var c int
	var c2 int
	var t int
	var found bool
	var final_time int
	var t_local []float64
	var t_local_next []float64
	for i = 0; i < num_participants; i++ {
		t_local = append(t_local, 0.0)
		t_local_next = append(t_local_next, 0.0)
	}
	for c = 0; c < len(comm); c++ {
		copy(t_local_next, t_local)
		for c2 = 0; c2 < len(comm[c]); c2++ {
			found = false
			i = comm[c][c2][0]
			j = comm[c][c2][1]

			for t = 0; t < len(grid[ec[i]][ec[j]]); t++ {

				if grid[ec[i]][ec[j]][t] >= t_local[i] {
					found = true
					if grid[ec[i]][ec[j]][t] > t_local_next[j] {
						t_local_next[j] = grid[ec[i]][ec[j]][t]
					}
					break
				} else if grid[ec[i]][ec[j]][t] == -1 {
					break
				}
			}
			if !found {
				return false, -1
			}
		}
		copy(t_local, t_local_next)
		// fmt.Println(t_local)
	}
	final_time = 0
	for t = 0; t < num_participants; t++ {
		if final_time < int(t_local[t]) {
			final_time = int(t_local[t])
		}
	}
	return true, final_time
}

func get_comm(num_participants int) [][][][]int {
	var comm [][][][]int
	var temp [][][]int
	var temp1 [][]int
	var temp2 [][]int
	var temp3 [][]int
	var temp4 [][]int

	for i := 0; i < num_participants; i++ {
		temp = [][][]int{}

		temp1 = [][]int{}
		for j := 0; j < num_participants; j++ {
			if i != j {
				temp1 = append(temp1, []int{i, j})
			}
		}
		temp = append(temp, temp1)

		temp2 = [][]int{}
		for j := 0; j < num_participants; j++ {
			if i != j {
				for k := 0; k < num_participants; k++ {
					if j != k {
						temp2 = append(temp2, []int{j, k})
					}
				}
			}
		}
		temp = append(temp, temp2)

		temp3 = [][]int{}
		for j := 0; j < num_participants; j++ {
			for k := 0; k < num_participants; k++ {
				if j != k {
					temp3 = append(temp3, []int{j, k})
				}
			}
		}
		temp = append(temp, temp3)

		temp4 = [][]int{}
		for j := 0; j < num_participants; j++ {
			if i != j {
				temp4 = append(temp4, []int{j, i})
			}
		}
		temp = append(temp, temp4)

		comm = append(comm, temp)
	}

	return comm
}

//export consensus_completeness_per
func consensus_completeness_per(combs_raw *float64, combs_n int64, grid_raw *float64, grid_n int64, num_sats int64, num_participants int64, output_size *C.int) *C.int {

	var grid_flat []float64
	var combs_flat []float64

	// var combs [][]float64
	var grid [][][]float64

	var comm [][][][]int
	var ec [][]int

	var completed bool
	var timer int

	var i int
	var j int
	var c int
	var timer_all int

	combs_flat = unsafe.Slice(combs_raw, combs_n)

	grid_flat = unsafe.Slice(grid_raw, grid_n)

	ec = convert_to_n_by_rest(combs_flat, int(num_participants))

	grid = convert_to_n_by_n_by_rest(grid_flat, int(num_sats))

	comm = get_comm(int(num_participants))

	var k int
	var kk int
	var uni []int32
	var already bool

	c = 0
	timer_all = 0

	for j = 0; j < len(comm); j++ {
		for i = 0; i < len(ec); i++ {
			completed, timer = consensus(comm[j], ec[i], grid, int(num_participants))
			if completed {
				c += 1
				timer_all += timer

				for kk = 0; kk < len(ec[i]); kk++ {
					already = false
					for k = 0; k < len(uni); k++ {
						if ec[i][kk] == int(uni[k]) {
							already = true
						}
					}
					if !already {
						uni = append(uni, int32(ec[i][kk]))
					}
				}

			}
		}
	}

	*output_size = C.int(len(uni))
	// fmt.Println(uni)
	ptr := C.malloc(C.size_t(len(uni)) * C.size_t(unsafe.Sizeof(uni[0])))

	// Cast the allocated memory to a Go slice
	cArray := (*[1<<30 - 1]int32)(ptr)[:len(uni):len(uni)]

	// Copy Go numbers to the C-allocated memory
	copy(cArray, uni)

	// Return pointer to the C-allocated memory
	return (*C.int)(unsafe.Pointer(ptr))

}
