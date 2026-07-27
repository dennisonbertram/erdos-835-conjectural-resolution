// Bounded dancing-links witness search for the C17 exact-cover matrix.
//
// A SAT output is only a candidate until the independent Python semantic
// verifier checks it. Timeout or local exhaustion is not a portable UNSAT
// certificate.

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

class Dlx {
 public:
  Dlx(int column_count, const std::vector<InputRow>& rows, std::uint64_t seed,
      double seconds)
      : rng_(seed),
        deadline_(std::chrono::steady_clock::now() +
                  std::chrono::milliseconds(
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
      if (row.label < 0 || row_node_[row.label] != -1) {
        throw std::runtime_error("duplicate or negative row label");
      }
      row_node_[row.label] = first;
    }
  }

  bool Search() { return SearchAtDepth(0); }
  bool ApplyFixedRow(const int label) {
    if (label < 0 || label >= static_cast<int>(row_node_.size()) ||
        row_node_[label] < 0) {
      return false;
    }
    const int row = row_node_[label];
    int node = row;
    do {
      const int header = column_[node];
      const bool header_active =
          right_[left_[header]] == header && left_[right_[header]] == header;
      const bool node_active =
          down_[up_[node]] == node && up_[down_[node]] == node;
      if (!header_active || !node_active) return false;
      node = right_[node];
    } while (node != row);

    solution_.push_back(label);
    Cover(column_[row]);
    for (node = right_[row]; node != row; node = right_[node]) {
      Cover(column_[node]);
    }
    return true;
  }
  bool timed_out() const { return timed_out_; }
  std::uint64_t nodes() const { return nodes_; }
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

  int SmallestColumn() const {
    int best = -1;
    int best_size = std::numeric_limits<int>::max();
    for (int header = right_[0]; header != 0; header = right_[header]) {
      if (size_[header] < best_size) {
        best = header;
        best_size = size_[header];
        if (best_size == 0) break;
      }
    }
    return best;
  }

  bool SearchAtDepth(const int depth) {
    ++nodes_;
    if (right_[0] == 0) return true;
    if ((nodes_ & ((1u << 10) - 1)) == 0) {
      if (std::chrono::steady_clock::now() >= deadline_) {
        timed_out_ = true;
        return false;
      }
    }
    if ((nodes_ & ((1u << 18) - 1)) == 0) {
      std::cerr << "nodes=" << nodes_ << " depth=" << depth << '\n';
    }

    const int header = SmallestColumn();
    if (header < 0 || size_[header] == 0) return false;
    std::vector<int> options;
    for (int row = down_[header]; row != header; row = down_[row]) {
      options.push_back(row);
    }
    std::shuffle(options.begin(), options.end(), rng_);
    Cover(header);
    for (const int row : options) {
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
  std::vector<int> solution_;
  std::mt19937_64 rng_;
  std::chrono::steady_clock::time_point deadline_;
  std::uint64_t nodes_ = 0;
  bool timed_out_ = false;
};

std::vector<InputRow> ReadMatrix(const std::string& path, int* columns) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open matrix");
  std::string line;
  if (!std::getline(input, line)) throw std::runtime_error("empty matrix");
  std::istringstream header(line);
  std::string p, kind;
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
    if (row.label <= 0) throw std::runtime_error("row labels must be positive");
    int column;
    while (stream >> column) row.columns.push_back(column);
    if (!stream.eof()) throw std::runtime_error("trailing non-integer row data");
    auto distinct = row.columns;
    std::sort(distinct.begin(), distinct.end());
    if (std::adjacent_find(distinct.begin(), distinct.end()) != distinct.end()) {
      throw std::runtime_error("duplicate column in matrix row");
    }
    rows.push_back(std::move(row));
  }
  if (static_cast<int>(rows.size()) != rows_declared) {
    throw std::runtime_error("matrix row count mismatch");
  }
  return rows;
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
  if (close(descriptor) != 0) {
    throw std::runtime_error("model close failed");
  }
}

int main(int argc, char** argv) {
  if (argc < 5) {
    std::cerr
        << "usage: solve_c17_exact_cover MATRIX MODEL SECONDS SEED [FIXED_ROW...]\n";
    return 64;
  }
  try {
    int columns = 0;
    auto rows = ReadMatrix(argv[1], &columns);
    if (columns != 1'140 || rows.size() != 2'964) {
      throw std::runtime_error("matrix does not have canonical C17 dimensions");
    }
    const double seconds = std::stod(argv[3]);
    const std::uint64_t seed = std::stoull(argv[4]);
    Dlx solver(columns, rows, seed, seconds);
    for (int argument = 5; argument < argc; ++argument) {
      const int label = std::stoi(argv[argument]);
      if (!solver.ApplyFixedRow(label)) {
        throw std::runtime_error("incompatible or invalid fixed row");
      }
    }
    if (!solver.Search()) {
      std::cout << (solver.timed_out() ? "UNKNOWN timeout"
                                      : "EXHAUSTED_WITHOUT_CERTIFICATE")
                << " nodes=" << solver.nodes() << '\n';
      return solver.timed_out() ? 2 : 3;
    }
    WriteModelExclusive(argv[2], solver.solution());
    std::cout << "SAT_CANDIDATE rows=" << solver.solution().size()
              << " nodes=" << solver.nodes() << " seed=" << seed << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
