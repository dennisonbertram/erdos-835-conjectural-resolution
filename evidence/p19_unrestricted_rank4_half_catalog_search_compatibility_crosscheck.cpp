#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <mutex>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <utility>
#include <vector>

// Independent cross-check of the exact Schur search over all 396 isomorphism
// classes of one-factorizations of K_10.  For a fixed
// factor-to-magnitude bijection and a fixed four-vertex anchor, the remaining
// edge signs are solved exactly by a precomputed compatibility-mask CSP.
//
// If H is a nonsingular 4x4 principal block and X contains the entries from
// the anchor to the other six vertices, rank(A)=4 is equivalent to
//
//       D = -X^T H^{-1} X.
//
// Vertex switching lets us make the three entries from the first anchor
// vertex to the other anchors positive, and independently make the first
// coordinate of each column of X positive.  Only 2^3 anchor sign patterns and
// 2^3 states per outside vertex remain.  Pairwise compatibility of the six
// outside states is then an exact 6-partite clique problem.
//
// This variant deliberately differs from the primary implementation:
// compatibility is represented by lazily computed eight-bit state masks, then
// a minimum-remaining-values recursion propagates those domains.
// Exact-anchor mode enumerates all 396*8! jobs; heuristic mode remains
// available only for exploratory runs.

static constexpr int P = 19;
static constexpr int N = 10;
static constexpr int FACTORS = 9;
static constexpr int EDGES = 45;
static constexpr int STATES = 8;

using Matrix4 = std::array<std::array<int, 4>, 4>;
using Matrix10 = std::array<std::array<int, N>, N>;

struct Factorization {
    std::array<int, EDGES> edge_factor{};
};

struct Anchor {
    std::array<int, 4> inside{};
    std::array<int, 6> outside{};
    std::array<std::array<int, 4>, 4> inside_edges{};
    std::array<std::array<int, 6>, 4> cross_edges{};
    std::array<std::array<int, 6>, 6> outside_edges{};
};

struct Witness {
    int case_number = -1;
    std::array<int, FACTORS> magnitudes{};
    Anchor anchor{};
    int anchor_sign_pattern = 0;
    std::array<int, 6> outside_states{};
    Matrix10 matrix{};
};

static int mod(int value) {
    value %= P;
    return value < 0 ? value + P : value;
}

static int inverse_scalar(int value) {
    int answer = 1;
    int exponent = P - 2;
    value = mod(value);
    while (exponent) {
        if (exponent & 1) answer = mod(answer * value);
        value = mod(value * value);
        exponent >>= 1;
    }
    return answer;
}

static int sign_class(int value) {
    value = mod(value);
    return std::min(value, P - value);
}

static int edge_index(int left, int right) {
    if (left > right) std::swap(left, right);
    int index = 0;
    for (int first = 0; first < left; ++first) {
        index += N - first - 1;
    }
    return index + right - left - 1;
}

static bool invert_matrix(Matrix4 input, Matrix4& output) {
    output = {};
    for (int row = 0; row < 4; ++row) output[row][row] = 1;
    for (int column = 0; column < 4; ++column) {
        int pivot = column;
        while (pivot < 4 && input[pivot][column] == 0) ++pivot;
        if (pivot == 4) return false;
        std::swap(input[pivot], input[column]);
        std::swap(output[pivot], output[column]);
        const int scale = inverse_scalar(input[column][column]);
        for (int entry = 0; entry < 4; ++entry) {
            input[column][entry] = mod(input[column][entry] * scale);
            output[column][entry] = mod(output[column][entry] * scale);
        }
        for (int row = 0; row < 4; ++row) {
            if (row == column || input[row][column] == 0) continue;
            const int multiplier = input[row][column];
            for (int entry = 0; entry < 4; ++entry) {
                input[row][entry] =
                    mod(input[row][entry] - multiplier * input[column][entry]);
                output[row][entry] =
                    mod(output[row][entry] - multiplier * output[column][entry]);
            }
        }
    }
    return true;
}

