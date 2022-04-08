#!/bin/bash

# perfrom recepies experiments
for i in {1..5}; 
do
    echo "**************************************" >> experiment_output.txt
done
echo "START STUDENTS EXPERIMENTS" >> experiment_output.txt

for i in {1..5}; 
do 
    echo "**************************************" >> experiment_output.txt
    echo "Starting run $i" >> experiment_output.txt
    pypy3 main.py ./samples/students_excel/job.json >> experiment_output.txt
    echo "**************************************" >> experiment_output.txt
done
