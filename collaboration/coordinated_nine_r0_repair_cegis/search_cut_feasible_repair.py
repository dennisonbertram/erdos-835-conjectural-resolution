#!/usr/bin/env python3
"""CEGIS for a one-layer repair producing a cut-feasible triple.

This is a discovery search, not a proof certificate.  It uses the exact r=0
prefix and row CNF from ``search_one_layer_repair.py`` but asks only for three
of the seven size-ten rows that satisfy every internal-edge capacity cut.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Iterable

from pysat.solvers import Cadical195

from search_one_layer_repair import (
    EDGES,
    PREFIX_SIZES,
    VERTEX_SET,
    VERTICES,
    Cnf,
    build_instance,
    decode_model,
    display_edges,
    edge_mask,
    endpoints,
    is_matching_on,
    matching_family,
    nested_integer_lists,
    other_occupied,
    reject_duplicate_keys,
    remaining_row,
    support_vertex,
    integer_list,
    validate_raw_instance,
)


TRIPLE_COLOURS = tuple(range(7))


@dataclass(frozen=True)
class CutWitness:
    """A repair, selected rows, and residual-edge capacity certificate."""

    repair_layer: int
    replacement: tuple[int, ...]
    free_edges: tuple[int, ...]
    colours: tuple[int, int, int]
    complements: tuple[tuple[int, ...], ...]

    def record(self) -> dict[str, object]:
        return {
            "repair_layer": self.repair_layer,
            "replacement": list(self.replacement),
            "free_edges": list(self.free_edges),
            "colours": list(self.colours),
            "complements": [list(row) for row in self.complements],
        }


@dataclass(frozen=True)
class ExactUnionCutWitness:
    """Legacy witness fixing the exact union of the other five layers."""

    repair_layer: int
    replacement: tuple[int, ...]
    other_mask: int
    colours: tuple[int, int, int]
    complements: tuple[tuple[int, ...], ...]

    def record(self) -> dict[str, object]:
        return {
            "repair_layer": self.repair_layer,
            "replacement": list(self.replacement),
            "other_edges": [
                edge_index
                for edge_index in range(len(EDGES))
                if self.other_mask & (1 << edge_index)
            ],
            "colours": list(self.colours),
            "complements": [list(row) for row in self.complements],
        }


def validate_cut_witness(witness: CutWitness) -> None:
    if not 0 <= witness.repair_layer < 6:
        raise AssertionError("invalid repair layer")
    if len(witness.replacement) != PREFIX_SIZES[witness.repair_layer]:
        raise AssertionError("replacement has the wrong size")
    support = frozenset(endpoints(witness.replacement))
    if not is_matching_on(witness.replacement, support):
        raise AssertionError("replacement is not a perfect matching")
    if (
        tuple(sorted(witness.free_edges)) != witness.free_edges
        or len(set(witness.free_edges)) != len(witness.free_edges)
        or any(not 0 <= edge_index < len(EDGES) for edge_index in witness.free_edges)
    ):
        raise AssertionError("free-edge certificate is not canonical")
    if not set(witness.replacement) <= set(witness.free_edges):
        raise AssertionError("replacement edges are not certified free")
    if tuple(sorted(witness.colours)) != witness.colours:
        raise AssertionError("selected colours are not canonical")
    if len(set(witness.colours)) != 3 or any(
        colour not in TRIPLE_COLOURS for colour in witness.colours
    ):
        raise AssertionError("selected colours are not three triple rows")
    if len(witness.complements) != 3:
        raise AssertionError("wrong complement count")
    for complement in witness.complements:
        if (
            len(complement) != 3
            or tuple(sorted(complement)) != complement
            or len(set(complement)) != 3
            or any(vertex not in VERTEX_SET for vertex in complement)
        ):
            raise AssertionError("invalid triple complement")
    certificate_mask = edge_mask(
        edge_index
        for edge_index in witness.free_edges
        if edge_index not in witness.replacement
    )
    for internal_mask, required in cut_requirements(witness.complements):
        if bin(internal_mask & certificate_mask).count("1") < required:
            raise AssertionError("free edges do not certify every capacity cut")


def validate_exact_union_witness(witness: ExactUnionCutWitness) -> None:
    if not 0 <= witness.repair_layer < 6:
        raise AssertionError("invalid repair layer")
    if len(witness.replacement) != PREFIX_SIZES[witness.repair_layer]:
        raise AssertionError("replacement has the wrong size")
    support = frozenset(endpoints(witness.replacement))
    if not is_matching_on(witness.replacement, support):
        raise AssertionError("replacement is not a perfect matching")
    if witness.other_mask < 0 or witness.other_mask >> len(EDGES):
        raise AssertionError("other-layer mask has an invalid edge bit")
    if edge_mask(witness.replacement) & witness.other_mask:
        raise AssertionError("replacement meets another prefix layer")
    if tuple(sorted(witness.colours)) != witness.colours:
        raise AssertionError("selected colours are not canonical")
    if len(set(witness.colours)) != 3 or any(
        colour not in TRIPLE_COLOURS for colour in witness.colours
    ):
        raise AssertionError("selected colours are not three triple rows")
    if len(witness.complements) != 3:
        raise AssertionError("wrong complement count")
    for complement in witness.complements:
        if (
            len(complement) != 3
            or tuple(sorted(complement)) != complement
            or len(set(complement)) != 3
            or any(vertex not in VERTEX_SET for vertex in complement)
        ):
            raise AssertionError("invalid triple complement")
    requirements = cut_requirements(witness.complements)
    deleted_mask = witness.other_mask | edge_mask(witness.replacement)
    if not cuts_hold(requirements, deleted_mask):
        raise AssertionError("exact other-layer union is not cut-feasible")


@lru_cache(maxsize=None)
def cut_requirements(
    complements: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int], ...]:
    """Return all potentially binding size-six, seven, and eight cuts."""
    supports = tuple(VERTEX_SET - frozenset(row) for row in complements)
    requirements: list[tuple[int, int]] = []
    for size in (6, 7, 8):
        for vertices in combinations(VERTICES, size):
            vertex_set = frozenset(vertices)
            required = sum(
                max(0, len(support & vertex_set) - 5) for support in supports
            )
            minimum_available = size * (size - 1) // 2 - 5 * size // 2
            if required <= minimum_available:
                continue
            internal_mask = edge_mask(
                edge_index
                for edge_index, edge in enumerate(EDGES)
                if edge[0] in vertex_set and edge[1] in vertex_set
            )
            requirements.append((internal_mask, required))
    return tuple(requirements)


def cuts_hold(requirements: tuple[tuple[int, int], ...], deleted_mask: int) -> bool:
    return all(
        bin(internal_mask & ~deleted_mask).count("1") >= required
        for internal_mask, required in requirements
    )


def cut_certificate(
    requirements: tuple[tuple[int, int], ...],
    deleted_mask: int,
) -> tuple[int, ...] | None:
    """Choose explicit residual edges witnessing every capacity inequality."""
    selected: set[int] = set()
    for internal_mask, required in requirements:
        available = internal_mask & ~deleted_mask
        available_edges = tuple(
            edge_index
            for edge_index in range(len(EDGES))
            if available & (1 << edge_index)
        )
        if len(available_edges) < required:
            return None
        selected.update(available_edges[:required])

    # Make the certificate inclusion-minimal.  Removing a residual edge is
    # safe exactly when every cut containing it still has more selected
    # witnesses than its lower bound.
    selected_counts = [
        sum(bool(internal_mask & (1 << edge_index)) for edge_index in selected)
        for internal_mask, _ in requirements
    ]
    for edge_index in sorted(selected, reverse=True):
        affected = [
            index
            for index, (internal_mask, _) in enumerate(requirements)
            if internal_mask & (1 << edge_index)
        ]
        if any(
            selected_counts[index] <= requirements[index][1]
            for index in affected
        ):
            continue
        selected.remove(edge_index)
        for index in affected:
            selected_counts[index] -= 1
    return tuple(sorted(selected))


def witness_clause(
    cnf: Cnf,
    witness: CutWitness | ExactUnionCutWitness,
) -> tuple[int, ...]:
    """Negate the exact semantic conditions under which the witness works."""
    if isinstance(witness, CutWitness):
        validate_cut_witness(witness)
    else:
        validate_exact_union_witness(witness)
    support = frozenset(endpoints(witness.replacement))
    literals: list[int] = []
    for vertex in VERTICES:
        literal = support_vertex(cnf, witness.repair_layer, vertex)
        literals.append(-literal if vertex in support else literal)

    if isinstance(witness, CutWitness):
        # The replacement edges and the selected residual certificate edges
        # need only remain unused by the other five layers.
        literals.extend(
            other_occupied(cnf, witness.repair_layer, edge_index)
            for edge_index in witness.free_edges
        )
    else:
        # Legacy proof streams fixed the exact other-layer union.  Preserve
        # that clause semantics so old records remain replayable.
        for edge_index in range(len(EDGES)):
            literal = other_occupied(cnf, witness.repair_layer, edge_index)
            literals.append(
                -literal
                if witness.other_mask & (1 << edge_index)
                else literal
            )

    for colour, complement in zip(witness.colours, witness.complements):
        complement_set = frozenset(complement)
        for vertex in VERTICES:
            literal = remaining_row(cnf, colour, vertex)
            literals.append(-literal if vertex in complement_set else literal)
    return tuple(dict.fromkeys(literals))


def canonical_record(
    witness: CutWitness | ExactUnionCutWitness,
    clause: tuple[int, ...],
) -> str:
    record = witness.record()
    record["clause_sha256"] = hashlib.sha256(
        " ".join(map(str, clause)).encode("ascii")
    ).hexdigest()
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def decode_witness_record(
    value: object,
) -> tuple[CutWitness | ExactUnionCutWitness, str]:
    if not isinstance(value, dict):
        raise ValueError("witness record must be a JSON object")
    expected_common = {
        "repair_layer",
        "replacement",
        "colours",
        "complements",
        "clause_sha256",
    }
    free_schema = expected_common | {"free_edges"}
    exact_schema = expected_common | {"other_edges"}
    if set(value) not in (free_schema, exact_schema):
        raise ValueError("witness record keys do not match the canonical schema")
    repair_layer = value["repair_layer"]
    if type(repair_layer) is not int:
        raise ValueError("repair_layer must be an integer")
    clause_sha256 = value["clause_sha256"]
    if (
        not isinstance(clause_sha256, str)
        or len(clause_sha256) != 64
        or any(character not in "0123456789abcdef" for character in clause_sha256)
    ):
        raise ValueError("clause_sha256 must be 64 lowercase hexadecimal digits")
    replacement = integer_list(value["replacement"], field="replacement")
    colours = integer_list(value["colours"], field="colours")
    complements = nested_integer_lists(
        value["complements"],
        field="complements",
    )
    if set(value) == free_schema:
        witness: CutWitness | ExactUnionCutWitness = CutWitness(
            repair_layer=repair_layer,
            replacement=replacement,
            free_edges=integer_list(value["free_edges"], field="free_edges"),
            colours=colours,
            complements=complements,
        )
        validate_cut_witness(witness)
    else:
        other_edges = integer_list(value["other_edges"], field="other_edges")
        if (
            tuple(sorted(other_edges)) != other_edges
            or len(set(other_edges)) != len(other_edges)
            or any(
                not 0 <= edge_index < len(EDGES)
                for edge_index in other_edges
            )
        ):
            raise ValueError("other_edges must be distinct canonical edge indices")
        witness = ExactUnionCutWitness(
            repair_layer=repair_layer,
            replacement=replacement,
            other_mask=edge_mask(other_edges),
            colours=colours,
            complements=complements,
        )
        validate_exact_union_witness(witness)
    return witness, clause_sha256


def replay_witnesses(
    cnf: Cnf,
    path: Path,
) -> Iterable[tuple[CutWitness | ExactUnionCutWitness, str]]:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            raw = line.rstrip("\r\n")
            if not raw:
                raise ValueError(f"{path}:{line_number}: blank record")
            try:
                value = json.loads(raw, object_pairs_hook=reject_duplicate_keys)
                witness, recorded_hash = decode_witness_record(value)
                clause = witness_clause(cnf, witness)
                expected = canonical_record(witness, clause)
            except (AssertionError, json.JSONDecodeError, ValueError) as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
            expected_hash = json.loads(expected)["clause_sha256"]
            if recorded_hash != expected_hash:
                raise ValueError(f"{path}:{line_number}: clause hash mismatch")
            if raw != expected:
                raise ValueError(f"{path}:{line_number}: noncanonical JSON")
            cnf.add(*clause)
            yield witness, expected


def write_dimacs(path: Path, cnf: Cnf) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with path.open("w", encoding="ascii", newline="\n") as output:
        header = f"p cnf {cnf.top} {len(cnf.clauses)}\n"
        output.write(header)
        digest.update(header.encode("ascii"))
        for clause in cnf.clauses:
            line = " ".join(map(str, (*clause, 0))) + "\n"
            output.write(line)
            digest.update(line.encode("ascii"))
    return digest.hexdigest()


def find_cut_witnesses(
    prefix: tuple[tuple[int, ...], ...],
    rows: tuple[tuple[int, ...], ...],
    *,
    limit: int,
    deadline: float,
) -> tuple[tuple[CutWitness, ...], bool]:
    """Find up to ``limit`` one-repair cut-feasible routes."""
    route_data = tuple(
        (
            colours,
            tuple(rows[colour] for colour in colours),
            cut_requirements(tuple(rows[colour] for colour in colours)),
        )
        for colours in combinations(TRIPLE_COLOURS, 3)
    )
    prefix_masks = tuple(edge_mask(layer) for layer in prefix)
    witnesses: list[CutWitness] = []
    represented: set[tuple[int, int, int, int]] = set()
    for repair_layer in range(6):
        other_mask = 0
        for colour, mask in enumerate(prefix_masks):
            if colour != repair_layer:
                other_mask |= mask
        support = endpoints(prefix[repair_layer])
        for replacement, replacement_mask in matching_family(support):
            if replacement_mask & other_mask:
                continue
            deleted_mask = other_mask | replacement_mask
            for colours, complements, requirements in route_data:
                signature = (repair_layer, *colours)
                if signature in represented:
                    continue
                certificate = cut_certificate(requirements, deleted_mask)
                if certificate is None:
                    continue
                witness = CutWitness(
                    repair_layer=repair_layer,
                    replacement=replacement,
                    free_edges=tuple(sorted(set(replacement) | set(certificate))),
                    colours=colours,
                    complements=complements,
                )
                validate_cut_witness(witness)
                witnesses.append(witness)
                represented.add(signature)
                if len(witnesses) >= limit:
                    return tuple(witnesses), False
            if time.monotonic() >= deadline:
                return tuple(witnesses), True
    return tuple(witnesses), False


def independently_has_cut_witness(
    prefix: tuple[tuple[int, ...], ...],
    rows: tuple[tuple[int, ...], ...],
    *,
    deadline: float,
) -> tuple[bool, bool]:
    """Raw second pass that shares no learned-clause construction."""
    prefix_masks = tuple(edge_mask(layer) for layer in prefix)
    requirements = tuple(
        cut_requirements(tuple(rows[colour] for colour in colours))
        for colours in combinations(TRIPLE_COLOURS, 3)
    )
    for repair_layer in range(6):
        other_mask = 0
        for colour, mask in enumerate(prefix_masks):
            if colour != repair_layer:
                other_mask |= mask
        support = endpoints(prefix[repair_layer])
        for _, replacement_mask in matching_family(support):
            if replacement_mask & other_mask:
                continue
            deleted_mask = other_mask | replacement_mask
            if any(cuts_hold(route, deleted_mask) for route in requirements):
                return True, False
            if time.monotonic() >= deadline:
                return False, True
    return False, False


def solve(
    *,
    max_rounds: int,
    cuts_per_model: int,
    time_limit_seconds: float,
    witness_log: Path | None,
    replay_witness_log: Path | None,
    unsat_cnf_dir: Path | None,
) -> dict[str, object]:
    start = time.monotonic()
    deadline = start + time_limit_seconds
    cnf = build_instance()
    initial_clauses = len(cnf.clauses)
    witness_hasher = hashlib.sha256()
    replay_hasher = hashlib.sha256()
    replayed_cuts = 0
    if replay_witness_log:
        for _, record in replay_witnesses(cnf, replay_witness_log):
            encoded = record.encode("utf-8") + b"\n"
            replay_hasher.update(encoded)
            witness_hasher.update(encoded)
            replayed_cuts += 1
    clauses_after_replay = len(cnf.clauses)
    solver = Cadical195(bootstrap_with=cnf.clauses)
    log_stream = witness_log.open("w", encoding="utf-8") if witness_log else None
    cuts = replayed_cuts
    new_cuts = 0
    rounds = 0
    result: dict[str, object]
    try:
        while max_rounds == 0 or rounds < max_rounds:
            if time.monotonic() >= deadline:
                result = {"status": "time_limit"}
                break
            rounds += 1
            if not solver.solve():
                result = {
                    "status": "unsat_uncertified",
                    "proof_claimed": False,
                }
                break
            model = {literal for literal in solver.get_model() if literal > 0}
            prefix, rows = decode_model(cnf, model)
            validate_raw_instance(prefix, rows)
            witnesses, timed_out = find_cut_witnesses(
                prefix,
                rows,
                limit=cuts_per_model,
                deadline=deadline,
            )
            if timed_out:
                result = {"status": "time_limit"}
                break
            if not witnesses:
                has_witness, replay_timed_out = independently_has_cut_witness(
                    prefix,
                    rows,
                    deadline=deadline,
                )
                if replay_timed_out:
                    result = {"status": "time_limit"}
                    break
                if has_witness:
                    raise AssertionError("independent pass found a missed witness")
                result = {
                    "status": "counterexample",
                    "counterexample_validated": True,
                    "prefix": [display_edges(layer) for layer in prefix],
                    "remaining_complements": [list(row) for row in rows],
                }
                break
            for witness in witnesses:
                clause = witness_clause(cnf, witness)
                solver.add_clause(clause)
                cnf.add(*clause)
                cuts += 1
                new_cuts += 1
                record = canonical_record(witness, clause)
                witness_hasher.update(record.encode("utf-8") + b"\n")
                if log_stream:
                    log_stream.write(record + "\n")
                    log_stream.flush()
        else:
            result = {"status": "round_limit"}
    finally:
        solver.delete()
        if log_stream:
            log_stream.close()

    if result["status"] == "unsat_uncertified" and unsat_cnf_dir is not None:
        cnf_path = unsat_cnf_dir / "cut_feasible_repair.cnf"
        result["cnf_sha256"] = write_dimacs(cnf_path, cnf)
        result["cnf_path"] = str(cnf_path)

    result.update(
        {
            "rounds": rounds,
            "cuts": cuts,
            "replayed_cuts": replayed_cuts,
            "new_cuts": new_cuts,
            "variables": cnf.top,
            "initial_clauses": initial_clauses,
            "clauses_after_replay": clauses_after_replay,
            "final_clauses": len(cnf.clauses),
            "witness_sha256": witness_hasher.hexdigest(),
            "replay_sha256": replay_hasher.hexdigest(),
            "elapsed_seconds": round(time.monotonic() - start, 3),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--cuts-per-model", type=int, default=990)
    parser.add_argument("--time-limit-seconds", type=float, default=600.0)
    parser.add_argument("--witness-log", type=Path)
    parser.add_argument("--replay-witness-log", type=Path)
    parser.add_argument("--unsat-cnf-dir", type=Path)
    args = parser.parse_args()
    if args.max_rounds < 0:
        parser.error("--max-rounds must be nonnegative")
    if args.cuts_per_model <= 0:
        parser.error("--cuts-per-model must be positive")
    if args.time_limit_seconds <= 0:
        parser.error("--time-limit-seconds must be positive")
    if (
        args.replay_witness_log
        and args.witness_log
        and args.replay_witness_log.resolve() == args.witness_log.resolve()
    ):
        parser.error(
            "--witness-log must differ from --replay-witness-log "
            "to protect the replay input"
        )
    result = solve(
        max_rounds=args.max_rounds,
        cuts_per_model=args.cuts_per_model,
        time_limit_seconds=args.time_limit_seconds,
        witness_log=args.witness_log,
        replay_witness_log=args.replay_witness_log,
        unsat_cnf_dir=args.unsat_cnf_dir,
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