static std::array<int, 4> matrix_vector(
    const Matrix4& matrix,
    const std::array<int, 4>& vector
) {
    std::array<int, 4> result{};
    for (int row = 0; row < 4; ++row) {
        int sum = 0;
        for (int column = 0; column < 4; ++column) {
            sum += matrix[row][column] * vector[column];
        }
        result[row] = sum % P;
    }
    return result;
}

static int dot_product(
    const std::array<int, 4>& left,
    const std::array<int, 4>& right
) {
    int sum = 0;
    for (int coordinate = 0; coordinate < 4; ++coordinate) {
        sum += left[coordinate] * right[coordinate];
    }
    return sum % P;
}

static std::vector<Anchor> all_anchors() {
    std::vector<Anchor> anchors;
    for (int a = 0; a < N; ++a) {
        for (int b = a + 1; b < N; ++b) {
            for (int c = b + 1; c < N; ++c) {
                for (int d = c + 1; d < N; ++d) {
                    Anchor anchor;
                    anchor.inside = {a, b, c, d};
                    int next = 0;
                    for (int vertex = 0; vertex < N; ++vertex) {
                        if (vertex != a && vertex != b
                            && vertex != c && vertex != d) {
                            anchor.outside[next++] = vertex;
                        }
                    }
                    for (int left = 0; left < 4; ++left) {
                        for (int right = left + 1; right < 4; ++right) {
                            anchor.inside_edges[left][right] = edge_index(
                                anchor.inside[left], anchor.inside[right]
                            );
                        }
                        for (int outside = 0; outside < 6; ++outside) {
                            anchor.cross_edges[left][outside] = edge_index(
                                anchor.inside[left], anchor.outside[outside]
                            );
                        }
                    }
                    for (int left = 0; left < 6; ++left) {
                        for (int right = left + 1; right < 6; ++right) {
                            anchor.outside_edges[left][right] = edge_index(
                                anchor.outside[left], anchor.outside[right]
                            );
                        }
                    }
                    anchors.push_back(anchor);
                }
            }
        }
    }
    return anchors;
}

static std::vector<Factorization> read_catalogue(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open catalogue: " + path);
    std::vector<Factorization> result;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == '#') continue;
        const std::size_t tab = line.find('\t');
        if (tab == std::string::npos) {
            throw std::runtime_error("catalogue line has no tab");
        }
        Factorization factorization;
        factorization.edge_factor.fill(-1);
        std::stringstream factors(line.substr(tab + 1));
        std::string factor_text;
        int factor = 0;
        while (std::getline(factors, factor_text, ';')) {
            if (factor >= FACTORS) {
                throw std::runtime_error("too many factors");
            }
            std::stringstream edges(factor_text);
            std::string edge_text;
            int edge_count = 0;
            while (std::getline(edges, edge_text, ',')) {
                if (edge_text.size() != 2
                    || edge_text[0] < '0' || edge_text[0] > '9'
                    || edge_text[1] < '0' || edge_text[1] > '9') {
                    throw std::runtime_error("bad edge encoding");
                }
                const int left = edge_text[0] - '0';
                const int right = edge_text[1] - '0';
                const int index = edge_index(left, right);
                if (left >= right || factorization.edge_factor[index] != -1) {
                    throw std::runtime_error("repeated or reversed edge");
                }
                factorization.edge_factor[index] = factor;
                ++edge_count;
            }
            if (edge_count != 5) {
                throw std::runtime_error("factor does not have five edges");
            }
            ++factor;
        }
        if (factor != FACTORS
            || std::find(
                factorization.edge_factor.begin(),
                factorization.edge_factor.end(),
                -1
            ) != factorization.edge_factor.end()) {
            throw std::runtime_error("incomplete factorization");
        }
        result.push_back(factorization);
    }
    if (result.size() != 396) {
        throw std::runtime_error("expected 396 factorizations");
    }
    return result;
}

