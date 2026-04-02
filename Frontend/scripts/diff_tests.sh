#!/bin/bash

# Directory configuration
EXPECTED="expected_outputs"
ACTUAL="outputs/test_case_outputs"

# Compare test files
for expected_file in "$EXPECTED"/*
do
    filename=$(basename "$expected_file")

    if diff "$expected_file" "$ACTUAL/$filename" > /dev/null
    then
        echo "$filename: PASS"
    else
        echo "$filename: FAIL"
        echo "Differences:"
        diff "$expected_file" "$ACTUAL/$filename"
    fi
done

echo "Test comparison complete."
