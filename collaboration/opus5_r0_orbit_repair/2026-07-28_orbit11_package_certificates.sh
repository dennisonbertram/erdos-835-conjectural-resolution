#!/bin/sh
set -eu

export LC_ALL=C
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
raw_dir=${RAW_DIR:-"$script_dir/2026-07-28_orbit11_fixed_pair_raw"}
proof_dir=${PROOF_DIR:-"$script_dir/2026-07-28_orbit11_fixed_pair_proof_work"}
package_dir=${PACKAGE_DIR:-"$script_dir/2026-07-28_orbit11_fixed_pair_cnf"}
all_cases="000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030 031 032 033 034 035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051 052 053 054 055 056 057 058 059 060 061 062 063 064 065 066 067 068 069 070 071 072 073 074 075 076 077 078 079 080 081 082 083 084 085 086 087 088 089 090 091 092"

if [ -e "$package_dir" ]; then
    echo "Refusing to overwrite existing package: $package_dir" >&2
    exit 2
fi
mkdir -p "$package_dir"

cp "$script_dir/2026-07-28_orbit11_fixed_pair_verify.py" \
    "$package_dir/orbit11_fixed_pair_verify.py"
cp "$script_dir/../r0_three_family_helly_gate/search_counterexamples.py" \
    "$package_dir/search_counterexamples.py"
cp "$script_dir/2026-07-28_remaining_pair_orbit_classifier.py" \
    "$package_dir/remaining_pair_orbit_classifier.py"
cp "$script_dir/2026-07-28_orbit11_fixed_pair_results.jsonl" \
    "$package_dir/orbit11_fixed_pair_results.jsonl"
cp "$script_dir/2026-07-28_orbit11_merge_results.py" \
    "$package_dir/orbit11_merge_results.py"
for worker_index in 0 1 2 3; do
    cp "$script_dir/2026-07-28_orbit11_fixed_pair_worker_$worker_index.jsonl" \
        "$package_dir/orbit11_fixed_pair_worker_$worker_index.jsonl"
done
cp "$script_dir/2026-07-28_orbit11_fixed_pair_classifier_audit.json" \
    "$package_dir/CLASSIFIER_AUDIT.json"
cp "$script_dir/2026-07-28_orbit11_fixed_pair_raw_audit.json" \
    "$package_dir/RAW_AUDIT.json"
cp "$script_dir/2026-07-28_orbit11_certificate_results.json" \
    "$package_dir/CERTIFICATE_RESULTS.json"
cp "$script_dir/2026-07-28_orbit11_toolchain.json" \
    "$package_dir/TOOLCHAIN.json"
cp "$script_dir/2026-07-28_orbit11_verify_certificates.sh" \
    "$package_dir/verify_certificates.sh"
cp "$script_dir/2026-07-28_orbit11_generate_proofs.sh" \
    "$package_dir/generate_proofs.sh"
cp "$script_dir/2026-07-28_orbit11_replay_raw.sh" \
    "$package_dir/replay_raw.sh"
cp "$script_dir/2026-07-28_orbit11_package_certificates.sh" \
    "$package_dir/package_certificates.sh"
chmod +x \
    "$package_dir/verify_certificates.sh" \
    "$package_dir/generate_proofs.sh" \
    "$package_dir/replay_raw.sh" \
    "$package_dir/package_certificates.sh"

raw_manifest=$package_dir/RAW_SHA256.txt
: >"$raw_manifest"

record_and_compress() {
    source_path=$1
    raw_name=$2
    compressed_path=$package_dir/$raw_name.gz
    if [ ! -f "$source_path" ]; then
        echo "Missing raw artifact: $source_path" >&2
        exit 2
    fi
    raw_digest=$(shasum -a 256 "$source_path" | awk '{print $1}')
    printf '%s  %s\n' "$raw_digest" "$raw_name" >>"$raw_manifest"
    gzip -9 -n -c "$source_path" >"$compressed_path"
}

for case_index in $all_cases; do
    case_name=orbit11_pair_$case_index
    record_and_compress \
        "$raw_dir/$case_name.cnf" \
        "$case_name.cnf"
    record_and_compress \
        "$raw_dir/$case_name.learned" \
        "$case_name.learned"
    record_and_compress \
        "$proof_dir/$case_name.drat" \
        "$case_name.drat"
    record_and_compress \
        "$proof_dir/$case_name.cadical.log" \
        "$case_name.cadical.log"
    record_and_compress \
        "$proof_dir/$case_name.drat-trim.log" \
        "$case_name.drat-trim.log"
done

(
    cd "$package_dir"
    shasum -a 256 \
        ./*.gz \
        CERTIFICATE_RESULTS.json \
        CLASSIFIER_AUDIT.json \
        RAW_AUDIT.json \
        RAW_SHA256.txt \
        TOOLCHAIN.json \
        generate_proofs.sh \
        orbit11_fixed_pair_results.jsonl \
        orbit11_fixed_pair_verify.py \
        orbit11_fixed_pair_worker_0.jsonl \
        orbit11_fixed_pair_worker_1.jsonl \
        orbit11_fixed_pair_worker_2.jsonl \
        orbit11_fixed_pair_worker_3.jsonl \
        orbit11_merge_results.py \
        package_certificates.sh \
        remaining_pair_orbit_classifier.py \
        replay_raw.sh \
        search_counterexamples.py \
        verify_certificates.sh \
        >MANIFEST.sha256
)
