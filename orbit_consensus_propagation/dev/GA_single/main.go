package main

import (
   "encoding/csv"
   "os"
   "fmt"
   "strconv"
   "math/rand"
   "os/exec"
)


const NUM_GENES = 4		// Even numbers work more evenly
const MAX_GENE = 81
const POP_SIZE = 100
const ITERATIONS = 100
const PAR_RATIO = 0.4	// Ratio of sorted population to use as parents for next pop
const ELITISM = 0.1

const SAVE_FILE = "data/ga_results.csv"

const STEP_SIZE = 60

const START_TIME = 1701448313
const DIS = 500

const LAG_TIME = 30*60



func fitness(genetics []int) (summer float64) {
	summer = consensus_time(genetics)
	return -summer
}

func initial_pop() (pop [][]int) {
	for j:=0;j<POP_SIZE;j++{
		var genetics []int
		for i:=0;i<NUM_GENES;i++{
			genetics = append(genetics, rand.Intn(MAX_GENE+1))
		}
		pop = append(pop, genetics)
	}
	return pop
}

func get_fit(pop [][]int) (fit_res []float64) {
	for i:=0;i<POP_SIZE;i++{
		fit_res = append(fit_res, fitness(pop[i]))
	}
	return fit_res
}

func sort_pop(pop [][]int, fit_res []float64) ([][]int) {
	n := POP_SIZE
	for i := 0; i < n-1; i++ {
		for j := 0; j < n-i-1; j++ {
			if fit_res[j] < fit_res[j+1] {
				fit_res[j], fit_res[j+1] = fit_res[j+1], fit_res[j]
				pop[j], pop[j+1] = pop[j+1], pop[j]
			}
		}
	}
	return pop
}

func mate(genes1, genes2 []int) (child_genes []int) {
	for i:=0;i<NUM_GENES;i++{
		prob := rand.Intn(100)
		if prob < 45 {
			child_genes = append(child_genes, genes1[i])
		} else if prob < 90 {
			child_genes = append(child_genes, genes2[i])
		} else {
			child_genes = append(child_genes, rand.Intn(MAX_GENE+1))
		}
	}
	return child_genes
}



func main() {
	fmt.Println("Start")

	// Generate initial population
	pop := initial_pop()
	// Get initial fitness
	fit_res := get_fit(pop)

	// Set initial top results
	min_res := fit_res[0]
	best_pop := pop[0]

	var pop_timeline [][]int
	var fit_timeline []float64
	
	for i:=0;i<ITERATIONS;i++{
		// Selection
		sorted_pop := sort_pop(pop, fit_res)		

		// Elitism
		var new_pop [][]int
		new_pop = append(new_pop, sorted_pop[:(POP_SIZE*ELITISM)]...)

		// Crossover
		for i:=0;i<POP_SIZE*(1-ELITISM);i++{
			parent1 := sorted_pop[POP_SIZE*(1-PAR_RATIO)+rand.Intn(POP_SIZE*PAR_RATIO)]
			parent2 := sorted_pop[POP_SIZE*(1-PAR_RATIO)+rand.Intn(POP_SIZE*PAR_RATIO)]
			new_pop = append(new_pop, mate(parent1, parent2))
		}

		// Calculate fitness
		pop = new_pop
		fit_res = get_fit(pop)

		// Display results for this population
		fmt.Println("Iteration:", i, "| Best pop:", pop[0], "| Fitness:", -fit_res[0]*STEP_SIZE/(60*60), "hours")
		if fit_res[0] > min_res {
			best_pop = pop[0]
			min_res = fit_res[0]
		}
		pop_timeline = append(pop_timeline, pop[0])
		fit_timeline = append(fit_timeline, -fit_res[0]*STEP_SIZE/(60*60))
	}

	save_timelines(pop_timeline, fit_timeline)

	fmt.Println("DONE")
	fmt.Println("-------------------")
	fmt.Println("Best pop:", best_pop, "| Fitness:", -min_res*STEP_SIZE/(60*60), "hours")
	fmt.Println("-------------------")

	// Call plot script
	_ = exec.Command("python", "plot_ga.py")
}


func save_timelines(pop_timeline [][]int, fit_timeline []float64) {
	file, _ := os.Create(SAVE_FILE)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
	for i:=0;i<len(pop_timeline);i++{
		var temp []string
		temp = append(temp,  fmt.Sprintf("%f",fit_timeline[i]))
		for j:=0;j<len(pop_timeline[i]);j++{
			temp = append(temp, strconv.Itoa(pop_timeline[i][j]))
		}
		w.Write(temp)
	}
}













func consensus_time(bin_li []int) float64 {

	// ################# Load bin_li from python

	num_sats := len(bin_li)

	// ################# Check input is okay

	if check_input(bin_li) {
		// fmt.Println("BAD INPUT EXITING")
		return float64(10000000)
	}

	// ################# Load specific sat files
	
	// Generate file names
	var file_sats []string
	for i:=0;i<num_sats;i++{
		file_sats = append(file_sats, strconv.Itoa(bin_li[i])+".csv")
	}
	// Get sat_data for sats in bin_li
	var sat_data [][][]float64
	for _, file := range file_sats {
		sat_data = append(sat_data, read_data_string("data/big/"+file))
	}
	
	// ################# Run consensus

	primary := 0
	var t_local []int

	// Get each array required
	array_primary := [][][]float64{sat_data[primary]}
	array_all := sat_data
	array_red := sat_data
	newLength := 0
	for index, _ := range array_red {
		// Remove other element
		if primary != index {
			array_red[newLength] = array_red[index]
			newLength++
		}
		// Set time
		t_local = append(t_local, 0)
	}
	array_red = array_red[:newLength]

	// Pre-prepare
	for _, sat1 := range array_primary {
		for j, sat2 := range array_all {
			if primary != j {
				conn_time := find_next_conn(0, sat1, sat2)
				if conn_time == -1 {
					return float64(10000000)
				}
				t_local[j] = conn_time
			}	
		}
	}

	// Decision Lag
	for i:=0;i<num_sats;i++{
		t_local[i] += LAG_TIME
	}

	// Prepare
	for j, sat2 := range array_all {
		var max_time int
		for i, sat1 := range array_all {
			if i != j && i != primary{
				conn_time := find_next_conn(t_local[i], sat1, sat2)
				if conn_time == -1 {
					return float64(10000000*0.75)
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}

	// Commit
	for j, sat2 := range array_all {
		var max_time int
		for i, sat1 := range array_all {
			if i != j {
				conn_time := find_next_conn(t_local[i], sat1, sat2)
				if conn_time == -1 {
					return  float64(10000000*0.5)
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		t_local[j] = max_time
	}

	// Reply
	for _, sat2 := range array_primary {
		var max_time int
		for i, sat1 := range array_all {
			if i != primary {
				conn_time := find_next_conn(t_local[i], sat1, sat2)
				if conn_time == -1 {
					return  float64(10000000*0.25)
				}
				if max_time < conn_time {
					max_time = conn_time
				}
			}	
		}
		// fmt.Println("Success")
		return float64(max_time)
	}

	// If it gets this far error has occurred

	return float64(100000000)
}


func find_next_conn(t_0 int, sat1 [][]float64, sat2 [][]float64) int {
	for t:=t_0;t<len(sat1);t++{
		x := sat1[t][0]-sat2[t][0]
		y := sat1[t][1]-sat2[t][1]
		z := sat1[t][2]-sat2[t][2]
		if (x*x+y*y+z*z) <= DIS*DIS {
			return t
		}
	}
	return -1
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