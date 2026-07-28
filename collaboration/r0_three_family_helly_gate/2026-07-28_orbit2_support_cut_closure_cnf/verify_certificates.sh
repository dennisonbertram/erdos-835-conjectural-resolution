#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
replay_dir=$(mktemp -d /private/tmp/orbit2-replay.XXXXXX)
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

for case_name in C10 C4_marked C6_marked; do
    gzip -dc "$certificate_dir/$case_name.cnf.gz" > "$replay_dir/$case_name.cnf"
    gzip -dc "$certificate_dir/$case_name.drat.gz" > "$replay_dir/$case_name.drat"
done

(
    cd "$replay_dir"
    shasum -a 256 -c "$certificate_dir/RAW_SHA256.txt"
)

PYTHONPATH="$certificate_dir/.." PYTHONPYCACHEPREFIX="$replay_dir/pycache" \
    /usr/bin/python3 \
    "$certificate_dir/../2026-07-28_orbit2_support_cut_closure_verify.py" \
    --cnf-dir "$replay_dir"

for case_name in C10 C4_marked C6_marked; do
    "$checker" \
        "$replay_dir/$case_name.cnf" \
        "$replay_dir/$case_name.drat" \
        -i -w
done
