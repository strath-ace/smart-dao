// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

package main

import (
   "encoding/csv"
   "os"
   "fmt"
   "strconv"
   "math/rand"
   "io/ioutil"
   "encoding/json"
//    "math"
	"github.com/schollz/progressbar/v3"
)

const START_TIME = 1705576078
const DATA_LOCATION = "../DATA/data_icsmd_1day"
const BIG_DATA = DATA_LOCATION+"/close_times"
const MAX_TIME = 86400

const SAVE_FILE = DATA_LOCATION+"/ga_0.csv"

func get_config() map[string][]float64 {
	jsonFile, err := os.Open("config.json")
    // if we os.Open returns an error then handle it
    if err != nil {
        fmt.Println(err)
    }
    // defer the closing of our jsonFile so that we can parse it later on
    defer jsonFile.Close()

    byteValue, _ := ioutil.ReadAll(jsonFile)

    var result map[string][]float64
    json.Unmarshal([]byte(byteValue), &result)
	return result
}


func fitness(genetics []int, LAG_TIME int) (float64) {
	check := consensus_time3(genetics, LAG_TIME)
	if check > 4 {
		return -float64(check-START_TIME)
	} else {
		return -MAX_TIME
	}
}

func initial_pop(num_genes int, POP_SIZE int, MAX_GENE int) (pop [][]int) {
	for j:=0;j<POP_SIZE;j++{
		var genetics []int
		for i:=0;i<num_genes;i++{
			genetics = append(genetics, rand.Intn(MAX_GENE+1))
		}
		pop = append(pop, genetics)
	}
	return pop
}

func get_fit(pop [][]int, LAG_TIME int) (fit_res []float64) {
	for i:=0;i<len(pop);i++{
		fit_res = append(fit_res, fitness(pop[i], LAG_TIME))
	}
	return fit_res
}

func sort_pop(pop [][]int, fit_res []float64) ([][]int) {
	n := len(pop)
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

func mate(genes1, genes2 []int, MAX_GENE int, RANDOMNESS float64) (child_genes []int) {
	for i:=0;i<len(genes1);i++{
		prob := float64(rand.Intn(100))
		if prob < 100*((1-RANDOMNESS)/2) {
			child_genes = append(child_genes, genes1[i])
		} else if prob < 100*((1-RANDOMNESS)) {
			child_genes = append(child_genes, genes2[i])
		} else {
			child_genes = append(child_genes, rand.Intn(MAX_GENE+1))
		}
	}
	return child_genes
}



func main() {

	var eval int
	eval = 0
	fmt.Println("-------------------")

	config_data := get_config()

	var MAX_GENE = int(config_data["MAX_GENE"][0])
	var RANDOMNESS = config_data["RANDOMNESS"][0]
	var POP_SIZE = int(config_data["POP_SIZE"][0])
	var ITERATIONS = int(config_data["ITERATIONS"][0])
	var PAR_RATIO = config_data["PAR_RATIO"][0]	// Ratio of sorted population to use as parents for next pop
	var ELITISM = config_data["ELITISM"][0]
	var ITERITER = int(config_data["ITERITER"][0])	// Number of times to reduce randomness (try different start genes)

	var GENE_LENGTHS = config_data["GENE_LENGTHS"]

	// Data for consensus fitness
	// var STEP_SIZE = config_data["STEP_SIZE"][0]   // Just for visual
	var LAG_TIME = int(config_data["LAG_TIME"][0])

	var best_pop_li [][]int
	var best_res_li []float64

	// var set bool

	for u:=0;u<len(GENE_LENGTHS);u++{

		num_genes := int(GENE_LENGTHS[u])
		pop := initial_pop(num_genes, POP_SIZE, MAX_GENE)
		fit_res := get_fit(pop, LAG_TIME)
		eval += len(pop)
		best_res := fit_res[0]
		best_best_pop := pop[0]
		
		for k:=0;k<ITERITER;k++{
			
			// Generate initial population
			pop := initial_pop(num_genes, POP_SIZE, MAX_GENE)
			// Get initial fitness
			fit_res := get_fit(pop, LAG_TIME)
			eval += len(pop)
			// Set initial top results
			min_res := fit_res[0]
			best_pop := pop[0]

			// Display
			fmt.Println("Genes:", num_genes, "(",u+1,"/", len(GENE_LENGTHS)+1, ")", "| Iteration:", k+1,"/",ITERITER)
			bar := progressbar.Default(int64(ITERATIONS))

			for i:=0;i<ITERATIONS;i++{

				// --- Dev code (If fitness is at max -> randomise pop)
				// set = false
				for i:=0;i<len(pop);i++{
					// for fit_res[i] == -1 {
					if -fit_res[i] == -MAX_TIME {
						var genetics []int
						for i:=0;i<num_genes;i++{
							genetics = append(genetics, rand.Intn(MAX_GENE+1))
						}
						pop[i] = genetics
						// set = true
						fit_res[i] = fitness(pop[i], LAG_TIME)
						eval += 1
					}
				}
				

				// Selection
				sorted_pop := sort_pop(pop, fit_res)

				// Elitism
				var new_pop [][]int
				new_pop = append(new_pop, sorted_pop[:int((float64(POP_SIZE)*ELITISM))]...)

				// Crossover
				for i:=0;i<int(float64(POP_SIZE)*(1-ELITISM));i++{
					parent1 := sorted_pop[int(float64(POP_SIZE)*(1-PAR_RATIO))+rand.Intn(int(float64(POP_SIZE)*PAR_RATIO))]
					parent2 := sorted_pop[int(float64(POP_SIZE)*(1-PAR_RATIO))+rand.Intn(int(float64(POP_SIZE)*PAR_RATIO))]
					new_pop = append(new_pop, mate(parent1, parent2, MAX_GENE, RANDOMNESS))
				}

				// Calculate fitness
				pop = new_pop
				fit_res = get_fit(pop, LAG_TIME)
				eval += len(pop)
				// If better overall fitness found
				if fit_res[0] > min_res && fit_res[0] != -1 {
					best_pop = pop[0]
					min_res = fit_res[0]
				}

				bar.Add(1)
				
			}
			fmt.Println("Best pop:", best_pop, "| Fitness:", -min_res, "seconds")
			fmt.Println("-------------------")

			if min_res > best_res {
				best_res = min_res
				best_best_pop = best_pop
			}
		}
		best_pop_li = append(best_pop_li, best_best_pop)
		best_res_li = append(best_res_li, best_res)
	}
	save_timelines(SAVE_FILE, GENE_LENGTHS, best_pop_li, best_res_li)
	fmt.Println("Evaluations: ",eval)
}


func save_timelines(SAVE_FILE string, gene_length []float64, pop_timeline [][]int, fit_timeline []float64) {
	file, _ := os.Create(SAVE_FILE)
	defer file.Close()
	w := csv.NewWriter(file)
	defer w.Flush()
	for i:=0;i<len(pop_timeline);i++{
		var temp []string
		temp = append(temp, strconv.Itoa(int(gene_length[i])))
		temp = append(temp,  fmt.Sprintf("%f",fit_timeline[i]))
		for j:=0;j<len(pop_timeline[i]);j++{
			temp = append(temp, strconv.Itoa(pop_timeline[i][j]))
		}
		w.Write(temp)
	}
}