static int edge_magnitude(
    const Factorization& factorization,
    const std::array<int, FACTORS>& magnitudes,
    int left,
    int right
) {
    return magnitudes[factorization.edge_factor[edge_index(left, right)]];
}

using StateVectors =
    std::array<std::array<std::array<int, 4>, STATES>, 6>;

static int state_count(std::uint8_t mask) {
    return __builtin_popcount(static_cast<unsigned int>(mask));
}

static int first_state(std::uint8_t mask) {
    return __builtin_ctz(static_cast<unsigned int>(mask));
}

static std::uint8_t compatible_state_mask(
    int fixed_vertex,
    int fixed_state,
    int free_vertex,
    const StateVectors& x,
    const StateVectors& transformed,
    const std::array<std::array<int, 6>, 6>& required
) {
    std::uint8_t mask = 0;
    const int left = std::min(fixed_vertex, free_vertex);
    const int right = std::max(fixed_vertex, free_vertex);
    for (int free_state = 0; free_state < STATES; ++free_state) {
        const int left_state =
            left == fixed_vertex ? fixed_state : free_state;
        const int right_state =
            right == fixed_vertex ? fixed_state : free_state;
        const int predicted = mod(-dot_product(
            x[left][left_state],
            transformed[right][right_state]
        ));
        if (sign_class(predicted) == required[left][right]) {
            mask = static_cast<std::uint8_t>(
                mask | static_cast<std::uint8_t>(1U << free_state)
            );
        }
    }
    return mask;
}

static bool solve_outside_mask_csp(
    int assigned_count,
    const StateVectors& x,
    const StateVectors& transformed,
    const std::array<std::array<int, 6>, 6>& required,
    std::array<std::uint8_t, 6> domains,
    std::array<int, 6>& assignment
) {
    if (assigned_count == 6) return true;

    int vertex = -1;
    int best_count = STATES + 1;
    for (int candidate = 0; candidate < 6; ++candidate) {
        if (assignment[candidate] != -1) continue;
        const int count = state_count(domains[candidate]);
        if (count == 0) return false;
        if (count < best_count) {
            vertex = candidate;
            best_count = count;
        }
    }

    std::uint8_t choices = domains[vertex];
    while (choices != 0) {
        const int state = first_state(choices);
        choices = static_cast<std::uint8_t>(
            choices & static_cast<std::uint8_t>(choices - 1)
        );
        assignment[vertex] = state;
        auto next_domains = domains;
        next_domains[vertex] =
            static_cast<std::uint8_t>(1U << state);
        bool consistent = true;
        for (int other = 0; other < 6; ++other) {
            if (assignment[other] != -1) continue;
            next_domains[other] = static_cast<std::uint8_t>(
                next_domains[other]
                & compatible_state_mask(
                    vertex,
                    state,
                    other,
                    x,
                    transformed,
                    required
                )
            );
            if (next_domains[other] == 0) {
                consistent = false;
                break;
            }
        }
        if (consistent && solve_outside_mask_csp(
                assigned_count + 1,
                x,
                transformed,
                required,
                next_domains,
                assignment
            )) {
            return true;
        }
        assignment[vertex] = -1;
    }
    return false;
}

static int rank_mod(Matrix10 matrix) {
    int rank = 0;
    for (int column = 0; column < N; ++column) {
        int pivot = rank;
        while (pivot < N && matrix[pivot][column] == 0) ++pivot;
        if (pivot == N) continue;
        std::swap(matrix[pivot], matrix[rank]);
        const int scale = inverse_scalar(matrix[rank][column]);
        for (int entry = 0; entry < N; ++entry) {
            matrix[rank][entry] = mod(matrix[rank][entry] * scale);
        }
        for (int row = 0; row < N; ++row) {
            if (row == rank || matrix[row][column] == 0) continue;
            const int multiplier = matrix[row][column];
            for (int entry = 0; entry < N; ++entry) {
                matrix[row][entry] =
                    mod(matrix[row][entry] - multiplier * matrix[rank][entry]);
            }
        }
        ++rank;
    }
    return rank;
}

