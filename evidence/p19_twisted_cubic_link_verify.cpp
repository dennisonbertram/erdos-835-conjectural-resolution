// Exhaust alternating forms and independent lift scalings on the normal
// rational curve in PG(3,p).
//
// A rainbow ordered link on p+1 vertices has incident labels F_p at every
// vertex.  Forgetting signs, each row must therefore contain one zero and
// two representatives of every nonzero class modulo {+1,-1}.  For arbitrary
// nonzero lift scalings, those multiplicities give a linear one-hot system.
// At p=11 and p=19, exact Gaussian elimination modulo 3 and modulo 5 makes
// that relaxation inconsistent for every form with the necessary zero
// pattern.  At p=3 and p=7 the program additionally exhausts every total
// order of each unscaled signless survivor.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

namespace {

using Form = std::array<int, 6>;
using Point = std::array<int, 4>;

int mod(int value, int prime) {
  value %= prime;
  return value < 0 ? value + prime : value;
}

int sign_class(int value, int prime) {
  value = mod(value, prime);
  return value == 0 ? 0 : std::min(value, prime - value);
}

int primitive_root(int prime) {
  for (int candidate = 2; candidate < prime; ++candidate) {
    int value = 1;
    int order = 0;
    do {
      value = value * candidate % prime;
      ++order;
    } while (value != 1);
    if (order == prime - 1) {
      return candidate;
    }
  }
  return -1;
}

std::vector<Form> projective_forms(int prime) {
  std::vector<Form> answer;
  for (int first_nonzero = 0; first_nonzero < 6; ++first_nonzero) {
    std::uint64_t total = 1;
    for (int index = first_nonzero + 1; index < 6; ++index) {
      total *= prime;
    }
    for (std::uint64_t code = 0; code < total; ++code) {
      Form form{};
      form[first_nonzero] = 1;
      std::uint64_t remaining = code;
      for (int index = first_nonzero + 1; index < 6; ++index) {
        form[index] = static_cast<int>(remaining % prime);
        remaining /= prime;
      }
      answer.push_back(form);
    }
  }
  return answer;
}

Point curve_point(int parameter, int prime) {
  if (parameter == prime) {
    return {0, 0, 0, 1};  // Infinity.
  }
  return {
      1,
      parameter,
      mod(parameter * parameter, prime),
      mod(parameter * parameter * parameter, prime),
  };
}

int pairing(
    const Point& left, const Point& right, const Form& form, int prime) {
  int answer = 0;
  int coefficient = 0;
  for (int i = 0; i < 4; ++i) {
    for (int j = i + 1; j < 4; ++j) {
      answer += form[coefficient++] *
                (left[i] * right[j] - left[j] * right[i]);
    }
  }
  return mod(answer, prime);
}

// Return 0 if some vertex does not have exactly one zero, 1 if the zero
// pattern works but the full sign-class multiplicities fail, and 2 if all
// sign-class rows work.
int signless_row_level(const Form& form, int prime) {
  bool all_sign_classes = true;
  for (int left = 0; left <= prime; ++left) {
    std::vector<int> counts((prime + 1) / 2);
    const Point left_point = curve_point(left, prime);
    for (int right = 0; right <= prime; ++right) {
      if (left == right) {
        continue;
      }
      const int value =
          pairing(left_point, curve_point(right, prime), form, prime);
      ++counts[sign_class(value, prime)];
    }
    if (counts[0] != 1) {
      return 0;
    }
    for (int sign = 1; sign <= (prime - 1) / 2; ++sign) {
      if (counts[sign] != 2) {
        all_sign_classes = false;
      }
    }
  }
  return all_sign_classes ? 2 : 1;
}

int inverse_mod(int value, int modulus) {
  value %= modulus;
  if (value < 0) {
    value += modulus;
  }
  for (int candidate = 1; candidate < modulus; ++candidate) {
    if (value * candidate % modulus == 1) {
      return candidate;
    }
  }
  return -1;
}

bool scaling_linear_relaxation_consistent(
    const Form& form, int prime, int coefficient_modulus) {
  const int classes = (prime - 1) / 2;
  const int vertices = prime + 1;
  const int variables = vertices * classes;
  const int generator = primitive_root(prime);
  std::vector<int> logarithm(prime, -1);
  int power = 1;
  for (int exponent = 0; exponent < prime - 1; ++exponent) {
    logarithm[power] = exponent % classes;
    power = power * generator % prime;
  }

  std::vector<std::vector<int>> equations;
  auto equation = [&]() {
    equations.emplace_back(variables + 1);
    return &equations.back();
  };

  for (int vertex = 0; vertex < vertices; ++vertex) {
    auto* row = equation();
    for (int value = 0; value < classes; ++value) {
      (*row)[vertex * classes + value] = 1;
    }
    (*row)[variables] = 1;
  }
  // Adding one common exponent to every lift preserves uniform row
  // multiplicities, so normalize the first lift to exponent zero.
  for (int value = 0; value < classes; ++value) {
    auto* row = equation();
    (*row)[value] = 1;
    (*row)[variables] = value == 0 ? 1 : 0;
  }

  for (int left = 0; left < vertices; ++left) {
    const Point left_point = curve_point(left, prime);
    for (int residue = 0; residue < classes; ++residue) {
      auto* row = equation();
      for (int right = 0; right < vertices; ++right) {
        if (left == right) {
          continue;
        }
        const int value =
            pairing(left_point, curve_point(right, prime), form, prime);
        if (value == 0) {
          continue;
        }
        int required = residue - logarithm[value];
        required %= classes;
        if (required < 0) {
          required += classes;
        }
        ++(*row)[right * classes + required];
      }
      (*row)[variables] = 2;
    }
  }

  int pivot_row = 0;
  for (int column = 0;
       column < variables && pivot_row < static_cast<int>(equations.size());
       ++column) {
    int pivot = pivot_row;
    while (pivot < static_cast<int>(equations.size()) &&
           equations[pivot][column] % coefficient_modulus == 0) {
      ++pivot;
    }
    if (pivot == static_cast<int>(equations.size())) {
      continue;
    }
    std::swap(equations[pivot], equations[pivot_row]);
    const int inverse =
        inverse_mod(equations[pivot_row][column], coefficient_modulus);
    for (int entry = column; entry <= variables; ++entry) {
      equations[pivot_row][entry] =
          equations[pivot_row][entry] * inverse % coefficient_modulus;
    }
    for (int row = 0; row < static_cast<int>(equations.size()); ++row) {
      if (row == pivot_row) {
        continue;
      }
      int multiplier = equations[row][column] % coefficient_modulus;
      if (multiplier < 0) {
        multiplier += coefficient_modulus;
      }
      if (multiplier == 0) {
        continue;
      }
      for (int entry = column; entry <= variables; ++entry) {
        equations[row][entry] =
            (equations[row][entry] -
             multiplier * equations[pivot_row][entry]) %
            coefficient_modulus;
      }
    }
    ++pivot_row;
  }
  for (const auto& row : equations) {
    bool all_zero = true;
    for (int column = 0; column < variables; ++column) {
      if (row[column] % coefficient_modulus != 0) {
        all_zero = false;
        break;
      }
    }
    if (all_zero && row[variables] % coefficient_modulus != 0) {
      return false;
    }
  }
  return true;
}

bool is_ordered_rainbow(
    const Form& form, const std::vector<int>& order, int prime) {
  for (int position = 0; position <= prime; ++position) {
    std::vector<bool> seen(prime, false);
    for (int other = 0; other <= prime; ++other) {
      if (other == position) {
        continue;
      }
      const int lower = std::min(position, other);
      const int upper = std::max(position, other);
      const int value = pairing(
          curve_point(order[lower], prime),
          curve_point(order[upper], prime),
          form,
          prime);
      seen[value] = true;
    }
    if (std::count(seen.begin(), seen.end(), true) != prime) {
      return false;
    }
  }
  return true;
}

struct Result {
  std::uint64_t forms = 0;
  std::uint64_t zero_pattern_survivors = 0;
  std::uint64_t signless_survivors = 0;
  std::uint64_t scaling_linear_survivors_mod2 = 0;
  std::uint64_t scaling_linear_survivors_mod3 = 0;
  std::uint64_t scaling_linear_survivors_mod5 = 0;
  std::uint64_t forms_with_an_order = 0;
};

Result exhaust(int prime, bool exhaust_orders) {
  const std::vector<Form> forms = projective_forms(prime);
  Result result;
  result.forms = forms.size();
  for (const Form& form : forms) {
    const int level = signless_row_level(form, prime);
    if (level == 0) {
      continue;
    }
    ++result.zero_pattern_survivors;
    if (scaling_linear_relaxation_consistent(form, prime, 2)) {
      ++result.scaling_linear_survivors_mod2;
    }
    if (scaling_linear_relaxation_consistent(form, prime, 3)) {
      ++result.scaling_linear_survivors_mod3;
    }
    if (scaling_linear_relaxation_consistent(form, prime, 5)) {
      ++result.scaling_linear_survivors_mod5;
    }
    if (level == 1) {
      continue;
    }
    ++result.signless_survivors;
    if (!exhaust_orders) {
      continue;
    }
    std::vector<int> order(prime + 1);
    std::iota(order.begin(), order.end(), 0);
    do {
      if (is_ordered_rainbow(form, order, prime)) {
        ++result.forms_with_an_order;
        break;
      }
    } while (std::next_permutation(order.begin(), order.end()));
  }
  return result;
}

}  // namespace

