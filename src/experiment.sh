#!/bin/bash
rm experiment_output.txt
touch experiment_output.txt

./scripts/events.sh
./scripts/students.sh
./scripts/recipes.sh