static bool verify_witness(
    const Factorization& factorization,
    const Witness& witness
) {
    if (rank_mod(witness.matrix) > 4) return false;
    for (int left = 0; left < N; ++left) {
        if (witness.matrix[left][left] != 0) return false;
        std::array<bool, 10> seen{};
        for (int right = 0; right < N; ++right) {
            if (left == right) continue;
            if (mod(witness.matrix[left][right]
                    + witness.matrix[right][left]) != 0) {
                return false;
            }
            const int label = sign_class(witness.matrix[left][right]);
            const int expected = edge_magnitude(
                factorization, witness.magnitudes, left, right
            );
            if (label != expected || seen[label]) return false;
            seen[label] = true;
        }
        for (int label = 1; label <= 9; ++label) {
            if (!seen[label]) return false;
        }
    }
    return true;
}

static bool test_anchor(
    const Factorization& factorization,
    int case_number,
    const std::array<int, FACTORS>& magnitudes,
    const Anchor& anchor,
    Witness& witness
) {
    std::array<int, EDGES> edge_magnitudes{};
    for (int edge = 0; edge < EDGES; ++edge) {
        edge_magnitudes[edge] =
            magnitudes[factorization.edge_factor[edge]];
    }
    for (int anchor_pattern = 0; anchor_pattern < 8; ++anchor_pattern) {
        Matrix4 h{};
        for (int left = 0; left < 4; ++left) {
            for (int right = left + 1; right < 4; ++right) {
                int value =
                    edge_magnitudes[anchor.inside_edges[left][right]];
                if (left != 0) {
                    const int bit =
                        (left == 1 && right == 2) ? 0
                        : (left == 1 && right == 3) ? 1 : 2;
                    if (anchor_pattern & (1 << bit)) value = mod(-value);
                }
                h[left][right] = value;
                h[right][left] = mod(-value);
            }
        }
        Matrix4 h_inverse{};
        if (!invert_matrix(h, h_inverse)) continue;

        StateVectors x{};
        for (int outside = 0; outside < 6; ++outside) {
            for (int state = 0; state < STATES; ++state) {
                for (int coordinate = 0; coordinate < 4; ++coordinate) {
                    int value =
                        edge_magnitudes[anchor.cross_edges[coordinate][outside]];
                    if (coordinate > 0
                        && (state & (1 << (coordinate - 1)))) {
                        value = mod(-value);
                    }
                    x[outside][state][coordinate] = value;
                }
            }
        }
        StateVectors transformed{};
        for (int outside = 0; outside < 6; ++outside) {
            for (int state = 0; state < STATES; ++state) {
                transformed[outside][state] =
                    matrix_vector(h_inverse, x[outside][state]);
            }
        }

        std::array<std::array<int, 6>, 6> required{};
        for (int left = 0; left < 6; ++left) {
            for (int right = left + 1; right < 6; ++right) {
                required[left][right] =
                    edge_magnitudes[anchor.outside_edges[left][right]];
            }
        }

        std::array<int, 6> assignment{};
        assignment.fill(-1);
        std::array<std::uint8_t, 6> domains{};
        domains.fill(0xffU);
        if (!solve_outside_mask_csp(
                0, x, transformed, required, domains, assignment
            )) {
            continue;
        }

        witness = {};
        witness.case_number = case_number;
        witness.magnitudes = magnitudes;
        witness.anchor = anchor;
        witness.anchor_sign_pattern = anchor_pattern;
        witness.outside_states = assignment;
        for (int left = 0; left < 4; ++left) {
            for (int right = 0; right < 4; ++right) {
                witness.matrix[anchor.inside[left]][anchor.inside[right]] =
                    h[left][right];
            }
        }
        for (int outside = 0; outside < 6; ++outside) {
            const int vertex = anchor.outside[outside];
            const int state = assignment[outside];
            for (int coordinate = 0; coordinate < 4; ++coordinate) {
                const int inside = anchor.inside[coordinate];
                const int value = x[outside][state][coordinate];
                witness.matrix[inside][vertex] = value;
                witness.matrix[vertex][inside] = mod(-value);
            }
        }
        for (int left = 0; left < 6; ++left) {
            for (int right = left + 1; right < 6; ++right) {
                const int value = mod(-dot_product(
                    x[left][assignment[left]],
                    transformed[right][assignment[right]]
                ));
                witness.matrix[anchor.outside[left]][anchor.outside[right]] =
                    value;
                witness.matrix[anchor.outside[right]][anchor.outside[left]] =
                    mod(-value);
            }
        }
        if (!verify_witness(factorization, witness)) {
            throw std::runtime_error("internal witness verification failed");
        }
        return true;
    }
    return false;
}

