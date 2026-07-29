// Search binary even subcodes for a Griesmer obstruction to S(14,15,31).
//
// This is an exploratory search.  Every reported candidate is evaluated
// exactly from the forced point-incidence-code Fourier values.  In the
// even subcode the only unknown case is size 16.  We treat every such set
// as the complement of a block, increasing its Fourier value by 2^15.
// This gives a rigorous lower bound on every punctured quotient weight.
//
// Scope: H is supported on a fixed set of 15 points, so this samples only
// subcodes with at least 16 zero columns.  In particular every h in H has
// even weight at most 14, making the common-zero length exact.  A positive
// punctured-weight lower bound proves that the restriction kernel is
// exactly H; the program applies Griesmer only in that case.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <vector>

namespace {

constexpr int kPoints = 31;
constexpr int kSupport = 15;
constexpr int kEvenDimension = 30;
constexpr int kMaskCount = 1 << kSupport;

// External-middle Fourier values F(s)=sum_B (-1)^|B intersect S|.
constexpr std::array<std::int64_t, 32> kFourier = {
    17678835, 570285, -570285, -58995, 58995, 10925, -10925, -3059,
    3059, 1197, -1197, -627, 627, 429, -429, 1549,
    31219, 429, -429, -627, 627, 1197, -1197, -3059,
    3059, 10925, -10925, -58995, 58995, 570285, -570285, -17678835,
};

int Weight(std::uint32_t value) {
  return __builtin_popcount(value);
}

std::vector<std::uint32_t> RowBasis(
    const std::vector<std::uint32_t>& rows) {
  std::array<std::uint32_t, kSupport> pivots{};
  for (std::uint32_t row : rows) {
    for (int bit = kSupport - 1; bit >= 0 && row != 0; --bit) {
      if (((row >> bit) & 1U) == 0) continue;
      if (pivots[bit] != 0) {
        row ^= pivots[bit];
      } else {
        pivots[bit] = row;
        break;
      }
    }
  }
  std::vector<std::uint32_t> basis;
  for (int bit = 0; bit < kSupport; ++bit) {
    if (pivots[bit] != 0) basis.push_back(pivots[bit]);
  }
  return basis;
}

std::vector<std::uint32_t> Span(
    const std::vector<std::uint32_t>& basis) {
  std::vector<std::uint32_t> words{0};
  for (std::uint32_t row : basis) {
    const std::size_t old_size = words.size();
    for (std::size_t i = 0; i < old_size; ++i) {
      words.push_back(words[i] ^ row);
    }
  }
  std::sort(words.begin(), words.end());
  return words;
}

std::int64_t Griesmer(std::int64_t distance, int dimension) {
  std::int64_t answer = 0;
  for (int i = 0; i < dimension; ++i) {
    const std::int64_t denominator = std::int64_t{1} << i;
    answer += (distance + denominator - 1) / denominator;
  }
  return answer;
}

struct Result {
  std::int64_t length = 0;
  std::int64_t distance_lower_bound = 0;
  std::int64_t griesmer = 0;
  std::int64_t slack = std::numeric_limits<std::int64_t>::max();
  bool rank_proved = false;
};

Result Evaluate(const std::vector<std::uint32_t>& basis) {
  const auto subgroup = Span(basis);
  const int subgroup_size = static_cast<int>(subgroup.size());
  std::int64_t subgroup_sum = 0;
  for (std::uint32_t word : subgroup) {
    if ((Weight(word) & 1) != 0 || Weight(word) > 14) std::abort();
    subgroup_sum += kFourier[Weight(word)];
  }
  if (subgroup_sum % subgroup_size != 0) std::abort();
  const std::int64_t length = subgroup_sum / subgroup_size;

  std::array<std::uint16_t, kMaskCount> seen{};
  std::int64_t minimum = std::numeric_limits<std::int64_t>::max();
  for (std::uint32_t representative = 0;
       representative < kMaskCount; ++representative) {
    if (seen[representative]) continue;
    std::array<int, kSupport + 1> enumerator{};
    for (std::uint32_t word : subgroup) {
      const std::uint32_t member = representative ^ word;
      seen[member] = 1;
      ++enumerator[Weight(member)];
    }

    const int parity = Weight(representative) & 1;
    for (int outside = parity; outside <= kPoints - kSupport;
         outside += 2) {
      if (representative == 0 && outside == 0) continue;
      std::int64_t translated_sum = 0;
      for (int inside = 0; inside <= kSupport; ++inside) {
        translated_sum +=
            std::int64_t{enumerator[inside]} *
            kFourier[inside + outside];
      }
      const std::int64_t numerator = subgroup_sum - translated_sum;
      const std::int64_t denominator = 2LL * subgroup_size;
      if (numerator % denominator != 0) std::abort();
      minimum = std::min(minimum, numerator / denominator);
    }
  }

  const int quotient_dimension =
      kEvenDimension - static_cast<int>(basis.size());
  if (minimum <= 0) {
    return Result{length, minimum, 0,
                  std::numeric_limits<std::int64_t>::max(), false};
  }
  // Every even point subset outside H was covered by one inside coset and
  // one admissible outside weight.  Positivity therefore proves that no
  // further word lies in the restriction kernel.
  const std::int64_t bound = Griesmer(minimum, quotient_dimension);
  return Result{length, minimum, bound, length - bound, true};
}

void PrintCandidate(int dimension, const std::vector<std::uint32_t>& basis,
                    const Result& result) {
  std::cout << "m=" << dimension
            << " length=" << result.length
            << " d_lower=" << result.distance_lower_bound
            << " rank_proved=" << result.rank_proved;
  if (result.rank_proved) {
    std::cout << " griesmer=" << result.griesmer
              << " slack=" << result.slack;
  }
  std::cout
            << " basis=";
  for (std::uint32_t row : basis) {
    std::cout << std::hex << row << ",";
  }
  std::cout << std::dec << "\n";
}

}  // namespace

int main(int argc, char** argv) {
  int trials = 1000;
  if (argc == 2) trials = std::stoi(argv[1]);
  std::mt19937_64 generator(0x835141531ULL);
  std::uniform_int_distribution<std::uint32_t> mask_distribution(
      1, kMaskCount - 1);

  for (int dimension = 4; dimension <= 14; ++dimension) {
    Result best;
    Result best_unproved;
    best_unproved.distance_lower_bound =
        std::numeric_limits<std::int64_t>::min();
    std::vector<std::uint32_t> best_basis;
    std::vector<std::uint32_t> best_unproved_basis;
    for (int trial = 0; trial < trials; ++trial) {
      std::vector<std::uint32_t> rows;
      while (static_cast<int>(rows.size()) < dimension) {
        std::uint32_t row = mask_distribution(generator);
        if ((Weight(row) & 1) == 0) rows.push_back(row);
      }
      auto basis = RowBasis(rows);
      if (static_cast<int>(basis.size()) != dimension) {
        --trial;
        continue;
      }
      const Result result = Evaluate(basis);
      if (result.rank_proved && result.slack < best.slack) {
        best = result;
        best_basis = basis;
      }
      if (!result.rank_proved &&
          result.distance_lower_bound >
              best_unproved.distance_lower_bound) {
        best_unproved = result;
        best_unproved_basis = basis;
      }
      if (result.rank_proved && result.slack < 0) {
        PrintCandidate(dimension, basis, result);
        return 0;
      }
    }
    if (!best_basis.empty()) {
      PrintCandidate(dimension, best_basis, best);
    } else {
      PrintCandidate(dimension, best_unproved_basis, best_unproved);
    }
  }
  std::cout << "No negative Griesmer slack found in deterministic random search.\n";
}
