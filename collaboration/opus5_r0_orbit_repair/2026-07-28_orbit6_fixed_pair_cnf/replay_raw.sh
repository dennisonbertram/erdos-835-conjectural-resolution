#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
raw_dir=${RAW_DIR:-"$script_dir/2026-07-28_orbit6_fixed_pair_raw"}
proof_dir=${PROOF_DIR:-"$script_dir/2026-07-28_orbit6_fixed_pair_proof_work"}
checker=${DRAT_TRIM:-/private/tmp/drat-trim-build.tsJCcW/drat-trim-master/drat-trim}
expected_checker_sha=42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9
all_cases="000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022"
case_indices=${CASES:-$all_cases}

if [ ! -x "$checker" ]; then
    echo "drat-trim executable not found: $checker" >&2
    exit 2
fi
actual_checker_sha=$(shasum -a 256 "$checker" | awk '{print $1}')
if [ "$actual_checker_sha" != "$expected_checker_sha" ]; then
    echo "Unexpected drat-trim SHA-256: $actual_checker_sha" >&2
    exit 2
fi

for case_index in $case_indices; do
    case_name=orbit6_pair_$case_index
    cnf_path=$raw_dir/$case_name.cnf
    proof_path=$proof_dir/$case_name.drat
    log_path=$proof_dir/$case_name.drat-trim.log
    temporary_log=$log_path.tmp

    test -f "$cnf_path"
    test -s "$proof_path"
    if [ -s "$log_path" ]; then
        grep -q "s VERIFIED" "$log_path"
        echo "$case_name already externally VERIFIED"
        continue
    fi
    if [ -e "$log_path" ]; then
        echo "Incomplete replay log for $case_name" >&2
        exit 2
    fi

    rm -f -- "$temporary_log"
    "$checker" "$cnf_path" "$proof_path" \
        >"$temporary_log" 2>&1
    grep -q "s VERIFIED" "$temporary_log"
    mv -- "$temporary_log" "$log_path"
    echo "$case_name externally VERIFIED"
done
