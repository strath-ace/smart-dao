# Find minimum consensus time for maximised number of satellites

This is part of the **fault-tolerant decision making** in space project.

## Setup and run

Clone repository and then make sure you are in the cwd.

Build venv, enter venv and install requirements with:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Get Satellite Data

Go to (Celestrak Active Sats)[https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle] and save the page as `active.txt` in the cwd.

In `sats_to_use.txt` list all satellites that you want to run within the system exactly as they are written in `active.txt`. The current list contains all satellites used in the Internation Charter Space and Major Disasters.

Run `get_less_sats.py`:

```bash
python3 get_less_sats.py
```

### Execute GA

Within `run.py` parameters for the genetic algorithm can be set.

Run GA with:

```bash
python3 run.py
```

### Extra

Run on specific cores:

```bash
taskset --cpu-list 17-19 python3 run.py
```