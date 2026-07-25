#!/usr/bin/env bash
set -euo pipefail

start_anchor="${1:-0}"
end_anchor="${2:-209}"
threads="${3:-8}"
seconds_per_anchor="${4:-600}"

source_file="evidence/p19_unrestricted_rank4_half_catalog_search.cpp"
catalogue="evidence/k10_one_factorizations_396.txt"
binary="/private/tmp/p19_half_catalog_search_all_anchors"
log_directory="evidence/p19_half_catalog_anchor_logs"

mkdir -p "$log_directory"
shasum -a 256 "$source_file" "$catalogue"
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic -pthread \
  "$source_file" -o "$binary"

for ((anchor = start_anchor; anchor <= end_anchor; ++anchor)); do
    log_file="$(printf '%s/anchor-%03d.txt' "$log_directory" "$anchor")"
    "$binary" "$catalogue" "$seconds_per_anchor" "$threads" \
      "$((190835 + anchor))" "$anchor" | tee "$log_file"
    if rg -q '^WITNESS$' "$log_file"; then
        exit 0
    fi
done
