#!/bin/bash

# Weekly integration script for the Banking System.
#
# This script runs the daily integration script seven times to simulate
# seven days of banking system operation.
#
# For each day:
# 1. A different set of frontend session input files is used.
# 2. The previous day's 'current bank accounts' file becomes the next day's
#    frontend input file.
# 3. The previous day's 'new master bank accounts' file becomes the next day's
#    backend 'master bank accounts' input file.

set -e

# Determine the repository root based on the script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DAILY_SCRIPT="$REPO_ROOT/scripts/daily_run.sh"

FRONTEND_INPUTS="$REPO_ROOT/frontend/inputs"
BACKEND_INPUTS="$REPO_ROOT/backend/inputs"
SYSTEM_OUTPUTS="$REPO_ROOT/system_outputs"

INITIAL_CURRENT_BANK_ACCOUNTS_FILE="$FRONTEND_INPUTS/current_bank_accounts.txt"
INITIAL_MASTER_BANK_ACCOUNTS_FILE="$BACKEND_INPUTS/master_bank_accounts.txt"

if [ ! -f "$DAILY_SCRIPT" ]; then
    echo "ERROR: Daily script not found at '$DAILY_SCRIPT'."
    exit 1
fi

mkdir -p "$SYSTEM_OUTPUTS"

current_bank_accounts_file="$INITIAL_CURRENT_BANK_ACCOUNTS_FILE"
master_bank_accounts_file="$INITIAL_MASTER_BANK_ACCOUNTS_FILE"

for day_number in 1 2 3 4 5 6 7
do
    echo " "
    echo "Running Sessions for day $day_number:"
    echo " "

    day_folder="$SYSTEM_OUTPUTS/day_${day_number}_run"
    mkdir -p "$day_folder"

    day_session_inputs="$REPO_ROOT/frontend/inputs/daily_session_inputs/day_${day_number}_session_inputs"
    merged_bank_account_transactions_file="$day_folder/merged_bank_account_transactions.txt"
    new_master_bank_accounts_file="$day_folder/new_master_bank_accounts.txt"
    new_current_bank_accounts_file="$day_folder/current_bank_accounts.txt"

    bash "$DAILY_SCRIPT" \
        "$day_session_inputs" \
        "$current_bank_accounts_file" \
        "$master_bank_accounts_file" \
        "$merged_bank_account_transactions_file" \
        "$new_master_bank_accounts_file" \
        "$new_current_bank_accounts_file"

    current_bank_accounts_file="$new_current_bank_accounts_file"
    master_bank_accounts_file="$new_master_bank_accounts_file"
done

echo "Weekly run completed."
