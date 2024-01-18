#! /bin/sh

# This file is for development activation of app

# This batch file:
# Creates the python virtual environment
# Installs the required libraries
# Launches the app front end

script_path=$( realpath "$0"  )
app_path=$( dirname "$script_path"  )

(cd $app_path; Pipenv install)

(xdg-open http://127.0.0.1:8000/docs)
(start http://127.0.0.1:8000/docs)
(open http://127.0.0.1:8000/docs)

(cd $app_path; Pipenv run uvicorn main:app --reload)