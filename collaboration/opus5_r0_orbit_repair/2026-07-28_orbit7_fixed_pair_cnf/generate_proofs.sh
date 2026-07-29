#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
raw_dir=${RAW_DIR:-"$script_dir/2026-07-28_orbit7_fixed_pair_raw"}
proof_dir=${PROOF_DIR:-"$script_dir/2026-07-28_orbit7_fixed_pair_proof_work"}
cadical=${CADICAL:-/opt/homebrew/bin/cadical}
expected_cadical_sha=52daad7dcbb97d3d68a7494fb415ba54a509c49d30f5dfcd157e1bcbe138e6ee
all_cases="000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030 031 032 033 034 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051 052 053 054 055 056 057 058 059 060 061 062 063 064 065 066 067 068 069 070 071 072 073 074 075"
case_indices=${CASES:-$all_cases}

if [ ! -x "$cadical" ]; then
    echo "CaDiCaL executable not found: $cadical" >&2
    exit 2
fi

actual_cadical_sha=$(shasum -a 256 "$cadical" | awk '{print $1}')
if [ "$actual_cadical_sha" != "$expected_cadical_sha" ]; then
    echo "Unexpected CaDiCaL SHA-256: $actual_cadical_sha" >&2
    exit 2
fi
if [ "$("$cadical" --version)" != "3.0.1" ]; then
    echo "Expected CaDiCaL 3.0.1" >&2
    exit 2
fi

mkdir -p "$proof_dir"
for case_index in $case_indices; do
    case_name=orbit7_pair_$case_index
    cnf_path=$raw_dir/$case_name.cnf
    proof_path=$proof_dir/$case_name.drat
    log_path=$proof_dir/$case_name.cadical.log
    temporary_proof=$proof_path.tmp
    temporary_log=$log_path.tmp

    if [ ! -f "$cnf_path" ]; then
        echo "Missing frozen CNF: $cnf_path" >&2
        exit 2
    fi
    if [ -s "$proof_path" ] && [ -s "$log_path" ]; then
        grep -q -- "--checkproof=1" "$log_path"
        grep -q "writing binary proof trace" "$log_path"
        grep -q "^s UNSATISFIABLE$" "$log_path"
        grep -q "^c exit 20$" "$log_path"
        echo "$case_name already complete"
        continue
    fi
    if [ -e "$proof_path" ] || [ -e "$log_path" ]; then
        echo "Incomplete final proof artifacts for $case_name" >&2
        exit 2
    fi

    rm -f -- "$temporary_proof" "$temporary_log"
    set +e
    "$cadical" --checkproof=1 \
        "$cnf_path" "$temporary_proof" \
        >"$temporary_log" 2>&1
    exit_status=$?
    set -e
    if [ "$exit_status" -ne 20 ]; then
        echo "CaDiCaL failed for $case_name with status $exit_status" >&2
        exit "$exit_status"
    fi
    grep -q -- "--checkproof=1" "$temporary_log"
    grep -q "writing binary proof trace" "$temporary_log"
    grep -q "^s UNSATISFIABLE$" "$temporary_log"
    grep -q "^c exit 20$" "$temporary_log"
    test -s "$temporary_proof"
    mv -- "$temporary_proof" "$proof_path"
    mv -- "$temporary_log" "$log_path"
    echo "$case_name internally checked UNSAT"
done