static void print_witness(const Witness& witness) {
    std::cout << "WITNESS\n";
    std::cout << "catalogue_case=" << witness.case_number << "\n";
    std::cout << "factor_magnitudes=[";
    for (int factor = 0; factor < FACTORS; ++factor) {
        if (factor) std::cout << ",";
        std::cout << witness.magnitudes[factor];
    }
    std::cout << "]\nanchor=[";
    for (int index = 0; index < 4; ++index) {
        if (index) std::cout << ",";
        std::cout << witness.anchor.inside[index];
    }
    std::cout << "]\nA=[\n";
    for (const auto& row : witness.matrix) {
        std::cout << "  [";
        for (int column = 0; column < N; ++column) {
            if (column) std::cout << ",";
            std::cout << row[column];
        }
        std::cout << "],\n";
    }
    std::cout << "]\nrank=" << rank_mod(witness.matrix) << "\n";
    std::cout << "half_link_verification=PASS\n";
}

static std::array<int, FACTORS> unrank_magnitudes(std::uint64_t rank) {
    static constexpr std::array<std::uint64_t, 9> factorial{
        1, 1, 2, 6, 24, 120, 720, 5040, 40320
    };
    std::vector<int> available{2, 3, 4, 5, 6, 7, 8, 9};
    std::array<int, FACTORS> magnitudes{};
    magnitudes[0] = 1;
    for (int position = 0; position < 8; ++position) {
        const std::uint64_t block = factorial[7 - position];
        const std::size_t choice =
            static_cast<std::size_t>(rank / block);
        rank %= block;
        magnitudes[position + 1] = available[choice];
        available.erase(available.begin() + static_cast<std::ptrdiff_t>(choice));
    }
    return magnitudes;
}

