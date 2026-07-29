// Audit-only DLX value-order benchmark for the canonical C17 exact-cover matrix.
//
// Every mode traverses the same exact-cover tree and changes only the order of
// rows below the minimum-cardinality column.  A SAT output remains only a
// candidate until the independent semantic verifier accepts it.  A timeout has
// no mathematical status.

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cerrno>
#include <cstring>
#include <fstream>
#include <fcntl.h>
#include <iostream>
#include <limits>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <unistd.h>

struct InputRow {
  int label;
  std::vector<int> columns;
};

enum class OrderMode {
  kRandom,
  kRandomColumnTies,
  kLeastConstraining,
  kMostConstraining,
  kLeastDamage,
  kHintFirstRandom,
  kHintFirstRandomColumnTies,
  kHintFirstLeastConstraining,
  kHintFirstLeastDamage,
  kHintRepair,
};

OrderMode ParseMode(const std::string& name) {
  if (name == "random") return OrderMode::kRandom;
  if (name == "random-ties") return OrderMode::kRandomColumnTies;
  if (name == "lcv") return OrderMode::kLeastConstraining;
  if (name == "mcv") return OrderMode::kMostConstraining;
  if (name == "damage") return OrderMode::kLeastDamage;
  if (name == "hint-random") return OrderMode::kHintFirstRandom;
  if (name == "hint-random-ties") {
    return OrderMode::kHintFirstRandomColumnTies;
  }
  if (name == "hint-lcv") return OrderMode::kHintFirstLeastConstraining;
  if (name == "hint-damage") return OrderMode::kHintFirstLeastDamage;
  if (name == "hint-repair") return OrderMode::kHintRepair;
  throw std::runtime_error("unknown order mode");
}

struct Option {
  int node;
  int size_sum;
  int damage;
  int preferred_loss;
  bool preferred;
};

class Dlx {
 public:
  Dlx(int column_count, const std::vector<InputRow>& rows, std::uint64_t seed,
      double seconds, OrderMode mode, const std::vector<int>& preferred_labels)
      : rng_(seed),
        mode_(mode),
        started_(std::chrono::steady_clock::now()),
        deadline_(started_ + std::chrono::milliseconds(
                                static_cast<std::int64_t>(seconds * 1000.0))) {
    const int capacity = 1 + column_count + static_cast<int>(rows.size()) * 5;
    left_.resize(capacity);
    right_.resize(capacity);
    up_.resize(capacity);
    down_.resize(capacity);
    column_.resize(capacity);
    row_label_.resize(capacity);
    size_.assign(1 + column_count, 0);
    int maximum_label = 0;
    for (const auto& row : rows) maximum_label = std::max(maximum_label, row.label);
    row_node_.assign(1 + maximum_label, -1);
    preferred_.assign(1 + maximum_label, false);
    seen_preferred_.assign(1 + maximum_label, 0);
    seen_conflict_.assign(1 + maximum_label, 0);

    for (int node = 0; node <= column_count; ++node) {
      left_[node] = node - 1;
      right_[node] = node + 1;
      up_[node] = down_[node] = node;
      column_[node] = node;
    }
    left_[0] = column_count;
    right_[column_count] = 0;

    int next = column_count + 1;
    for (const auto& row : rows) {
      if (row.columns.size() != 5) {
        throw std::runtime_error("each input row must have five columns");
      }
      int first = -1;
      int previous = -1;
      for (const int zero_based : row.columns) {
        if (zero_based < 0 || zero_based >= column_count) {
          throw std::runtime_error("column outside declared range");
        }
        const int header = 1 + zero_based;
        const int node = next++;
        column_[node] = header;
        row_label_[node] = row.label;
        up_[node] = up_[header];
        down_[node] = header;
        down_[up_[header]] = node;
        up_[header] = node;
        ++size_[header];

        if (first < 0) {
          first = previous = node;
          left_[node] = right_[node] = node;
        } else {
          left_[node] = previous;
          right_[node] = first;
          right_[previous] = node;
          left_[first] = node;
          previous = node;
        }
      }
      if (row.label <= 0 || row.label >= static_cast<int>(row_node_.size()) ||
          row_node_[row.label] != -1) {
        throw std::runtime_error("duplicate or nonpositive row label");
      }
      row_node_[row.label] = first;
    }
    for (const int label : preferred_labels) {
      if (label <= 0 || label > maximum_label || row_node_[label] < 0) {
        throw std::runtime_error("preferred row label is absent from matrix");
      }
      preferred_[label] = true;
    }
  }

