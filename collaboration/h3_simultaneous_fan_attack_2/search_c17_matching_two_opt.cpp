// Stochastic one- and two-variable local search for the canonical C17 exact
// cover.  This is a witness hunter only: a score-zero assignment is checked
// against all 1,140 columns before an exclusive SAT-candidate file is written.
// A timeout or positive score has no mathematical status.

#include <algorithm>
#include <array>
#include <chrono>
#include <cerrno>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <fcntl.h>
#include <iostream>
#include <limits>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
#include <unistd.h>

namespace {

constexpr int kColumns = 1'140;
constexpr int kRows = 2'964;
constexpr int kQuadGroups = 228;
constexpr int kTripleColourGroups = 912;
constexpr int kChoices = 13;

struct Row {
  int label = 0;
  int quad = -1;
  std::array<int, 4> triple_colours{};
};

struct Move {
  int quad = -1;
  int row = -1;
  int delta = 0;
  std::array<std::pair<int, int>, 8> changes{};
  int change_count = 0;
};

int Collision(const int count) { return count * (count - 1) / 2; }

std::vector<Row> ReadMatrix(
    const std::string& path,
    std::array<std::vector<int>, kQuadGroups>* rows_by_quad) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open matrix");
  std::string marker;
  std::string kind;
  int columns = 0;
  int declared_rows = 0;
  if (!(input >> marker >> kind >> columns >> declared_rows) ||
      marker != "p" || kind != "exact" || columns != kColumns ||
      declared_rows != kRows) {
    throw std::runtime_error("matrix does not have canonical C17 header");
  }

  std::vector<Row> rows;
  rows.reserve(kRows);
  std::array<bool, 3'877> seen_labels{};
  for (int index = 0; index < declared_rows; ++index) {
    int label = 0;
    std::array<int, 5> incidence{};
    if (!(input >> label) || label <= 0 ||
        label >= static_cast<int>(seen_labels.size()) ||
        seen_labels[label]) {
      throw std::runtime_error("invalid or duplicate matrix row label");
    }
    seen_labels[label] = true;
    for (int& column : incidence) {
      if (!(input >> column) || column < 0 || column >= columns) {
        throw std::runtime_error("invalid matrix incidence");
      }
    }
    std::sort(incidence.begin(), incidence.end());
    if (std::adjacent_find(incidence.begin(), incidence.end()) !=
        incidence.end()) {
      throw std::runtime_error("matrix row repeats a column");
    }
    if (incidence[0] < 0 || incidence[0] >= kQuadGroups ||
        incidence[1] < kQuadGroups) {
      throw std::runtime_error("row does not have one Q and four TC columns");
    }
    Row row;
    row.label = label;
    row.quad = incidence[0];
    for (int offset = 0; offset < 4; ++offset) {
      row.triple_colours[offset] =
          incidence[1 + offset] - kQuadGroups;
    }
    rows_by_quad->at(row.quad).push_back(index);
    rows.push_back(row);
  }
  std::string extra;
  if (input >> extra) throw std::runtime_error("trailing matrix data");
  for (const auto& group : *rows_by_quad) {
    if (group.size() != kChoices) {
      throw std::runtime_error("Q-group does not have thirteen rows");
    }
  }
  return rows;
}

