#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
replay_dir=$(mktemp -d /private/tmp/orbit6-fixed-replay.XXXXXX)
trap 'rm -rf -- "$replay_dir"' EXIT HUP INT TERM

if [ "${DRAT_TRIM:-}" ]; then
    checker=$DRAT_TRIM
elif command -v drat-trim >/dev/null 2>&1; then
    checker=$(command -v drat-trim)
else
    echo "Set DRAT_TRIM to the upstream drat-trim executable." >&2
    exit 2
fi

(
    cd "$certificate_dir"
    shasum -a 256 -c MANIFEST.sha256
    gzip -t ./*.gz
)

for case_index in \
    000 001 002 003 004 005 006 007 008 009 010 011 \
    012 013 014 015 016 017 018 019 020 021 022
do
    case_name=orbit6_pair_$case_index
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
    "$certificate_dir/orbit6_fixed_pair_verify.py" \
    --results "$certificate_dir/orbit6_fixed_pair_results.jsonl" \
    --cnf-dir "$replay_dir"

for case_index in \
    000 001 002 003 004 005 006 007 008 009 010 011 \
    012 013 014 015 016 017 018 019 020 021 022
do
    case_name=orbit6_pair_$case_index
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