int main(int argc, char** argv) {
    const std::string catalogue_path =
        argc > 1 ? argv[1] : "evidence/k10_one_factorizations_396.txt";
    const double seconds = argc > 2 ? std::atof(argv[2]) : 300.0;
    const int thread_count = argc > 3 ? std::atoi(argv[3]) : 4;
    const std::uint64_t seed = argc > 4
        ? std::strtoull(argv[4], nullptr, 10) : 190835ULL;
    const int exact_anchor_index = argc > 5 ? std::atoi(argv[5]) : -1;

    const auto factorizations = read_catalogue(catalogue_path);
    const auto anchors = all_anchors();
    if (exact_anchor_index >= static_cast<int>(anchors.size())) {
        throw std::runtime_error("exact anchor index is out of range");
    }
    std::atomic<bool> stop{false};
    std::atomic<std::uint64_t> trials{0};
    std::atomic<std::uint64_t> magnitude_assignments{0};
    std::mutex witness_mutex;
    Witness found;
    static constexpr std::uint64_t PERMUTATIONS = 40320;
    const std::uint64_t total_exact_jobs =
        static_cast<std::uint64_t>(factorizations.size()) * PERMUTATIONS;
    std::atomic<std::uint64_t> next_exact_job{0};
    const auto start = std::chrono::steady_clock::now();
    const auto elapsed = [&]() {
        return std::chrono::duration<double>(
            std::chrono::steady_clock::now() - start
        ).count();
    };

    std::vector<std::thread> threads;
    for (int thread_id = 0; thread_id < thread_count; ++thread_id) {
        threads.emplace_back([&, thread_id]() {
            std::mt19937_64 rng(
                seed + 0x9e3779b97f4a7c15ULL
                    * static_cast<std::uint64_t>(thread_id + 1)
            );
            std::array<int, FACTORS> magnitudes{};
            magnitudes[0] = 1;
            std::array<int, 8> tail{2, 3, 4, 5, 6, 7, 8, 9};
            while (!stop.load(std::memory_order_relaxed)
                   && elapsed() < seconds) {
                if (exact_anchor_index >= 0) {
                    const std::uint64_t job =
                        next_exact_job.fetch_add(1, std::memory_order_relaxed);
                    if (job >= total_exact_jobs) break;
                    const int case_index =
                        static_cast<int>(job / PERMUTATIONS);
                    magnitudes = unrank_magnitudes(job % PERMUTATIONS);
                    ++magnitude_assignments;
                    Witness candidate;
                    ++trials;
                    if (test_anchor(
                            factorizations[case_index], case_index + 1,
                            magnitudes, anchors[exact_anchor_index], candidate
                        )) {
                        {
                            std::lock_guard<std::mutex> lock(witness_mutex);
                            if (!stop.load(std::memory_order_relaxed)) {
                                found = candidate;
                            }
                        }
                        stop.store(true, std::memory_order_relaxed);
                        break;
                    }
                    continue;
                }

                const int case_index =
                    static_cast<int>(rng() % factorizations.size());
                std::shuffle(tail.begin(), tail.end(), rng);
                for (int index = 0; index < 8; ++index) {
                    magnitudes[index + 1] = tail[index];
                }
                ++magnitude_assignments;

                // Test a fresh random sample of anchors for this labelling.
                // Sixteen gives useful reuse of the magnitude assignment while
                // continuing to cover the 210 anchor positions broadly.
                for (int sample = 0; sample < 16; ++sample) {
                    const Anchor& anchor =
                        anchors[static_cast<std::size_t>(rng() % anchors.size())];
                    Witness candidate;
                    ++trials;
                    if (test_anchor(
                            factorizations[case_index], case_index + 1,
                            magnitudes, anchor, candidate
                        )) {
                        {
                            std::lock_guard<std::mutex> lock(witness_mutex);
                            if (!stop.load(std::memory_order_relaxed)) {
                                found = candidate;
                            }
                        }
                        stop.store(true, std::memory_order_relaxed);
                        break;
                    }
                }
            }
        });
    }
    for (auto& thread : threads) thread.join();

    std::cout << "catalogue_factorizations=" << factorizations.size() << "\n";
    std::cout << "anchor_positions=" << anchors.size() << "\n";
    if (exact_anchor_index >= 0) {
        std::cout << "exact_anchor_index=" << exact_anchor_index << "\n";
        std::cout << "exact_anchor_vertices=[";
        for (int index = 0; index < 4; ++index) {
            if (index) std::cout << ",";
            std::cout << anchors[exact_anchor_index].inside[index];
        }
        std::cout << "]\n";
        std::cout << "exact_jobs_total=" << total_exact_jobs << "\n";
    }
    std::cout << "magnitude_assignments_sampled="
              << magnitude_assignments.load() << "\n";
    std::cout << "anchor_trials=" << trials.load() << "\n";
    std::cout << "wall_seconds=" << elapsed() << "\n";
    if (found.case_number != -1) {
        print_witness(found);
        return 0;
    }
    if (exact_anchor_index >= 0
        && trials.load() == total_exact_jobs) {
        std::cout << "NO WITNESS FOR THIS ANCHOR (complete)\n";
        return 0;
    }
    std::cout << "NO WITNESS (heuristic only)\n";
    return 1;
}
