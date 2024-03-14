#!/bin/bash
for nd in {16,32,64,128}; do
  for bs in {25,30,50}; do
    python project.py -d $nd -b $bs &
  done
done
