// Exact global search for a K18 in the quotient
//
//   (e1,e2,e3,e4,e8+e1^8)
//
// over 16-subsets of F_32.  The low-coordinate ratio lemma reduces every
// clique of size at least four to a top family (deletions from formal
// 17-set prefix Q) or a star family (extensions of formal 15-set prefix Q).
// Scaling and Frobenius leave 6,778 prefix orbits.  A meet-in-the-middle
// enumeration builds the exact actual-edge graph for each family and an
// exact colour-bound branch-and-bound routine tests for K18.  The search
// finds the three-mask star certificate checked independently by
// f32_five_statistic_k18_verifier.py.

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <limits>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int kFieldSize = 32;
constexpr int kDegree = 8;
constexpr int kVertices = 1024;
constexpr int kWords = kVertices / 64;
constexpr std::uint16_t kModulus = 0b100101;  // X^5 + X^2 + 1.

using Coefficients = std::array<std::uint8_t, kDegree + 1>;
using Bits = std::array<std::uint64_t, kWords>;
using Adjacency = std::array<Bits, kVertices>;

std::array<std::array<std::uint8_t, kFieldSize>, kFieldSize> product{};
std::array<std::array<std::uint8_t, kDegree + 1>, kFieldSize> powers{};

std::uint8_t multiply(std::uint8_t left, std::uint8_t right) {
  std::uint16_t raw = 0;
  for (int bit = 0; bit < 5; ++bit) {
    if ((right >> bit) & 1) {
      raw ^= static_cast<std::uint16_t>(left) << bit;
    }
  }
  for (int degree = 8; degree >= 5; --degree) {
    if ((raw >> degree) & 1) {
      raw ^= kModulus << (degree - 5);
    }
  }
  return static_cast<std::uint8_t>(raw);
}

std::uint8_t power(std::uint8_t value, int exponent) {
  std::uint8_t answer = 1;
  while (exponent != 0) {
    if (exponent & 1) {
      answer = product[answer][value];
    }
    value = product[value][value];
    exponent >>= 1;
  }
  return answer;
}

struct HalfEntry {
  std::uint8_t size = 0;
  Coefficients coefficients{};
  std::uint32_t mask = 0;
};

std::vector<HalfEntry> make_half_entries(int first_point) {
  std::vector<HalfEntry> answer(1 << 16);
  answer[0].coefficients[0] = 1;
  for (std::uint32_t mask = 1; mask < (1U << 16); ++mask) {
    const std::uint32_t bit = mask & -mask;
    const int local_point = std::countr_zero(bit);
    const int previous = mask ^ bit;
    answer[mask] = answer[previous];
    ++answer[mask].size;
    const std::uint8_t point =
        static_cast<std::uint8_t>(first_point + local_point);
    for (int degree = kDegree; degree >= 1; --degree) {
      answer[mask].coefficients[degree] ^=
          product[point][answer[mask].coefficients[degree - 1]];
    }
    answer[mask].mask |= 1U << point;
  }
  return answer;
}

std::uint32_t prefix_key(
    int size, const std::array<std::uint8_t, 5>& coefficients) {
  std::uint32_t answer = static_cast<std::uint32_t>(size);
  for (int degree = 1; degree <= 4; ++degree) {
    answer |= static_cast<std::uint32_t>(coefficients[degree])
              << (5 * degree);
  }
  return answer;
}

std::uint32_t pack_prefix(const std::array<std::uint8_t, 5>& prefix) {
  std::uint32_t answer = 0;
  for (int degree = 1; degree <= 4; ++degree) {
    answer |= static_cast<std::uint32_t>(prefix[degree])
              << (5 * (degree - 1));
  }
  return answer;
}

std::array<std::uint8_t, 5> unpack_prefix(std::uint32_t code) {
  std::array<std::uint8_t, 5> answer{};
  answer[0] = 1;
  for (int degree = 1; degree <= 4; ++degree) {
    answer[degree] = static_cast<std::uint8_t>(
        (code >> (5 * (degree - 1))) & 31);
  }
  return answer;
}

