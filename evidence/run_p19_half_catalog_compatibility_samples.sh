#!/usr/bin/env bash
set -euo pipefail

threads="${1:-6}"
seconds_per_anchor="${2:-7200}"
shift "$(( $# >= 1 ? 1 : 0 ))"
shift "$(( $# >= 1 ? 1 : 0 ))"

source_file="evidence/p19_unrestricted_rank4_half_catalog_search_compatibility_crosscheck.cpp"
catalogue="evidence/k10_one_factorizations_396.txt"
binary="/private/tmp/p19_half_catalog_compatibility_crosscheck"
log_directory="evidence/p19_half_catalog_anchor_logs"
anchors=("$@")

if (( ${#anchors[@]} == 0 )); then
    anchors=(0 84 137 209)
fi

mkdir -p "$log_directory"
shasum -a 256 "$source_file" "$catalogue"
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic -pthread \
    "$source_file" -o "$binary"

for anchor in "${anchors[@]}"; do
    log_file="$(printf '%s/compat-lazy-anchor-%03d.txt' \
        "$log_directory" "$anchor")"
    "$binary" "$catalogue" "$seconds_per_anchor" "$threads" \
        "$((910835 + anchor))" "$anchor" | tee "$log_file"
    rg -q '^NO WITNESS FOR THIS ANCHOR \(complete\)$' "$log_file"
done
