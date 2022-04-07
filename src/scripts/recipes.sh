#!/bin/bash

# perfrom recepies experiments
for i in {1..5}; 
do
    echo "**************************************" >> experiment_output.txt
done
echo "START RECEPIES 14_7 EXPERIMENTS" >> experiment_output.txt

for i in {1..5}; 
do 
    echo "**************************************" >> experiment_output.txt
    echo "Starting run $i" >> experiment_output.txt
    pypy3 main.py ./samples/recepies/14_7.json >> experiment_output.txt
    echo "**************************************" >> experiment_output.txt
done
######################################################################################
for i in {1..5}; 
do
    echo "**************************************" >> experiment_output.txt
done
echo "START RECIPES 14_7_UO EXPERIMENTS" >> experiment_output.txt

for i in {1..5}; 
do 
    echo "**************************************" >> experiment_output.txt
    echo "Starting run $i" >> experiment_output.txt
    pypy3 main.py ./samples/recepies/14_7_UO.json >> experiment_output.txt
    echo "**************************************" >> experiment_output.txt
done