std::array<std::uint8_t, 5> needed_right_prefix(
    const std::array<std::uint8_t, 5>& target,
    const Coefficients& left) {
  std::array<std::uint8_t, 5> right{};
  right[0] = 1;
  for (int degree = 1; degree <= 4; ++degree) {
    std::uint8_t value = target[degree];
    for (int left_degree = 1; left_degree <= degree; ++left_degree) {
      value ^= product[left[left_degree]][right[degree - left_degree]];
    }
    right[degree] = value;
  }
  return right;
}

Coefficients combine(
    const Coefficients& left, const Coefficients& right) {
  Coefficients answer{};
  for (int degree = 0; degree <= kDegree; ++degree) {
    for (int left_degree = 0; left_degree <= degree; ++left_degree) {
      answer[degree] ^=
          product[left[left_degree]][right[degree - left_degree]];
    }
  }
  return answer;
}

void set_edge(Adjacency& adjacency, int left, int right) {
  if (left == right) {
    std::cerr << "unexpected quotient loop\n";
    std::exit(2);
  }
  adjacency[left][right >> 6] |= 1ULL << (right & 63);
  adjacency[right][left >> 6] |= 1ULL << (left & 63);
}

bool empty(const Bits& bits) {
  for (std::uint64_t word : bits) {
    if (word != 0) {
      return false;
    }
  }
  return true;
}

int pop_first(Bits& bits) {
  for (int word = 0; word < kWords; ++word) {
    if (bits[word] != 0) {
      const int offset = std::countr_zero(bits[word]);
      bits[word] &= bits[word] - 1;
      return 64 * word + offset;
    }
  }
  return -1;
}

void remove_vertex(Bits& bits, int vertex) {
  bits[vertex >> 6] &= ~(1ULL << (vertex & 63));
}

Bits intersection(const Bits& left, const Bits& right) {
  Bits answer{};
  for (int word = 0; word < kWords; ++word) {
    answer[word] = left[word] & right[word];
  }
  return answer;
}

struct CliqueDecision {
  const Adjacency& adjacency;
  int target = 18;
  std::uint64_t nodes = 0;
  std::vector<int> witness;

  CliqueDecision(const Adjacency& graph, int requested_target)
      : adjacency(graph), target(requested_target) {}

  bool expand(int size, Bits candidates, std::vector<int>& chosen) {
    ++nodes;
    std::vector<int> order;
    std::vector<int> bounds;
    order.reserve(kVertices);
    bounds.reserve(kVertices);

    Bits uncoloured = candidates;
    int colour = 0;
    while (!empty(uncoloured)) {
      ++colour;
      Bits available = uncoloured;
      while (!empty(available)) {
        const int vertex = pop_first(available);
        order.push_back(vertex);
        bounds.push_back(colour);
        remove_vertex(uncoloured, vertex);
        for (int word = 0; word < kWords; ++word) {
          available[word] &= ~adjacency[vertex][word];
        }
      }
    }

    for (int index = static_cast<int>(order.size()) - 1; index >= 0;
         --index) {
      if (size + bounds[index] < target) {
        return false;
      }
      const int vertex = order[index];
      if (((candidates[vertex >> 6] >> (vertex & 63)) & 1) == 0) {
        continue;
      }
      chosen.push_back(vertex);
      if (size + 1 == target) {
        witness = chosen;
        return true;
      }
      Bits next = intersection(candidates, adjacency[vertex]);
      if (!empty(next) && expand(size + 1, next, chosen)) {
        return true;
      }
      chosen.pop_back();
      remove_vertex(candidates, vertex);
    }
    return false;
  }

  bool find(const Bits& vertices) {
    std::vector<int> chosen;
    return expand(0, vertices, chosen);
  }
};

bool brute_force_has_clique(
    const Adjacency& adjacency, int number, int target) {
  for (std::uint64_t subset = 0; subset < (1ULL << number); ++subset) {
    if (std::popcount(subset) < target) {
      continue;
    }
    bool valid = true;
    std::uint64_t remaining = subset;
    while (remaining != 0) {
      const int vertex = std::countr_zero(remaining);
      remaining &= remaining - 1;
      const std::uint64_t others = subset & ~(1ULL << vertex);
      if ((adjacency[vertex][0] & others) != others) {
        valid = false;
        break;
      }
    }
    if (valid) {
      return true;
    }
  }
  return false;
}

