package satellite

import (
	"fmt"
)

func main () {
	line1 := "1 00900U 64063C   24007.86057439  .00000704  00000+0  72958-3 0  9997"
	line2 := "2 00900  90.1957  51.9974 0028313 107.6787 316.3828 13.74706637948860"
	sat1 := Satellite{Line1: line1, Line2: line2}
	fmt.Println(sat1)
	fmt.Println(Propagate(sat1, 2022, 10, 5, 4, 5, 4))
}