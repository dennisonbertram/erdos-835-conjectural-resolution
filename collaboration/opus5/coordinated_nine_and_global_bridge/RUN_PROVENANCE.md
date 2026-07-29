# Sanitized Opus 5 run provenance

Date: 2026-07-28.

The prompt for this run is committed at
`../prompts/2026-07-28_coordinated_nine_and_global_bridge_prompt.md`.
The run used `claude-opus-5` at the highest available reasoning effort
and completed successfully.

Recorded completion metadata:

- wall-clock duration: 4,118,023 ms;
- API processing duration: 3,983,163 ms;
- model turns: 43;
- reported cost: USD 15.3856255;
- model output tokens: 343,302; and
- terminal status: completed successfully.

The run produced `NOTE.md` and its four Python programs.  Three
deterministic verifiers ended with `ALL CHECKS PASS`; the fourth program
is explicitly a fixed-seed search and supplies evidence only.

## Independent post-run correction

The run proposed Statement (T3) after finding no counterexample in its
bounded search.  An independent exact certificate subsequently refuted
T3.  `NOTE.md` has been amended to mark the statement false and to identify
the narrower equality-core trade that actually remains.  No theorem in the
note relies on T3 or on the bounded search.

## Why the raw stream is not published

The raw machine stream is deliberately excluded from version control.  It
contains local filesystem paths, account identifiers, environment
inventory, session identifiers, and signed internal reasoning payloads.
Those records are not mathematical evidence and are unsuitable for a
public repository.  The public evidence consists instead of the original
prompt, this provenance record, the corrected note, the executable
verifiers, and their reproducible outputs.