void self_test_clique_decision() {
  const std::array<std::pair<int, int>, 10> edges = {{
      {0, 1}, {0, 2}, {0, 3}, {0, 4}, {1, 2},
      {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4},
  }};
  for (int graph_code = 0; graph_code < (1 << edges.size());
       ++graph_code) {
    Adjacency adjacency{};
    Bits vertices{};
    vertices[0] = 31;
    for (int edge_index = 0;
         edge_index < static_cast<int>(edges.size()); ++edge_index) {
      if ((graph_code >> edge_index) & 1) {
        set_edge(adjacency, edges[edge_index].first,
                 edges[edge_index].second);
      }
    }
    for (int target = 1; target <= 6; ++target) {
      CliqueDecision decision{adjacency, target};
      const bool found = decision.find(vertices);
      const bool expected =
          brute_force_has_clique(adjacency, 5, target);
      if (found != expected) {
        std::cerr << "clique decision self-test failed\n";
        std::exit(2);
      }
    }
  }
}

struct FamilyResult {
  std::uint64_t blocks = 0;
  std::uint64_t edges = 0;
  std::uint64_t clique_nodes = 0;
  std::vector<int> clique;
  std::array<std::uint32_t, 18 * 18> requested_witnesses{};
};

FamilyResult build_and_search_family(
    const std::array<std::uint8_t, 5>& target,
    bool top_family,
    const std::vector<HalfEntry>& left_entries,
    const std::vector<HalfEntry>& right_entries,
    const std::unordered_map<std::uint32_t, std::vector<std::uint16_t>>&
        right_index,
    const std::vector<int>* requested_clique = nullptr) {
  Adjacency adjacency{};
  Bits vertices{};
  FamilyResult result;
  const int base_size = top_family ? 17 : 15;
  std::array<int, kVertices> requested_positions{};
  requested_positions.fill(-1);
  if (requested_clique != nullptr) {
    if (requested_clique->size() != 18) {
      std::cerr << "requested witness clique has wrong size\n";
      std::exit(2);
    }
    for (int index = 0; index < 18; ++index) {
      requested_positions[(*requested_clique)[index]] = index;
    }
  }

  for (const HalfEntry& left : left_entries) {
    const int right_size = base_size - left.size;
    if (right_size < 0 || right_size > 16) {
      continue;
    }
    const auto right_prefix =
        needed_right_prefix(target, left.coefficients);
    const auto found =
        right_index.find(prefix_key(right_size, right_prefix));
    if (found == right_index.end()) {
      continue;
    }
    for (std::uint16_t right_index_value : found->second) {
      const HalfEntry& right = right_entries[right_index_value];
      const Coefficients rho =
          combine(left.coefficients, right.coefficients);
      for (int degree = 1; degree <= 4; ++degree) {
        if (rho[degree] != target[degree]) {
          std::cerr << "MITM prefix mismatch\n";
          std::exit(2);
        }
      }
      const std::uint32_t mask = left.mask | right.mask;
      if (std::popcount(mask) != base_size) {
        std::cerr << "MITM size mismatch\n";
        std::exit(2);
      }
      ++result.blocks;
      std::array<int, 17> block_vertices{};
      int count = 0;
      std::uint32_t remaining =
          top_family ? mask : ~mask;
      while (remaining != 0) {
        const int point = std::countr_zero(remaining);
        remaining &= remaining - 1;
        Coefficients half_set{};
        half_set[0] = 1;
        if (top_family) {
          for (int degree = 1; degree <= kDegree; ++degree) {
            half_set[degree] =
                rho[degree] ^
                product[point][half_set[degree - 1]];
          }
        } else {
          for (int degree = 1; degree <= kDegree; ++degree) {
            half_set[degree] =
                rho[degree] ^
                product[point][rho[degree - 1]];
          }
        }
        const std::uint8_t first = half_set[1];
        const std::uint8_t lam =
            half_set[8] ^ powers[first][8];
        const int vertex = 32 * point + lam;
        block_vertices[count++] = vertex;
        vertices[vertex >> 6] |= 1ULL << (vertex & 63);
      }
      if (count != 17) {
        std::cerr << "block deletion count mismatch\n";
        std::exit(2);
      }
      for (int left_index = 0; left_index < 17; ++left_index) {
        for (int right_index_value = left_index + 1;
             right_index_value < 17; ++right_index_value) {
          set_edge(adjacency, block_vertices[left_index],
                   block_vertices[right_index_value]);
          if (requested_clique != nullptr) {
            int first =
                requested_positions[block_vertices[left_index]];
            int second =
                requested_positions[block_vertices[right_index_value]];
            if (first >= 0 && second >= 0) {
              if (first > second) {
                std::swap(first, second);
              }
              result.requested_witnesses[18 * first + second] = mask;
            }
          }
        }
      }
    }
  }

  for (int vertex = 0; vertex < kVertices; ++vertex) {
    for (std::uint64_t word : adjacency[vertex]) {
      result.edges += std::popcount(word);
    }
  }
  result.edges /= 2;

  CliqueDecision decision{adjacency, 18};
  if (decision.find(vertices)) {
    result.clique = decision.witness;
  }
  result.clique_nodes = decision.nodes;
  if (requested_clique != nullptr) {
    for (int left = 0; left < 18; ++left) {
      for (int right = left + 1; right < 18; ++right) {
        if (result.requested_witnesses[18 * left + right] == 0) {
          std::cerr << "missing requested edge witness\n";
          std::exit(2);
        }
      }
    }
  }
  return result;
}