int main() {
  const Result p3 = exhaust(3, true);
  const Result p7 = exhaust(7, true);
  const Result p11 = exhaust(11, false);
  const Result p19 = exhaust(19, false);

  if (p3.forms != 364 || p3.zero_pattern_survivors != 24 ||
      p3.scaling_linear_survivors_mod2 != 24 ||
      p3.scaling_linear_survivors_mod3 != 24 ||
      p3.scaling_linear_survivors_mod5 != 24 ||
      p3.signless_survivors != 24 ||
      p3.forms_with_an_order != 21) {
    return 2;
  }
  if (p7.forms != 19608 || p7.zero_pattern_survivors != 49 ||
      p7.scaling_linear_survivors_mod2 != 49 ||
      p7.scaling_linear_survivors_mod3 != 49 ||
      p7.scaling_linear_survivors_mod5 != 49 ||
      p7.signless_survivors != 49 ||
      p7.forms_with_an_order != 0) {
    return 2;
  }
  if (p11.forms != 177156 || p11.zero_pattern_survivors != 55 ||
      p11.scaling_linear_survivors_mod2 != 55 ||
      p11.scaling_linear_survivors_mod3 != 0 ||
      p11.scaling_linear_survivors_mod5 != 0 ||
      p11.signless_survivors != 0) {
    return 2;
  }
  if (p19.forms != 2613660 || p19.zero_pattern_survivors != 171 ||
      p19.scaling_linear_survivors_mod2 != 171 ||
      p19.scaling_linear_survivors_mod3 != 0 ||
      p19.scaling_linear_survivors_mod5 != 0 ||
      p19.signless_survivors != 0) {
    return 2;
  }

  std::cout << "p=3: projective_forms=" << p3.forms
            << " zero_pattern=" << p3.zero_pattern_survivors
            << " scaling_linear_mod2=" << p3.scaling_linear_survivors_mod2
            << " mod3=" << p3.scaling_linear_survivors_mod3
            << " mod5=" << p3.scaling_linear_survivors_mod5
            << " signless=" << p3.signless_survivors
            << " ordered=" << p3.forms_with_an_order << "\n";
  std::cout << "p=7: projective_forms=" << p7.forms
            << " zero_pattern=" << p7.zero_pattern_survivors
            << " scaling_linear_mod2=" << p7.scaling_linear_survivors_mod2
            << " mod3=" << p7.scaling_linear_survivors_mod3
            << " mod5=" << p7.scaling_linear_survivors_mod5
            << " signless=" << p7.signless_survivors
            << " ordered=" << p7.forms_with_an_order << "\n";
  std::cout << "p=11: projective_forms=" << p11.forms
            << " zero_pattern=" << p11.zero_pattern_survivors
            << " scaling_linear_mod2=" << p11.scaling_linear_survivors_mod2
            << " mod3=" << p11.scaling_linear_survivors_mod3
            << " mod5=" << p11.scaling_linear_survivors_mod5
            << " signless=" << p11.signless_survivors << "\n";
  std::cout << "p=19: projective_forms=" << p19.forms
            << " zero_pattern=" << p19.zero_pattern_survivors
            << " scaling_linear_mod2=" << p19.scaling_linear_survivors_mod2
            << " mod3=" << p19.scaling_linear_survivors_mod3
            << " mod5=" << p19.scaling_linear_survivors_mod5
            << " signless=" << p19.signless_survivors << "\n";
  std::cout << "twisted-cubic alternating-link exhaustion: PASS\n";
}