  bool Search() { return SearchAtDepth(0); }
  bool timed_out() const { return timed_out_; }
  std::uint64_t nodes() const { return nodes_; }
  std::uint64_t branches() const { return branches_; }
  std::uint64_t dead_ends() const { return dead_ends_; }
  int max_depth() const { return max_depth_; }
  double elapsed_seconds() const {
    return std::chrono::duration<double>(
               std::chrono::steady_clock::now() - started_)
        .count();
  }
  const std::vector<int>& solution() const { return solution_; }

 private:
  void Cover(const int header) {
    right_[left_[header]] = right_[header];
    left_[right_[header]] = left_[header];
    for (int row = down_[header]; row != header; row = down_[row]) {
      for (int node = right_[row]; node != row; node = right_[node]) {
        down_[up_[node]] = down_[node];
        up_[down_[node]] = up_[node];
        --size_[column_[node]];
      }
    }
  }

  void Uncover(const int header) {
    for (int row = up_[header]; row != header; row = up_[row]) {
      for (int node = left_[row]; node != row; node = left_[node]) {
        ++size_[column_[node]];
        down_[up_[node]] = node;
        up_[down_[node]] = node;
      }
    }
    right_[left_[header]] = header;
    left_[right_[header]] = header;
  }

  bool RandomizeColumnTies() const {
    return mode_ == OrderMode::kRandomColumnTies ||
           mode_ == OrderMode::kHintFirstRandomColumnTies;
  }

  int SmallestColumn() {
    int best = -1;
    int best_size = std::numeric_limits<int>::max();
    int ties = 0;
    for (int header = right_[0]; header != 0; header = right_[header]) {
      if (size_[header] < best_size) {
        best = header;
        best_size = size_[header];
        ties = 1;
      } else if (size_[header] == best_size && RandomizeColumnTies()) {
        ++ties;
        if (std::uniform_int_distribution<int>(1, ties)(rng_) == 1) {
          best = header;
        }
      }
      if (best_size == 0) break;
    }
    return best;
  }

  int SizeSum(const int row) const {
    int result = 0;
    int node = row;
    do {
      result += size_[column_[node]];
      node = right_[node];
    } while (node != row);
    return result;
  }

  int PreferredLoss(const int row) {
    if (++seen_token_ == 0) {
      std::fill(seen_preferred_.begin(), seen_preferred_.end(), 0);
      seen_token_ = 1;
    }
    int result = 0;
    int selected = row;
    do {
      const int header = column_[selected];
      for (int conflict = down_[header]; conflict != header;
           conflict = down_[conflict]) {
        const int label = row_label_[conflict];
        if (preferred_[label] && seen_preferred_[label] != seen_token_) {
          seen_preferred_[label] = seen_token_;
          ++result;
        }
      }
      selected = right_[selected];
    } while (selected != row);
    return result;
  }

  int Damage(const int row) {
    if (++conflict_token_ == 0) {
      std::fill(seen_conflict_.begin(), seen_conflict_.end(), 0);
      conflict_token_ = 1;
    }
    int selected_headers[5];
    int selected_count = 0;
    int selected = row;
    do {
      selected_headers[selected_count++] = column_[selected];
      selected = right_[selected];
    } while (selected != row);
    if (selected_count != 5) throw std::runtime_error("wrong row degree");

    std::vector<int> conflicts;
    for (const int header : selected_headers) {
      for (int conflict = down_[header]; conflict != header;
           conflict = down_[conflict]) {
        const int label = row_label_[conflict];
        if (seen_conflict_[label] != conflict_token_) {
          seen_conflict_[label] = conflict_token_;
          conflicts.push_back(label);
        }
      }
    }

    int result = 0;
    for (const int label : conflicts) {
      int node = row_node_[label];
      const int first = node;
      do {
        const int header = column_[node];
        if (std::find(selected_headers, selected_headers + 5, header) ==
            selected_headers + 5) {
          ++result;
        }
        node = right_[node];
      } while (node != first);
    }
    return result;
  }