std::vector<int> ReadHint(
    const std::string& path,
    const std::vector<Row>& rows,
    const std::array<std::vector<int>, kQuadGroups>& rows_by_quad) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open hint");
  std::vector<int> label_to_row(3'877, -1);
  for (int row = 0; row < static_cast<int>(rows.size()); ++row) {
    if (rows[row].label <= 0 ||
        rows[row].label >= static_cast<int>(label_to_row.size()) ||
        label_to_row[rows[row].label] != -1) {
      throw std::runtime_error("duplicate or invalid matrix row label");
    }
    label_to_row[rows[row].label] = row;
  }
  std::vector<int> selected(kQuadGroups, -1);
  int label = 0;
  int labels = 0;
  while (input >> label) {
    if (label <= 0 || label >= static_cast<int>(label_to_row.size()) ||
        label_to_row[label] < 0) {
      throw std::runtime_error("hint contains absent row label");
    }
    const int row = label_to_row[label];
    const int quad = rows[row].quad;
    if (selected[quad] != -1) {
      throw std::runtime_error("hint repeats a Q-group");
    }
    selected[quad] = row;
    ++labels;
  }
  if (!input.eof() || labels != kQuadGroups ||
      std::find(selected.begin(), selected.end(), -1) != selected.end()) {
    throw std::runtime_error("hint is not a 228-row Q-transversal");
  }
  for (int quad = 0; quad < kQuadGroups; ++quad) {
    if (std::find(rows_by_quad[quad].begin(), rows_by_quad[quad].end(),
                  selected[quad]) == rows_by_quad[quad].end()) {
      throw std::runtime_error("hint Q-group mapping drift");
    }
  }
  return selected;
}

void Recompute(
    const std::vector<Row>& rows,
    const std::vector<int>& selected,
    std::array<int, kTripleColourGroups>* counts,
    int* score) {
  counts->fill(0);
  for (const int row : selected) {
    for (const int group : rows[row].triple_colours) {
      ++counts->at(group);
    }
  }
  *score = 0;
  for (const int count : *counts) *score += Collision(count);
}

Move MakeMove(
    const int quad,
    const int replacement,
    const std::vector<Row>& rows,
    const std::vector<int>& selected,
    const std::array<int, kTripleColourGroups>& counts) {
  Move move;
  move.quad = quad;
  move.row = replacement;
  const Row& old_row = rows[selected[quad]];
  const Row& new_row = rows[replacement];
  std::array<int, 8> touched{};
  int touched_count = 0;
  for (const int group : old_row.triple_colours) {
    touched[touched_count++] = group;
  }
  for (const int group : new_row.triple_colours) {
    touched[touched_count++] = group;
  }
  std::sort(touched.begin(), touched.begin() + touched_count);
  for (int begin = 0; begin < touched_count;) {
    int end = begin + 1;
    while (end < touched_count && touched[end] == touched[begin]) ++end;
    const int group = touched[begin];
    const int old_hit = std::count(
        old_row.triple_colours.begin(), old_row.triple_colours.end(), group);
    const int new_hit = std::count(
        new_row.triple_colours.begin(), new_row.triple_colours.end(), group);
    const int change = new_hit - old_hit;
    if (change != 0) {
      move.changes[move.change_count++] = {group, change};
      move.delta += Collision(counts[group] + change) -
                    Collision(counts[group]);
    }
    begin = end;
  }
  return move;
}

int Interaction(const Move& first, const Move& second) {
  int result = 0;
  for (int left = 0; left < first.change_count; ++left) {
    for (int right = 0; right < second.change_count; ++right) {
      if (first.changes[left].first == second.changes[right].first) {
        result += first.changes[left].second * second.changes[right].second;
      }
    }
  }
  return result;
}

void ApplyMove(
    const Move& move,
    std::vector<int>* selected,
    std::array<int, kTripleColourGroups>* counts,
    int* score) {
  for (int index = 0; index < move.change_count; ++index) {
    counts->at(move.changes[index].first) += move.changes[index].second;
  }
  selected->at(move.quad) = move.row;
  *score += move.delta;
}

