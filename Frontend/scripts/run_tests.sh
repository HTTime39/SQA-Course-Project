#!/bin/bash
shopt -s nullglob

INPUT_DIR="inputs"
OUTPUT_DIR="outputs"
SRC_DIR="src"
ACCOUNTS_FILE="$INPUT_DIR/current_bank_accounts.txt"
TRANSACTION_FILE="$OUTPUT_DIR/bank_account_transactions.txt"

# Clean 'outputs' folder
rm -f "$OUTPUT_DIR"/*

mkdir -p "$OUTPUT_DIR"

for input_file in "$INPUT_DIR"/*.input
do
    test_name=$(basename "$input_file" .input)

    echo "Running $test_name"

    python "$SRC_DIR/banking_system.py" \
        "$ACCOUNTS_FILE" \
        < "$input_file" \
        > "$OUTPUT_DIR/$test_name.output"

    # Save per-test transaction record
    if [[ -f "$TRANSACTION_FILE" ]]; then
        mv "$TRANSACTION_FILE" "$OUTPUT_DIR/$test_name.record"
    fi
done