#! /bin/sh

# This file is for activating app

(cd sandbox; ./sandbox up)

echo "Sandbox On"

(cd apps/app-template; ./dev.sh)