int ApplyBestGlobalImprovement(
    const std::vector<Row>& rows,
    const std::array<std::vector<int>, kQuadGroups>& rows_by_quad,
    std::vector<int>* selected,
    std::array<int, kTripleColourGroups>* counts,
    int* score,
    std::uint64_t* pair_scans) {
  std::vector<Move> all_moves;
  all_moves.reserve(kQuadGroups * (kChoices - 1));
  for (int quad = 0; quad < kQuadGroups; ++quad) {
    for (const int row : rows_by_quad[quad]) {
      if (row != selected->at(quad)) {
        all_moves.push_back(
            MakeMove(quad, row, rows, *selected, *counts));
      }
    }
  }
  const auto best_single = std::min_element(
      all_moves.begin(), all_moves.end(),
      [](const Move& left, const Move& right) {
        return left.delta < right.delta;
      });
  if (best_single != all_moves.end() && best_single->delta < 0) {
    ApplyMove(*best_single, selected, counts, score);
    return 1;
  }

  std::array<std::vector<int>, kTripleColourGroups> positive_moves;
  std::array<std::vector<int>, kTripleColourGroups> negative_moves;
  for (int move_index = 0;
       move_index < static_cast<int>(all_moves.size());
       ++move_index) {
    const Move& move = all_moves[move_index];
    for (int change = 0; change < move.change_count; ++change) {
      const auto [group, amount] = move.changes[change];
      (amount > 0 ? positive_moves[group] : negative_moves[group])
          .push_back(move_index);
    }
  }
  const Move* best_first = nullptr;
  const Move* best_second = nullptr;
  int best_pair_delta = 0;
  for (int group = 0; group < kTripleColourGroups; ++group) {
    for (const int positive : positive_moves[group]) {
      for (const int negative : negative_moves[group]) {
        if (all_moves[positive].quad == all_moves[negative].quad) continue;
        const int delta =
            all_moves[positive].delta + all_moves[negative].delta +
            Interaction(all_moves[positive], all_moves[negative]);
        if (delta < best_pair_delta) {
          best_pair_delta = delta;
          best_first = &all_moves[positive];
          best_second = &all_moves[negative];
        }
      }
    }
  }
  ++*pair_scans;
  if (best_first == nullptr || best_second == nullptr) return 0;
  for (int index = 0; index < best_first->change_count; ++index) {
    counts->at(best_first->changes[index].first) +=
        best_first->changes[index].second;
  }
  for (int index = 0; index < best_second->change_count; ++index) {
    counts->at(best_second->changes[index].first) +=
        best_second->changes[index].second;
  }
  selected->at(best_first->quad) = best_first->row;
  selected->at(best_second->quad) = best_second->row;
  *score += best_pair_delta;
  return 2;
}

bool VerifyExactCover(
    const std::vector<Row>& rows,
    const std::vector<int>& selected) {
  if (selected.size() != kQuadGroups) return false;
  std::array<int, kColumns> counts{};
  for (const int row_index : selected) {
    const Row& row = rows[row_index];
    ++counts[row.quad];
    for (const int group : row.triple_colours) {
      ++counts[kQuadGroups + group];
    }
  }
  return std::all_of(
      counts.begin(), counts.end(), [](const int count) { return count == 1; });
}

void WriteExclusive(
    const std::string& path,
    const std::string& content,
    const bool executable = false) {
  const int mode = executable ? 0755 : 0644;
  const int descriptor =
      open(path.c_str(), O_WRONLY | O_CREAT | O_EXCL, mode);
  if (descriptor < 0) {
    throw std::runtime_error("cannot exclusively create output: " +
                             std::string(std::strerror(errno)));
  }
  std::size_t written = 0;
  while (written < content.size()) {
    const ssize_t count =
        write(descriptor, content.data() + written, content.size() - written);
    if (count <= 0) {
      const std::string message = std::strerror(errno);
      close(descriptor);
      throw std::runtime_error("output write failed: " + message);
    }
    written += static_cast<std::size_t>(count);
  }
  if (close(descriptor) != 0) {
    throw std::runtime_error("output close failed");
  }
}

void WriteCandidate(
    const std::string& path,
    const std::vector<Row>& rows,
    const std::vector<int>& selected) {
  std::ostringstream output;
  output << "s SATISFIABLE\nv";
  for (const int row : selected) output << ' ' << rows[row].label;
  output << " 0\n";
  WriteExclusive(path, output.str());
}

