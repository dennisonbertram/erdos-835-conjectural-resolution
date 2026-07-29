#!/usr/bin/env python3
"""Export a HiGHS IPM-crossover basis for the exact five-point LP.

This is an acceleration helper, not a mathematical verifier.  The resulting
floating-point basis can seed SoPlex's exact rational refinement.  Only the
independent exact checker can certify the final rational primal point.
"""

from __future__ import annotations

import argparse

import numpy as np
import highspy

import solve_five_point_star_gluing_lp as model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--basis",
        default="five_point_full_reorder_highs.bas",
    )
    parser.add_argument(
        "--solution",
        default="five_point_full_reorder_highs.sol",
    )
    parser.add_argument("--time-limit", type=float, default=1800)
    args = parser.parse_args()

    (
        orbits,
        orbit_index,
        transitions,
        q,
        categories,
        four_records,
        five_records,
    ) = model.prepare()
    variable_count, four_vars, four_partitions = model.build_variables(
        four_records, five_records
    )
    variable_count, reorder_stats = model.collapse_full_reorder_symmetry(
        variable_count,
        four_records,
        four_vars,
        five_records,
    )

    rows = model.SparseRows()
    model.add_four_endpoint_rows(
        rows, four_records, four_partitions, four_vars, q
    )
    model.add_four_symmetry_rows(
        rows,
        four_records,
        four_partitions,
        four_vars,
        orbit_index,
    )
    model.add_local_bijection_rows(
        rows,
        orbits,
        transitions,
        q,
        four_partitions,
        four_vars,
    )
    model.add_slot_marginal_rows(
        rows,
        five_records,
        categories,
        four_partitions,
        four_vars,
    )
    model.add_rebased_rows(
        rows,
        "drop-y-w2",
        (0, 3, 2, 4),
        five_records,
        orbits,
        transitions,
        orbit_index,
        four_partitions,
        four_vars,
        integer_scale=False,
    )
    matrix = rows.matrix(variable_count)
    rhs = np.frombuffer(rows.rhs, dtype=np.float64)

    lp = highspy.HighsLp()
    lp.num_col_ = variable_count
    lp.num_row_ = matrix.shape[0]
    lp.col_cost_ = np.zeros(variable_count)
    lp.col_lower_ = np.zeros(variable_count)
    lp.col_upper_ = np.full(variable_count, highspy.kHighsInf)
    lp.row_lower_ = rhs
    lp.row_upper_ = rhs
    lp.col_names_ = [f"x{index}" for index in range(variable_count)]
    lp.row_names_ = [f"c{index}" for index in range(matrix.shape[0])]
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.num_col_ = variable_count
    lp.a_matrix_.num_row_ = matrix.shape[0]
    lp.a_matrix_.start_ = matrix.indptr
    lp.a_matrix_.index_ = matrix.indices
    lp.a_matrix_.value_ = matrix.data

    highs = highspy.Highs()
    assert highs.passModel(lp) == highspy.HighsStatus.kOk
    highs.setOptionValue("solver", "ipm")
    highs.setOptionValue("presolve", "off")
    highs.setOptionValue("run_crossover", "on")
    highs.setOptionValue("time_limit", args.time_limit)
    highs.setOptionValue("output_flag", True)
    highs.run()

    info = highs.getInfo()
    status = highs.getModelStatus()
    print(
        {
            "model_status": highs.modelStatusToString(status),
            "basis_validity": highs.basisValidityToString(
                info.basis_validity
            ),
            "ipm_iterations": info.ipm_iteration_count,
            "crossover_iterations": info.crossover_iteration_count,
            "reorder_symmetry": reorder_stats,
        },
        flush=True,
    )
    assert info.basis_validity == highspy.kBasisValidityValid
    assert highs.writeBasis(args.basis) == highspy.HighsStatus.kOk
    assert highs.writeSolution(args.solution, 0) == highspy.HighsStatus.kOk


if __name__ == "__main__":
    main()
