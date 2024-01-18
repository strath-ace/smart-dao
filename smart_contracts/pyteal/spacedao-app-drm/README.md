# spacedao-app-drm



## Install and Setup

This assumes that you have the algorand sandbox and docker setup and running.

First clone the repository.

Next create the virtual library environment by navigating to the base folder of the clone of this repository and entering the following:
```
pipenv shell
```
To exit this when done use:
```
exit
```

Check that the localhost that you are connecting to in main.py is the same as the algorand sandbox.

Next start the FastAPI interface with:
```
uvicorn main:app --reload
```
and navigate to (fill in) in your browser.