void WriteBestEffort(
    const std::string& path,
    const std::vector<Row>& rows,
    const std::vector<int>& selected) {
  std::ostringstream output;
  for (const int row : selected) output << rows[row].label << '\n';
  WriteExclusive(path, output.str());
}

struct Options {
  std::string matrix;
  std::string model;
  double seconds = 0.0;
  std::uint64_t seed = 0;
  std::string hint;
  std::string best_effort;
};

Options ParseOptions(const int argc, char** argv) {
  if (argc < 5) {
    throw std::runtime_error(
        "usage: search_c17_matching_two_opt MATRIX MODEL SECONDS SEED "
        "[--hint ROW_LABEL_FILE] [--best-effort ROW_LABEL_FILE]");
  }
  Options options;
  options.matrix = argv[1];
  options.model = argv[2];
  options.seconds = std::stod(argv[3]);
  options.seed = std::stoull(argv[4]);
  if (options.seconds <= 0.0) {
    throw std::runtime_error("SECONDS must be positive");
  }
  for (int argument = 5; argument < argc; ++argument) {
    const std::string flag = argv[argument];
    if ((flag == "--hint" || flag == "--best-effort") &&
        argument + 1 < argc) {
      const std::string value = argv[++argument];
      if (flag == "--hint") {
        options.hint = value;
      } else {
        options.best_effort = value;
      }
    } else {
      throw std::runtime_error("invalid option");
    }
  }
  if ((!options.hint.empty() && options.model == options.hint) ||
      (!options.best_effort.empty() &&
       (options.best_effort == options.model ||
        options.best_effort == options.hint))) {
    throw std::runtime_error(
        "model, hint, and best-effort paths must be distinct");
  }
  return options;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = ParseOptions(argc, argv);
    std::array<std::vector<int>, kQuadGroups> rows_by_quad;
    const std::vector<Row> rows =
        ReadMatrix(options.matrix, &rows_by_quad);
    std::vector<int> hinted;
    if (!options.hint.empty()) {
      hinted = ReadHint(options.hint, rows, rows_by_quad);
    }

    std::mt19937_64 rng(options.seed);
    const auto started = std::chrono::steady_clock::now();
    const auto deadline =
        started + std::chrono::milliseconds(static_cast<std::int64_t>(
                      options.seconds * 1000.0));
    std::vector<int> best_selection;
    int best_score = std::numeric_limits<int>::max();
    std::uint64_t moves = 0;
    std::uint64_t pair_scans = 0;
    std::uint64_t restarts = 0;
    const auto record_best_and_write_candidate =
        [&](const std::vector<int>& selected, const int score) {
          if (score >= best_score) return false;
          best_score = score;
          best_selection = selected;
          std::cout << "best=" << best_score << " moves=" << moves
                    << " restarts=" << restarts << " pair_scans="
                    << pair_scans << " elapsed="
                    << std::chrono::duration<double>(
                           std::chrono::steady_clock::now() - started)
                           .count()
                    << '\n';
          if (best_score != 0) return false;
          if (!VerifyExactCover(rows, best_selection)) {
            throw std::runtime_error(
                "score-zero semantic verification failed");
          }
          WriteCandidate(options.model, rows, best_selection);
          std::cout << "SAT_CANDIDATE rows=" << best_selection.size()
                    << " loaded_matrix_verification=PASS "
                    << "independent_verification=REQUIRED\n";
          return true;
        };

    while (std::chrono::steady_clock::now() < deadline) {
      ++restarts;
      std::vector<int> selected(kQuadGroups);
      if (restarts == 1 && !hinted.empty()) {
        selected = hinted;
      } else if (!best_selection.empty() && restarts % 4 != 0) {
        selected = best_selection;
        const int perturbations = 2 + static_cast<int>(restarts % 9);
        for (int step = 0; step < perturbations; ++step) {
          const int quad =
              std::uniform_int_distribution<int>(0, kQuadGroups - 1)(rng);
          selected[quad] = rows_by_quad[quad][
              std::uniform_int_distribution<int>(0, kChoices - 1)(rng)];
        }
      } else {
        for (int quad = 0; quad < kQuadGroups; ++quad) {
          selected[quad] = rows_by_quad[quad][
              std::uniform_int_distribution<int>(0, kChoices - 1)(rng)];
        }
      }

      std::array<int, kTripleColourGroups> counts{};
      int score = 0;
      Recompute(rows, selected, &counts, &score);
      if (record_best_and_write_candidate(selected, score)) return 0;
      int since_improvement = 0;

      while (std::chrono::steady_clock::now() < deadline &&
             since_improvement < 5'000) {
        if (since_improvement % 100 == 0) {
          const int previous_best = best_score;
          const int improved = ApplyBestGlobalImprovement(
              rows, rows_by_quad, &selected, &counts, &score, &pair_scans);
          if (improved != 0) {
            moves += static_cast<std::uint64_t>(improved);
            since_improvement += improved;
            if (record_best_and_write_candidate(selected, score)) return 0;
            if (score < previous_best) since_improvement = 0;
            continue;
          }
        }

        std::vector<int> overloaded;
        for (int group = 0; group < kTripleColourGroups; ++group) {
          if (counts[group] > 1) overloaded.push_back(group);
        }
        if (overloaded.empty()) {
          throw std::runtime_error("positive score without overloaded group");
        }
        const int target = overloaded[
            std::uniform_int_distribution<std::size_t>(
                0, overloaded.size() - 1)(rng)];
        std::vector<int> implicated;
        for (int quad = 0; quad < kQuadGroups; ++quad) {
          const auto& groups = rows[selected[quad]].triple_colours;
          if (std::find(groups.begin(), groups.end(), target) != groups.end()) {
            implicated.push_back(quad);
          }
        }
        const int quad = implicated[
            std::uniform_int_distribution<std::size_t>(
                0, implicated.size() - 1)(rng)];
        std::vector<Move> choices;
        for (const int row : rows_by_quad[quad]) {
          if (row != selected[quad]) {
            choices.push_back(MakeMove(quad, row, rows, selected, counts));
          }
        }
        const int minimum = std::min_element(
            choices.begin(), choices.end(),
            [](const Move& left, const Move& right) {
              return left.delta < right.delta;
            })->delta;
        std::vector<int> minima;
        for (int index = 0; index < static_cast<int>(choices.size()); ++index) {
          if (choices[index].delta == minimum) minima.push_back(index);
        }
        const Move choice = choices[minima[
            std::uniform_int_distribution<std::size_t>(
                0, minima.size() - 1)(rng)]];
        ApplyMove(choice, &selected, &counts, &score);
        ++moves;
        ++since_improvement;
        const int previous_best = best_score;
        if (record_best_and_write_candidate(selected, score)) return 0;
        if (score < previous_best) since_improvement = 0;

        if (moves % 100'000 == 0) {
          std::array<int, kTripleColourGroups> exact_counts{};
          int exact_score = 0;
          Recompute(rows, selected, &exact_counts, &exact_score);
          if (counts != exact_counts || score != exact_score) {
            throw std::runtime_error("incremental score drift");
          }
        }
      }
    }

    if (best_selection.empty()) {
      throw std::runtime_error("search produced no assignment");
    }
    if (!options.best_effort.empty()) {
      WriteBestEffort(options.best_effort, rows, best_selection);
      std::cout << "best_effort=" << options.best_effort << '\n';
    }
    std::cout << "status=UNKNOWN best_collision_score=" << best_score
              << " moves=" << moves << " restarts=" << restarts
              << " pair_scans=" << pair_scans << '\n'
              << "certificate=NONE\n"
              << "scope=positive score or timeout has no mathematical status\n";
    return 2;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
