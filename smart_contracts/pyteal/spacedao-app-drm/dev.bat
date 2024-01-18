@ ECHO OFF

:: This file is for development activation of app

:: This batch file:
:: Activates the python virtual environment
:: Installs the required libraries
:: Launches the app front end

TITLE Activate App - Development

SET app_path=%~dp0

CD %app_path%

echo %cd%

Pipenv install

START http://127.0.0.1:8000/docs

Pipenv run uvicorn main:app --reload