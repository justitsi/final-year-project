#!/bin/bash

# perfrom events experiments
for i in {1..5}; 
do
    echo "**************************************" >> experiment_output.txt
done
echo "START EVENTS 6_2 EXPERIMENTS" >> experiment_output.txt

for i in {1..5}; 
do 
    echo "**************************************" >> experiment_output.txt
    echo "Starting run $i" >> experiment_output.txt
    pypy3 main.py ./samples/events/6_2.json >> experiment_output.txt
    echo "**************************************" >> experiment_output.txt
done
######################################################################################
for i in {1..5}; 
do
    echo "**************************************" >> experiment_output.txt
done
echo "START EVENTS 10_3 EXPERIMENTS" >> experiment_output.txt

for i in {1..5}; 
do 
    echo "**************************************" >> experiment_output.txt
    echo "Starting run $i" >> experiment_output.txt
    pypy3 main.py ./samples/events/10_3.json >> experiment_output.txt
    echo "**************************************" >> experiment_output.txt
done
######################################################################################
for i in {1..5}; 
do
    echo "**************************************" >> experiment_output.txt
done
echo "START EVENTS 6_2_UO EXPERIMENTS" >> experiment_output.txt

for i in {1..5}; 
do 
    echo "**************************************" >> experiment_output.txt
    echo "Starting run $i" >> experiment_output.txt
    pypy3 main.py ./samples/events/6_2_UO.json >> experiment_output.txt
    echo "**************************************" >> experiment_output.txt
done
######################################################################################
for i in {1..5}; 
do
    echo "**************************************" >> experiment_output.txt
done
echo "START EVENTS 10_3_UO EXPERIMENTS" >> experiment_output.txt

for i in {1..5}; 
do 
    echo "**************************************" >> experiment_output.txt
    echo "Starting run $i" >> experiment_output.txt
    pypy3 main.py ./samples/events/10_3_UO.json >> experiment_output.txt
    echo "**************************************" >> experiment_output.txt
done