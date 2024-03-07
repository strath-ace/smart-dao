package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/joshuaferrara/go-satellite"
	"github.com/schollz/progressbar/v3"
)

func generateRealSats() (sat_coords [][]Coord) {
	_, err := os.Stat("./TLE.txt")
	if errors.Is(err, os.ErrNotExist) {
		fmt.Println("Downloading current TLE data")
		out, _ := os.Create("TLE.txt")
		defer out.Close()
		resp, err := http.Get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")
		check(err)
		defer resp.Body.Close()
		io.Copy(out, resp.Body)
	} else {
		fmt.Println("TLE data already exists")
	}

	file, err := os.Open("TLE.txt")
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)

	var all_sats_tle []TLE
	var temp []string
	for scanner.Scan() {
		temp = append(temp, string(scanner.Text()))
		if len(temp) == 3 {
			all_sats_tle = append(all_sats_tle, TLE{temp[0], temp[1], temp[2]})
			temp = nil
		}
	}

	file, err = os.Open("chosen_sats.txt")
	if err != nil {
		log.Fatal(err)
	}
	scanner = bufio.NewScanner(file)
	var chosen_sats_names []string
	for scanner.Scan() {
		chosen_sats_names = append(chosen_sats_names, string(scanner.Text()))
	}
	// fmt.PrintS(all_sats)

	os.Mkdir("data", 0755)
	os.Mkdir("data/pos_real", 0755)

	start_t := time.Unix(START_TIME, 0)
	t := start_t
	var found_chosen bool
	// var temp []string
	var s satellite.Satellite
	bar := progressbar.Default(int64(len(all_sats_tle)))
	if APPLY_SUBSET {
		bar = progressbar.Default(int64(len(chosen_sats_names)))
	}
	var c int
	for j := 0; j < len(all_sats_tle); j++ {
		if APPLY_SUBSET {
			found_chosen = false
			for k := 0; k < len(chosen_sats_names); k++ {
				if chosen_sats_names[k] == strings.TrimSpace(all_sats_tle[j].name) {
					s = satellite.TLEToSat(
						all_sats_tle[j].l1,
						all_sats_tle[j].l2,
						"wgs84",
					)
					found_chosen = true
					c += 1
					break
				}
			}
		} else {
			found_chosen = true
			c += 1
		}
		if found_chosen {
			bar.Add(1)
			var all_pos [][]string
			var all_coords []Coord

			t = start_t
			for i := 0; i < ITERATIONS; i++ {
				pos, _ := satellite.Propagate(s, t.Year(), int(t.Month()), t.Day(), t.Hour(), t.Minute(), t.Second())
				t = t.Add(time.Second * 30)
				temp = nil
				temp = append(temp, fmt.Sprintf("%f", pos.X))
				temp = append(temp, fmt.Sprintf("%f", pos.Y))
				temp = append(temp, fmt.Sprintf("%f", pos.Z))

				all_pos = append(all_pos, temp)
				all_coords = append(all_coords, Coord{pos.X, pos.Y, pos.Z})
			}
			writeFile2D(all_pos, "./data/pos_real/"+strconv.Itoa(c)+".csv")
			sat_coords = append(sat_coords, all_coords)
		} else {
			bar.Add(1)
		}
	}
	return sat_coords
}