std::vector<std::uint32_t> semilinear_representatives() {
  constexpr std::uint32_t count = 1U << 20;
  std::vector<bool> seen(count, false);
  std::vector<std::uint32_t> answer;
  for (std::uint32_t code = 0; code < count; ++code) {
    if (seen[code]) {
      continue;
    }
    answer.push_back(code);
    const auto prefix = unpack_prefix(code);
    for (int frobenius = 0; frobenius < 5; ++frobenius) {
      for (std::uint8_t scale = 1; scale < 32; ++scale) {
        std::array<std::uint8_t, 5> transformed{};
        transformed[0] = 1;
        for (int degree = 1; degree <= 4; ++degree) {
          std::uint8_t value = prefix[degree];
          for (int iteration = 0; iteration < frobenius; ++iteration) {
            value = product[value][value];
          }
          transformed[degree] =
              product[value][power(scale, degree)];
        }
        seen[pack_prefix(transformed)] = true;
      }
    }
  }
  return answer;
}

void initialise_field() {
  for (int left = 0; left < 32; ++left) {
    for (int right = 0; right < 32; ++right) {
      product[left][right] =
          multiply(static_cast<std::uint8_t>(left),
                   static_cast<std::uint8_t>(right));
    }
  }
  for (int value = 0; value < 32; ++value) {
    powers[value][0] = 1;
    for (int exponent = 1; exponent <= kDegree; ++exponent) {
      powers[value][exponent] =
          product[powers[value][exponent - 1]][value];
    }
  }
  for (int value = 1; value < 32; ++value) {
    if (power(static_cast<std::uint8_t>(value), 31) != 1) {
      std::cerr << "field inverse check failed\n";
      std::exit(2);
    }
  }
}

}  // namespace

