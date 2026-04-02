#!/bin/bash

# Daily integration script for the Banking System.
#
# This script:
# 1. Runs the frontend once for each seassion input file for a given day.
# 2. Writes a separate 'bank account transaction' file for each session.
# 3. Concatenates the session 'bank account transaction' files into a 
#    single 'merged bank account transactions' file.
# 4. Runs the backend using the 'merged bank account transactions' file.

set -e
shopt -s nullglob

# Determine the repository root based on the script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Root folders
FRONTEND_SRC="$REPO_ROOT/frontend/src"
FRONTEND_INPUTS="$REPO_ROOT/frontend/inputs"
FRONTEND_OUTPUTS="$REPO_ROOT/frontend/outputs"

BACKEND_SRC="$REPO_ROOT/backend/src"
BACKEND_INPUTS="$REPO_ROOT/backend/inputs"
BACKEND_OUTPUTS="$REPO_ROOT/backend/outputs"

DAY_SESSION_INPUTS="$REPO_ROOT/frontend/inputs/daily_session_inputs/day_1_session_inputs"

# Files used by the script
CURRENT_BANK_ACCOUNTS_FILE="$FRONTEND_INPUTS/current_bank_accounts.txt"
MASTER_BANK_ACCOUNTS_FILE="$BACKEND_INPUTS/master_bank_accounts.txt"
MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE="$BACKEND_INPUTS/merged_bank_account_transactions.txt"

NEW_MASTER_BANK_ACCOUNTS_FILE="$BACKEND_OUTPUTS/new_master_bank_accounts.txt"
NEW_CURRENT_BANK_ACCOUNTS_FILE="$BACKEND_OUTPUTS/current_bank_accounts.txt"

# Remove old frontend session output files
rm -f "$FRONTEND_OUTPUTS"/daily_session_outputs/session_*.txt
rm -f "$FRONTEND_OUTPUTS"/daily_session_outputs/session_*.out

# Remove old output files for the current daily run
rm -f "$MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE"
rm -f "$NEW_MASTER_BANK_ACCOUNTS_FILE"
rm -f "$NEW_CURRENT_BANK_ACCOUNTS_FILE"

session_files=("$DAY_SESSION_INPUTS"/*.input)

if [ ${#session_files[@]} -eq 0 ]; then
    echo "ERROR: No session input files found in '$DAY_SESSION_INPUTS'."
    exit 1
fi

echo "Running frontend session input files from '$DAY_SESSION_INPUTS'..."

session_number=1

for session_input in "${session_files[@]}"
do
    echo "Running session $session_number using '$(basename "$session_input")' file..."

    (
        cd "$FRONTEND_SRC"
        python banking_system_frontend.py \
            "$CURRENT_BANK_ACCOUNTS_FILE" \
            "$FRONTEND_OUTPUTS/daily_session_outputs/session_${session_number}.txt" \
            < "$session_input" \
            > "$FRONTEND_OUTPUTS/daily_session_outputs/session_${session_number}.out"
    )

    session_number=$((session_number + 1))
done

echo "Merging daily 'bank account transaction' files..."
cat "$FRONTEND_OUTPUTS"/daily_session_outputs/session_*.txt > "$MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE"
echo "Running backend using the 'merged bank account transaction' file..."

(
    cd "$BACKEND_SRC"
    python banking_system_backend.py \
        "$MASTER_BANK_ACCOUNTS_FILE" \
        "$MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE" \
        "$NEW_MASTER_BANK_ACCOUNTS_FILE" \
        "$NEW_CURRENT_BANK_ACCOUNTS_FILE"
)

echo "Daily run completed."
echo "Output files:"
echo "- $MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE"
echo "- $NEW_MASTER_BANK_ACCOUNTS_FILE"
echo "- $NEW_CURRENT_BANK_ACCOUNTS_FILE"
