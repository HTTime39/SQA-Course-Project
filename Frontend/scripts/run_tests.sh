#!/bin/bash
shopt -s nullglob

# Directory configuration
INPUT_DIR="inputs/test_case_inputs"
OUTPUT_DIR="outputs/test_case_outputs"
SRC_DIR="src"
CURRENT_BANK_ACCOUNTS_FILE="inputs/current_bank_accounts.txt"
BANK_ACCOUNT_TRANSACTION_FILE="outputs/bank_account_transactions.txt"

# Clean output directory
rm -f "$OUTPUT_DIR"/*
mkdir -p "$OUTPUT_DIR"

# Run test cases
for input_file in "$INPUT_DIR"/*.input
do
    test_name=$(basename "$input_file" .input)

    echo "Running $test_name"

    # Run frontend with redirected input and capture output
    python "$SRC_DIR/banking_system_frontend.py" \
        "$CURRENT_BANK_ACCOUNTS_FILE" \
        < "$input_file" \
        > "$OUTPUT_DIR/$test_name.output"

    # Rename generated transaction record files
    if [[ -f "$BANK_ACCOUNT_TRANSACTION_FILE" ]]; then
        mv "$BANK_ACCOUNT_TRANSACTION_FILE" "$OUTPUT_DIR/$test_name.record"
    fi
done

echo "Test run complete."
