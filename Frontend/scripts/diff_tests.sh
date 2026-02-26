#!/bin/bash

EXPECTED="expected_outputs"
ACTUAL="outputs"

for expected_file in "$EXPECTED"/*
do
    filename=$(basename "$expected_file")

    if diff "$expected_file" "$ACTUAL/$filename" > /dev/null
    then
        echo "$filename: PASS"
    else
        echo "$filename: FAIL"
        diff "$expected_file" "$ACTUAL/$filename"
    fi
done