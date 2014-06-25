#!/bin/bash
for F in $(ls $1);
do
  ./flatten.py "$1/$F" "$2/$F"
done