int main(int argc, char** argv) {
  initialise_field();
  self_test_clique_decision();
  const auto left_entries = make_half_entries(0);
  const auto right_entries = make_half_entries(16);

  std::unordered_map<std::uint32_t, std::vector<std::uint16_t>>
      right_index;
  right_index.reserve(1 << 17);
  for (std::uint32_t index = 0; index < right_entries.size(); ++index) {
    const HalfEntry& entry = right_entries[index];
    std::array<std::uint8_t, 5> prefix{};
    prefix[0] = 1;
    for (int degree = 1; degree <= 4; ++degree) {
      prefix[degree] = entry.coefficients[degree];
    }
    right_index[prefix_key(entry.size, prefix)].push_back(
        static_cast<std::uint16_t>(index));
  }

  const std::vector<std::uint32_t> representatives =
      semilinear_representatives();
  std::cout << "semilinear prefix orbits: " << representatives.size()
            << "\n";

  if (argc == 6 && std::string(argv[1]) == "--raw") {
    std::array<std::uint8_t, 5> prefix{};
    prefix[0] = 1;
    for (int degree = 1; degree <= 4; ++degree) {
      const int value = std::stoi(argv[degree + 1]);
      if (value < 0 || value >= 32) {
        std::cerr << "raw prefix coordinates must lie in [0,31]\n";
        return 2;
      }
      prefix[degree] = static_cast<std::uint8_t>(value);
    }
    for (bool top_family : {true, false}) {
      const FamilyResult result = build_and_search_family(
          prefix, top_family, left_entries, right_entries, right_index);
      std::cout << (top_family ? "top" : "star") << "_raw_prefix=("
                << static_cast<int>(prefix[1]) << ","
                << static_cast<int>(prefix[2]) << ","
                << static_cast<int>(prefix[3]) << ","
                << static_cast<int>(prefix[4]) << ") blocks="
                << result.blocks << " edges=" << result.edges
                << " clique_nodes=" << result.clique_nodes
                << " has_K18=" << !result.clique.empty() << "\n";
      if (!result.clique.empty()) {
        return 1;
      }
    }
    return 0;
  }

  std::size_t first = 0;
  std::size_t last = representatives.size();
  if (argc == 2) {
    first = static_cast<std::size_t>(std::stoull(argv[1]));
    last = std::min(first + 1, representatives.size());
  } else if (argc == 3) {
    first = static_cast<std::size_t>(std::stoull(argv[1]));
    last = std::min(
        static_cast<std::size_t>(std::stoull(argv[2])),
        representatives.size());
  }
  if (first > last || first >= representatives.size()) {
    std::cerr << "invalid representative range\n";
    return 2;
  }

  std::uint64_t total_blocks = 0;
  std::uint64_t total_edges = 0;
  std::uint64_t total_nodes = 0;
  std::uint64_t maximum_edges = 0;
  std::uint64_t maximum_nodes = 0;
  for (std::size_t index = first; index < last; ++index) {
    const auto prefix = unpack_prefix(representatives[index]);
    for (bool top_family : {true, false}) {
      FamilyResult result = build_and_search_family(
          prefix, top_family, left_entries, right_entries, right_index);
      total_blocks += result.blocks;
      total_edges += result.edges;
      total_nodes += result.clique_nodes;
      maximum_edges = std::max(maximum_edges, result.edges);
      maximum_nodes = std::max(maximum_nodes, result.clique_nodes);
      if (!result.clique.empty()) {
        std::cout << "K18 FOUND family="
                  << (top_family ? "top" : "star")
                  << " orbit=" << index << " prefix=("
                  << static_cast<int>(prefix[1]) << ","
                  << static_cast<int>(prefix[2]) << ","
                  << static_cast<int>(prefix[3]) << ","
                  << static_cast<int>(prefix[4]) << ") vertices=";
        for (int vertex : result.clique) {
          std::cout << "(" << vertex / 32 << "," << vertex % 32
                    << ")";
        }
        std::cout << "\n";
        const FamilyResult certified = build_and_search_family(
            prefix, top_family, left_entries, right_entries, right_index,
            &result.clique);
        std::cout << "WITNESS_MASK_ROWS = (\n";
        for (int left = 0; left < 18; ++left) {
          std::cout << "    (";
          for (int right = left + 1; right < 18; ++right) {
            std::cout << "0x" << std::hex << std::uppercase
                      << std::setw(8) << std::setfill('0')
                      << certified.requested_witnesses[18 * left + right]
                      << std::dec << ",";
            if (right + 1 < 18) {
              std::cout << " ";
            }
          }
          std::cout << "),\n";
        }
        std::cout << ")\n";
        return 1;
      }
    }
    if ((index - first + 1) % 100 == 0 || index + 1 == last) {
      std::cout << "checked=" << (index - first + 1)
                << " through_orbit=" << index
                << " total_blocks=" << total_blocks
                << " max_edges=" << maximum_edges
                << " max_clique_nodes=" << maximum_nodes << "\n";
    }
  }

  std::cout << "NO K18 in checked top and star families"
            << " first=" << first << " last=" << last
            << " total_blocks=" << total_blocks
            << " total_edges=" << total_edges
            << " total_clique_nodes=" << total_nodes
            << " max_edges=" << maximum_edges
            << " max_clique_nodes=" << maximum_nodes << "\n";
  return 0;
}
