#!/bin/bash
set -xe
padc_script_dir="$HOME/git_hub/padc"

# cleanup
for i in {1..5}; do
    env VIRTUAL_ENV="$padc_script_dir/.venv" "$padc_script_dir/.venv/bin/padc" users delete -f "$padc_script_dir/.env" "Pingu${i} pythonico${i}"
done
