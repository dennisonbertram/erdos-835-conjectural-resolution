#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CHECKER=${1:-drat-trim}
PROOF=$(mktemp "${TMPDIR:-/tmp}/erdos835-prefix-drat.XXXXXX")
trap 'rm -f "$PROOF"' EXIT HUP INT TERM

gzip -dc "$HERE/finite_completion.drat.gz" > "$PROOF"
"$CHECKER" "$HERE/finite_completion.cnf" "$PROOF"