  std::vector<Option> OrderedOptions(const int header) {
    std::vector<Option> options;
    const bool needs_loss =
        mode_ == OrderMode::kHintFirstLeastConstraining ||
        mode_ == OrderMode::kHintFirstLeastDamage ||
        mode_ == OrderMode::kHintRepair;
    const bool needs_damage =
        mode_ == OrderMode::kLeastDamage ||
        mode_ == OrderMode::kHintFirstLeastDamage;
    for (int row = down_[header]; row != header; row = down_[row]) {
      options.push_back({row, SizeSum(row), needs_damage ? Damage(row) : 0,
                         needs_loss ? PreferredLoss(row) : 0,
                         preferred_[row_label_[row]]});
    }
    std::shuffle(options.begin(), options.end(), rng_);
    if (mode_ == OrderMode::kRandom ||
        mode_ == OrderMode::kRandomColumnTies) {
      return options;
    }
    if (mode_ == OrderMode::kLeastConstraining) {
      std::stable_sort(options.begin(), options.end(),
                       [](const Option& left, const Option& right) {
                         return left.size_sum < right.size_sum;
                       });
    } else if (mode_ == OrderMode::kMostConstraining) {
      std::stable_sort(options.begin(), options.end(),
                       [](const Option& left, const Option& right) {
                         return left.size_sum > right.size_sum;
                       });
    } else if (mode_ == OrderMode::kLeastDamage) {
      std::stable_sort(options.begin(), options.end(),
                       [](const Option& left, const Option& right) {
                         if (left.damage != right.damage) {
                           return left.damage < right.damage;
                         }
                         return left.size_sum < right.size_sum;
                       });
    } else if (mode_ == OrderMode::kHintFirstRandom ||
               mode_ == OrderMode::kHintFirstRandomColumnTies) {
      std::stable_partition(options.begin(), options.end(),
                            [](const Option& option) {
                              return option.preferred;
                            });
    } else if (mode_ == OrderMode::kHintFirstLeastConstraining) {
      std::stable_sort(options.begin(), options.end(),
                       [](const Option& left, const Option& right) {
                         if (left.preferred != right.preferred) {
                           return left.preferred > right.preferred;
                         }
                         if (left.preferred_loss != right.preferred_loss) {
                           return left.preferred_loss < right.preferred_loss;
                         }
                         return left.size_sum < right.size_sum;
                       });
    } else if (mode_ == OrderMode::kHintFirstLeastDamage) {
      std::stable_sort(options.begin(), options.end(),
                       [](const Option& left, const Option& right) {
                         if (left.preferred != right.preferred) {
                           return left.preferred > right.preferred;
                         }
                         if (left.preferred_loss != right.preferred_loss) {
                           return left.preferred_loss < right.preferred_loss;
                         }
                         if (left.damage != right.damage) {
                           return left.damage < right.damage;
                         }
                         return left.size_sum < right.size_sum;
                       });
    } else {
      std::stable_sort(options.begin(), options.end(),
                       [](const Option& left, const Option& right) {
                         if (left.preferred_loss != right.preferred_loss) {
                           return left.preferred_loss < right.preferred_loss;
                         }
                         if (left.preferred != right.preferred) {
                           return left.preferred > right.preferred;
                         }
                         return left.size_sum < right.size_sum;
                       });
    }
    return options;
  }

  bool SearchAtDepth(const int depth) {
    ++nodes_;
    max_depth_ = std::max(max_depth_, depth);
    if (right_[0] == 0) return true;
    if ((nodes_ & ((1u << 10) - 1)) == 0 &&
        std::chrono::steady_clock::now() >= deadline_) {
      timed_out_ = true;
      return false;
    }

    const int header = SmallestColumn();
    if (header < 0 || size_[header] == 0) {
      ++dead_ends_;
      return false;
    }
    auto options = OrderedOptions(header);
    Cover(header);
    for (const auto& option : options) {
      ++branches_;
      const int row = option.node;
      solution_.push_back(row_label_[row]);
      for (int node = right_[row]; node != row; node = right_[node]) {
        Cover(column_[node]);
      }
      if (SearchAtDepth(depth + 1)) return true;
      for (int node = left_[row]; node != row; node = left_[node]) {
        Uncover(column_[node]);
      }
      solution_.pop_back();
      if (timed_out_) break;
    }
    Uncover(header);
    return false;
  }

  std::vector<int> left_, right_, up_, down_, column_, row_label_, size_;
  std::vector<int> row_node_;
  std::vector<bool> preferred_;
  std::vector<std::uint32_t> seen_preferred_;
  std::vector<std::uint32_t> seen_conflict_;
  std::vector<int> solution_;
  std::mt19937_64 rng_;
  OrderMode mode_;
  std::chrono::steady_clock::time_point started_;
  std::chrono::steady_clock::time_point deadline_;
  std::uint64_t nodes_ = 0;
  std::uint64_t branches_ = 0;
  std::uint64_t dead_ends_ = 0;
  std::uint32_t seen_token_ = 0;
  std::uint32_t conflict_token_ = 0;
  int max_depth_ = 0;
  bool timed_out_ = false;
};

