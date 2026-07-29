#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
replay_dir=$(mktemp -d /private/tmp/orbit4-fixed-replay.XXXXXX)
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

for case_index in 00 01 02 03 04 05 06 07 08 09 10; do
    case_name=orbit4_pair_$case_index
    gzip -dc "$certificate_dir/$case_name.cnf.gz" > "$replay_dir/$case_name.cnf"
    gzip -dc "$certificate_dir/$case_name.learned.gz" > "$replay_dir/$case_name.learned"
    gzip -dc "$certificate_dir/$case_name.drat.gz" > "$replay_dir/$case_name.drat"
done

(
    cd "$replay_dir"
    shasum -a 256 -c "$certificate_dir/RAW_SHA256.txt"
)

TMPDIR="$replay_dir" PYTHONPYCACHEPREFIX="$replay_dir/pycache" \
    /usr/bin/python3 \
    "$certificate_dir/../2026-07-28_orbit4_fixed_pair_verify.py" \
    --results "$certificate_dir/../2026-07-28_orbit4_fixed_pair_certificate_results.jsonl" \
    --cnf-dir "$replay_dir"

for case_index in 00 01 02 03 04 05 06 07 08 09 10; do
    case_name=orbit4_pair_$case_index
    "$checker" \
        "$replay_dir/$case_name.cnf" \
        "$replay_dir/$case_name.drat"
done
