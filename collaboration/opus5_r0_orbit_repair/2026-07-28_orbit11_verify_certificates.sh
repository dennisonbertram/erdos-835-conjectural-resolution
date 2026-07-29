#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
replay_dir=$(mktemp -d /private/tmp/orbit11-fixed-replay.XXXXXX)
trap 'rm -rf -- "$replay_dir"' EXIT HUP INT TERM
expected_checker_sha=42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9
all_cases="000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030 031 032 033 034 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051 052 053 054 055 056 057 058 059 060 061 062 063 064 065 066 067 068 069 070 071 072 073 074 075 076 077 078 079 080 081 082 083 084 085 086 087 088 089 090 091 092"

if [ "${DRAT_TRIM:-}" ]; then
    checker=$DRAT_TRIM
elif command -v drat-trim >/dev/null 2>&1; then
    checker=$(command -v drat-trim)
else
    echo "Set DRAT_TRIM to the upstream drat-trim executable." >&2
    exit 2
fi
actual_checker_sha=$(shasum -a 256 "$checker" | awk '{print $1}')
if [ "$actual_checker_sha" != "$expected_checker_sha" ]; then
    echo "Unexpected drat-trim SHA-256: $actual_checker_sha" >&2
    exit 2
fi

(
    cd "$certificate_dir"
    shasum -a 256 -c MANIFEST.sha256
    gzip -t ./*.gz
    TMPDIR="$replay_dir" PYTHONPYCACHEPREFIX="$replay_dir/merge-pycache" \
        /usr/bin/python3 orbit11_merge_results.py \
        orbit11_fixed_pair_worker_0.jsonl \
        orbit11_fixed_pair_worker_1.jsonl \
        orbit11_fixed_pair_worker_2.jsonl \
        orbit11_fixed_pair_worker_3.jsonl \
        >"$replay_dir/merged.jsonl"
    cmp orbit11_fixed_pair_results.jsonl "$replay_dir/merged.jsonl"
)

for case_index in $all_cases; do
    case_name=orbit11_pair_$case_index
    for suffix in cnf learned drat cadical.log drat-trim.log; do
        gzip -dc "$certificate_dir/$case_name.$suffix.gz" \
            >"$replay_dir/$case_name.$suffix"
    done
done

(
    cd "$replay_dir"
    shasum -a 256 -c "$certificate_dir/RAW_SHA256.txt"
)

TMPDIR="$replay_dir" PYTHONPYCACHEPREFIX="$replay_dir/pycache" \
    /usr/bin/python3 \
    "$certificate_dir/orbit11_fixed_pair_verify.py" \
    --results "$certificate_dir/orbit11_fixed_pair_results.jsonl" \
    --cnf-dir "$replay_dir"

for case_index in $all_cases; do
    case_name=orbit11_pair_$case_index
    grep -q -- "--checkproof=1" \
        "$replay_dir/$case_name.cadical.log"
    grep -q "writing binary proof trace" \
        "$replay_dir/$case_name.cadical.log"
    grep -q "^s UNSATISFIABLE$" \
        "$replay_dir/$case_name.cadical.log"
    grep -q "^c exit 20$" \
        "$replay_dir/$case_name.cadical.log"
    grep -q "s VERIFIED" \
        "$replay_dir/$case_name.drat-trim.log"
    "$checker" \
        "$replay_dir/$case_name.cnf" \
        "$replay_dir/$case_name.drat"
done