std::vector<InputRow> ReadMatrix(const std::string& path, int* columns) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open matrix");
  std::string line;
  if (!std::getline(input, line)) throw std::runtime_error("empty matrix");
  std::istringstream header(line);
  std::string p;
  std::string kind;
  int rows_declared = 0;
  if (!(header >> p >> kind >> *columns >> rows_declared) || p != "p" ||
      kind != "exact") {
    throw std::runtime_error("invalid matrix header");
  }
  std::vector<InputRow> rows;
  while (std::getline(input, line)) {
    if (line.empty()) continue;
    std::istringstream stream(line);
    InputRow row;
    if (!(stream >> row.label)) throw std::runtime_error("invalid row label");
    int column = 0;
    while (stream >> column) row.columns.push_back(column);
    if (!stream.eof() || row.columns.size() != 5) {
      throw std::runtime_error("invalid matrix row");
    }
    auto distinct = row.columns;
    std::sort(distinct.begin(), distinct.end());
    if (row.label <= 0 ||
        std::adjacent_find(distinct.begin(), distinct.end()) != distinct.end()) {
      throw std::runtime_error("invalid row label or duplicate column");
    }
    rows.push_back(std::move(row));
  }
  if (static_cast<int>(rows.size()) != rows_declared) {
    throw std::runtime_error("matrix row count mismatch");
  }
  return rows;
}

std::vector<int> ReadLabels(const std::string& path) {
  if (path == "-") return {};
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open preferred-row file");
  std::vector<int> labels;
  int label = 0;
  while (input >> label) labels.push_back(label);
  if (!input.eof()) throw std::runtime_error("invalid preferred-row file");
  return labels;
}

void WriteModelExclusive(const std::string& path,
                         const std::vector<int>& labels) {
  std::ostringstream content;
  content << "s SATISFIABLE\nv";
  for (const int label : labels) content << ' ' << label;
  content << " 0\n";
  const std::string bytes = content.str();
  const int descriptor =
      open(path.c_str(), O_WRONLY | O_CREAT | O_EXCL, 0644);
  if (descriptor < 0) {
    throw std::runtime_error("cannot exclusively create model: " +
                             std::string(std::strerror(errno)));
  }
  std::size_t written = 0;
  while (written < bytes.size()) {
    const ssize_t count =
        write(descriptor, bytes.data() + written, bytes.size() - written);
    if (count <= 0) {
      const std::string message = std::strerror(errno);
      close(descriptor);
      throw std::runtime_error("model write failed: " + message);
    }
    written += static_cast<std::size_t>(count);
  }
  if (close(descriptor) != 0) throw std::runtime_error("model close failed");
}

int main(int argc, char** argv) {
  if (argc != 7) {
    std::cerr << "usage: solve_c17_exact_cover_order_bench "
                 "MATRIX MODEL SECONDS SEED MODE HINT_OR_DASH\n";
    return 64;
  }
  try {
    int columns = 0;
    const auto rows = ReadMatrix(argv[1], &columns);
    if (columns != 1'140 || rows.size() != 2'964) {
      throw std::runtime_error("matrix does not have canonical C17 dimensions");
    }
    const std::string mode_name = argv[5];
    Dlx solver(columns, rows, std::stoull(argv[4]), std::stod(argv[3]),
               ParseMode(mode_name), ReadLabels(argv[6]));
    const bool sat = solver.Search();
    if (sat) {
      WriteModelExclusive(argv[2], solver.solution());
      std::cout << "SAT_CANDIDATE";
    } else {
      std::cout << (solver.timed_out() ? "UNKNOWN timeout"
                                      : "EXHAUSTED_WITHOUT_CERTIFICATE");
    }
    std::cout << " mode=" << mode_name << " nodes=" << solver.nodes()
              << " branches=" << solver.branches()
              << " dead_ends=" << solver.dead_ends()
              << " max_depth=" << solver.max_depth()
              << " elapsed=" << solver.elapsed_seconds();
    if (sat) std::cout << " rows=" << solver.solution().size();
    std::cout << '\n';
    return sat ? 0 : (solver.timed_out() ? 2 : 3);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
