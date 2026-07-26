// Independent exact verifier for the finite 2-adic XOR window at r = 15.
//
// This program checks the cancelled numerator modulo 2^31 for every
// 0 <= j <= 570344 and every layer d = 0,...,31.  The middle-layer
// internal branch then follows from the proved Delta lemma.
//
// It intentionally uses a different implementation from the Python/Fable
// verifier:
//   * three NTT primes and exact unsigned-128-bit CRT;
//   * coefficients represented modulo 2^31 (not modulo 2^47);
//   * the exact w <-> 31-w parity pairing before layer assembly;
//   * independent cpp_int checks of every cofactor and the trivial series
//     through degree 400.
//
// Build (macOS/Homebrew):
//   clang++ -O3 -std=c++20 -I/opt/homebrew/include \
//     evidence/verify_s141531_higher_xor_window.cpp \
//     -L/opt/homebrew/lib -lcrypto \
//     -o /private/tmp/verify_s141531_higher_xor_window
//
// Run:
//   /private/tmp/verify_s141531_higher_xor_window

#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

#include <boost/multiprecision/cpp_int.hpp>
#include <openssl/sha.h>

using boost::multiprecision::cpp_int;
using u128 = unsigned __int128;

namespace {

constexpr uint32_t MOD2 = uint32_t{1} << 31;
constexpr uint32_t MASK2 = MOD2 - 1;
constexpr int V = 31;
constexpr int R = 15;
constexpr int M = 570285;
constexpr int L = M + 59;
constexpr int NTT_N = 1 << 20;
constexpr int CROSS_J = 400;

struct Prime {
  uint32_t p;
  uint32_t primitive_root;
};

constexpr std::array<Prime, 3> PRIMES{{
    {998244353U, 3U},
    {1004535809U, 3U},
    {469762049U, 3U},
}};

uint64_t choose_small(int n, int k) {
  if (k < 0 || k > n) return 0;
  k = std::min(k, n - k);
  uint64_t ans = 1;
  for (int i = 1; i <= k; ++i) {
    ans = ans * uint64_t(n - k + i) / uint64_t(i);
  }
  return ans;
}

uint32_t pow_mod(uint32_t a, uint64_t e, uint32_t mod) {
  uint64_t x = a;
  uint64_t out = 1;
  while (e) {
    if (e & 1) out = out * x % mod;
    x = x * x % mod;
    e >>= 1;
  }
  return uint32_t(out);
}

uint32_t inv_odd_mod_2_31(uint32_t a) {
  assert(a & 1U);
  // Newton iteration in Z/2^32Z; masking at the end gives the inverse
  // modulo 2^31 as well.
  uint32_t x = a;
  for (int i = 0; i < 5; ++i) x *= 2U - a * x;
  return x & MASK2;
}

std::vector<uint32_t> binom_mod_2_31(int n, int upto = -1) {
  if (upto < 0 || upto > n) upto = n;
  std::vector<uint32_t> out(size_t(upto) + 1);
  uint64_t odd = 1;
  int exponent = 0;
  out[0] = 1;
  for (int i = 1; i <= upto; ++i) {
    uint32_t x = uint32_t(n - i + 1);
    while ((x & 1U) == 0) {
      x >>= 1;
      ++exponent;
    }
    uint32_t y = uint32_t(i);
    while ((y & 1U) == 0) {
      y >>= 1;
      --exponent;
    }
    assert(exponent >= 0);
    odd = (odd * x) & MASK2;
    odd = (odd * inv_odd_mod_2_31(y)) & MASK2;
    out[size_t(i)] =
        exponent >= 31 ? 0U : uint32_t((odd << exponent) & MASK2);
  }
  return out;
}

void ntt(std::vector<uint32_t>& a, const Prime prime, bool invert) {
  const size_t n = a.size();
  for (size_t i = 1, j = 0; i < n; ++i) {
    size_t bit = n >> 1;
    while (j & bit) {
      j ^= bit;
      bit >>= 1;
    }
    j ^= bit;
    if (i < j) std::swap(a[i], a[j]);
  }

  for (size_t len = 2; len <= n; len <<= 1) {
    uint32_t root =
        pow_mod(prime.primitive_root, (prime.p - 1) / len, prime.p);
    if (invert) root = pow_mod(root, prime.p - 2, prime.p);
    for (size_t start = 0; start < n; start += len) {
      uint64_t w = 1;
      const size_t half = len >> 1;
      for (size_t j = 0; j < half; ++j) {
        const uint32_t u = a[start + j];
        const uint32_t v =
            uint32_t(uint64_t(a[start + j + half]) * w % prime.p);
        uint32_t plus = u + v;
        if (plus >= prime.p) plus -= prime.p;
        const uint32_t minus = u >= v ? u - v : u + prime.p - v;
        a[start + j] = plus;
        a[start + j + half] = minus;
        w = w * root % prime.p;
      }
    }
  }

  if (invert) {
    const uint32_t n_inv = pow_mod(uint32_t(n % prime.p),
                                   prime.p - 2, prime.p);
    for (uint32_t& x : a) x = uint32_t(uint64_t(x) * n_inv % prime.p);
  }
}

std::vector<uint32_t> convolution_mod_2_31(
    const std::vector<uint32_t>& x,
    const std::vector<uint32_t>& y) {
  assert(x.size() + y.size() - 1 == size_t(M + 1));
  std::array<std::vector<uint32_t>, 3> residues;
  for (size_t q = 0; q < PRIMES.size(); ++q) {
    const Prime prime = PRIMES[q];
    std::vector<uint32_t> fx(NTT_N, 0), fy(NTT_N, 0);
    for (size_t i = 0; i < x.size(); ++i) fx[i] = x[i] % prime.p;
    for (size_t i = 0; i < y.size(); ++i) fy[i] = y[i] % prime.p;
    ntt(fx, prime, false);
    ntt(fy, prime, false);
    for (int i = 0; i < NTT_N; ++i) {
      fx[size_t(i)] =
          uint32_t(uint64_t(fx[size_t(i)]) * fy[size_t(i)] % prime.p);
    }
    ntt(fx, prime, true);
    residues[q] = std::move(fx);
  }

  const uint64_t p1 = PRIMES[0].p;
  const uint64_t p2 = PRIMES[1].p;
  const uint64_t p3 = PRIMES[2].p;
  const uint64_t p12 = p1 * p2;
  const uint32_t inv_p1_mod_p2 =
      pow_mod(uint32_t(p1 % p2), uint32_t(p2 - 2), uint32_t(p2));
  const uint32_t inv_p12_mod_p3 =
      pow_mod(uint32_t(p12 % p3), uint32_t(p3 - 2), uint32_t(p3));

  std::vector<uint32_t> out(M + 1);
  for (int i = 0; i <= M; ++i) {
    const uint64_t r1 = residues[0][size_t(i)];
    const uint64_t r2 = residues[1][size_t(i)];
    const uint64_t r3 = residues[2][size_t(i)];
    const uint64_t diff2 = (r2 + p2 - r1 % p2) % p2;
    const uint64_t t2 = diff2 * inv_p1_mod_p2 % p2;
    const uint64_t x12 = r1 + p1 * t2;
    const uint64_t diff3 = (r3 + p3 - x12 % p3) % p3;
    const uint64_t t3 = diff3 * inv_p12_mod_p3 % p3;
    const u128 exact_residue = u128(x12) + u128(p12) * t3;
    out[size_t(i)] = uint32_t(exact_residue & MASK2);
  }
  return out;
}

std::string sha256_words(const std::vector<uint32_t>& words) {
  SHA256_CTX ctx;
  SHA256_Init(&ctx);
  for (const uint32_t x : words) {
    const std::array<unsigned char, 4> little{{
        static_cast<unsigned char>(x),
        static_cast<unsigned char>(x >> 8),
        static_cast<unsigned char>(x >> 16),
        static_cast<unsigned char>(x >> 24),
    }};
    SHA256_Update(&ctx, little.data(), little.size());
  }
  std::array<unsigned char, SHA256_DIGEST_LENGTH> digest{};
  SHA256_Final(digest.data(), &ctx);
  std::ostringstream out;
  out << std::hex << std::setfill('0');
  for (unsigned char c : digest) out << std::setw(2) << unsigned(c);
  return out.str();
}

std::string sha256_text(const std::string& text) {
  std::array<unsigned char, SHA256_DIGEST_LENGTH> digest{};
  SHA256(reinterpret_cast<const unsigned char*>(text.data()), text.size(),
         digest.data());
  std::ostringstream out;
  out << std::hex << std::setfill('0');
  for (unsigned char c : digest) out << std::setw(2) << unsigned(c);
  return out.str();
}

std::array<int64_t, V + 1> forced_phi(int64_t& b) {
  std::array<int64_t, R> lambda{};
  for (int s = 0; s < R; ++s) {
    const uint64_t numerator = choose_small(V - s, R - 1 - s);
    assert(numerator % uint64_t(R - s) == 0);
    lambda[size_t(s)] = int64_t(numerator / uint64_t(R - s));
  }
  b = lambda[0];

  std::array<int64_t, V + 1> phi{};
  for (int w = 0; w <= R; ++w) {
    int64_t value = 0;
    const int limit = std::min(w, R - 1);
    for (int s = 0; s <= limit; ++s) {
      const int64_t sign_power =
          (s & 1) ? -int64_t(1ULL << s) : int64_t(1ULL << s);
      value += sign_power * int64_t(choose_small(w, s)) * lambda[size_t(s)];
    }
    phi[size_t(w)] = value;
  }
  for (int w = R + 1; w <= V; ++w) phi[size_t(w)] = -phi[size_t(V - w)];
  return phi;
}

std::array<std::array<int64_t, V + 1>, V + 1> kraw_small() {
  std::array<std::array<int64_t, V + 1>, V + 1> out{};
  for (int d = 0; d <= V; ++d) {
    for (int w = 0; w <= V; ++w) {
      int64_t value = 0;
      for (int h = 0; h <= w; ++h) {
        if (h > d || w - h > V - d) continue;
        const int64_t term =
            int64_t(choose_small(d, h) * choose_small(V - d, w - h));
        value += (h & 1) ? -term : term;
      }
      out[size_t(d)][size_t(w)] = value;
    }
  }
  return out;
}

std::vector<cpp_int> binom_exact_prefix(int n, int upto) {
  std::vector<cpp_int> out(size_t(upto) + 1);
  out[0] = 1;
  for (int j = 1; j <= upto; ++j) {
    out[size_t(j)] =
        out[size_t(j - 1)] * (n - j + 1) / j;
  }
  return out;
}

uint32_t low_31(cpp_int value) {
  static const cpp_int modulus = cpp_int(1) << 31;
  value %= modulus;
  if (value < 0) value += modulus;
  return value.convert_to<uint32_t>();
}

std::vector<cpp_int> kraw_exact(int64_t F, int64_t b, int upto) {
  std::vector<cpp_int> out(size_t(upto) + 1);
  out[0] = 1;
  if (upto == 0) return out;
  out[1] = F;
  for (int j = 1; j < upto; ++j) {
    cpp_int numerator =
        F * out[size_t(j)] - (b - j + 1) * out[size_t(j - 1)];
    assert(numerator % (j + 1) == 0);
    out[size_t(j + 1)] = numerator / (j + 1);
  }
  return out;
}

uint32_t signed_mod_2_31(int64_t x) {
  const int64_t reduced = x % int64_t(MOD2);
  return uint32_t(reduced < 0 ? reduced + MOD2 : reduced);
}

}  // namespace

int main() {
  const auto started = std::chrono::steady_clock::now();

  int64_t b = 0;
  const auto phi = forced_phi(b);
  const int64_t F0 = phi[R];
  const int64_t F1 = F0 - (int64_t(1) << R);
  assert(b == 17678835);
  assert(b / 31 == M);
  assert(F0 == 1549 && F1 == -31219);
  const int A = int((b - M) / 2);
  assert(2LL * A + M == b);

  const long double log_bound =
      std::log2(static_cast<long double>(M + 1)) + 62.0L;
  long double log_prime_product = 0;
  for (const Prime q : PRIMES) log_prime_product += std::log2(q.p);
  assert(log_prime_product > log_bound);

  std::set<int> signed_args;
  for (int w = 1; w < V; ++w) signed_args.insert(int(phi[size_t(w)]));
  signed_args.insert(int(F0));
  signed_args.insert(int(F1));
  std::set<int> abs_args;
  for (int F : signed_args) abs_args.insert(std::abs(F));
  const std::set<int> expected_abs{
      429, 627, 1197, 1549, 3059, 10925, 31219, 58995, 570285};
  assert(abs_args == expected_abs);

  std::cout << "r=15 finite XOR window, independent C++ verifier\n";
  std::cout << "b=" << b << ", M=" << M << ", A=" << A
            << ", threshold=" << M + 30 << ", checked through " << L << "\n";
  std::cout << "CRT log2(product)=" << std::fixed << std::setprecision(3)
            << double(log_prime_product) << ", coefficient bound <2^"
            << double(log_bound) << "\n";

  std::map<int, std::vector<uint32_t>> U;
  std::map<int, std::string> u_hashes;
  for (const int abs_F : abs_args) {
    const int aa = (M + abs_F) / 2;
    const int cc = (M - abs_F) / 2;
    auto left = binom_mod_2_31(aa);
    auto right = binom_mod_2_31(cc);
    for (size_t j = 1; j < right.size(); j += 2) {
      if (right[j]) right[j] = MOD2 - right[j];
    }
    auto positive = convolution_mod_2_31(left, right);
    auto negative = positive;
    for (size_t j = 1; j < negative.size(); j += 2) {
      if (negative[j]) negative[j] = MOD2 - negative[j];
    }
    u_hashes[abs_F] = sha256_words(positive);
    U[abs_F] = std::move(positive);
    U[-abs_F] = std::move(negative);
    std::cout << "  U_" << abs_F << " sha256=" << u_hashes[abs_F] << "\n";
  }

  // Cross-check 1: independent exact bigint cofactors through degree 400.
  for (const int abs_F : abs_args) {
    const int aa = (M + abs_F) / 2;
    const int cc = (M - abs_F) / 2;
    const auto left = binom_exact_prefix(aa, CROSS_J);
    const auto right = binom_exact_prefix(cc, CROSS_J);
    for (int j = 0; j <= CROSS_J; ++j) {
      cpp_int coefficient = 0;
      for (int i = 0; i <= j; ++i) {
        cpp_int term = left[size_t(i)] * right[size_t(j - i)];
        coefficient += ((j - i) & 1) ? -term : term;
      }
      assert(U[abs_F][size_t(j)] == low_31(coefficient));
      if (j & 1) coefficient = -coefficient;
      assert(U[-abs_F][size_t(j)] == low_31(coefficient));
    }
  }
  std::cout << "[ok] all 9 positive and negative U_F match cpp_int through j="
            << CROSS_J << "\n";

  // The on-parity trivial-character residual:
  // 2(1+z)^M ((1+z)/(1-z))^A, truncated modulo 2^31 after rho=29.
  std::vector<uint32_t> S(size_t(L) + 1, 0);
  std::vector<uint32_t> Ar(size_t(L) + 1, 0);
  const auto choose_M = binom_mod_2_31(M);
  std::copy(choose_M.begin(), choose_M.end(), Ar.begin());
  const auto choose_A_prefix = binom_mod_2_31(A, 29);
  for (int rho = 0; rho < 30; ++rho) {
    const uint32_t two =
        rho + 1 >= 31 ? 0U : uint32_t(uint64_t(1) << (rho + 1));
    const uint32_t factor =
        uint32_t(uint64_t(two) * choose_A_prefix[size_t(rho)] & MASK2);
    for (int j = rho; j <= L; ++j) {
      const uint64_t add =
          uint64_t(factor) * Ar[size_t(j - rho)];
      S[size_t(j)] =
          uint32_t((uint64_t(S[size_t(j)]) + add) & MASK2);
    }
    uint32_t running = 0;
    for (int j = 0; j <= L; ++j) {
      running = uint32_t((uint64_t(running) + Ar[size_t(j)]) & MASK2);
      Ar[size_t(j)] = running;
    }
  }
  const std::string s_hash = sha256_words(S);
  std::cout << "  S sha256=" << s_hash << "\n";

  // Cross-check 2: exact quotient expansion through degree 400.
  const auto plus_exact = binom_exact_prefix(M + A, CROSS_J);
  std::vector<cpp_int> minus_exact(size_t(CROSS_J) + 1);
  minus_exact[0] = 1;
  for (int j = 1; j <= CROSS_J; ++j) {
    minus_exact[size_t(j)] =
        minus_exact[size_t(j - 1)] * (A + j - 1) / j;
  }
  for (int j = 0; j <= CROSS_J; ++j) {
    cpp_int coefficient = 0;
    for (int i = 0; i <= j; ++i) {
      coefficient += plus_exact[size_t(i)] * minus_exact[size_t(j - i)];
    }
    coefficient *= 2;
    assert(S[size_t(j)] == low_31(coefficient));
  }
  std::cout << "[ok] trivial residual S matches cpp_int through j="
            << CROSS_J << "\n";

  const auto KW = kraw_small();
  const std::vector<uint32_t>& delta_U = U.at(int(F1));
  std::array<uint64_t, V + 1> violations{};
  std::array<int, V + 1> first_violation{};
  first_violation.fill(-1);
  uint64_t conditions = 0;

  // Pair w with 31-w.  Since phi(31-w)=-phi(w),
  // K_{31-w}(d)=(-1)^d K_w(d), and U_{-F,j}=(-1)^j U_{F,j},
  // the radial part is exactly zero off parity and twice the w=1..15
  // half on parity.
  for (int d = 0; d <= V; ++d) {
    const int64_t corr =
        d == R ? F0 : (d == R + 1 ? -F0 : phi[size_t(d)]);
    const uint32_t corr2 =
        uint32_t(uint64_t(2) * signed_mod_2_31(corr) & MASK2);
    for (int j = 0; j <= L; ++j) {
      if ((j + d) & 1) continue;
      ++conditions;
      uint64_t residue = S[size_t(j)];
      if (j <= M) {
        for (int w = 1; w <= R; ++w) {
          const uint32_t coefficient =
              uint32_t(uint64_t(2) *
                       signed_mod_2_31(KW[size_t(d)][size_t(w)]) &
                       MASK2);
          residue += uint64_t(coefficient) *
                     U.at(int(phi[size_t(w)]))[size_t(j)];
          residue &= MASK2;
        }
        const uint32_t du =
            uint32_t((uint64_t(delta_U[size_t(j)]) + MOD2 -
                      U.at(int(F0))[size_t(j)]) &
                     MASK2);
        residue += uint64_t(corr2) * du;
        residue &= MASK2;
      }
      if (residue != 0) {
        ++violations[size_t(d)];
        if (first_violation[size_t(d)] < 0) first_violation[size_t(d)] = j;
      }
    }
    std::cout << "  layer d=" << std::setw(2) << d
              << ": violations=" << violations[size_t(d)];
    if (first_violation[size_t(d)] >= 0) {
      std::cout << ", first j=" << first_violation[size_t(d)];
    }
    std::cout << "\n";
  }

  // Cross-check 3: the uncancelled exact numerator on every layer through
  // degree 400.  This uses the Krawtchouk recurrence at length b and shares
  // no NTT or tail-cancellation arithmetic with the full-window check.
  std::set<int64_t> exact_args;
  exact_args.insert(b);
  exact_args.insert(F1);
  for (int w = 1; w < V; ++w) exact_args.insert(phi[size_t(w)]);
  std::map<int64_t, std::vector<cpp_int>> K;
  for (const int64_t F : exact_args) K[F] = kraw_exact(F, b, CROSS_J);
  for (int j = 0; j <= CROSS_J; ++j) {
    for (int d = 0; d <= V; ++d) {
      cpp_int numerator =
          ((j + d) & 1) ? cpp_int(0) : 2 * K[b][size_t(j)];
      for (int w = 1; w < V; ++w) {
        numerator += KW[size_t(d)][size_t(w)] *
                     K[phi[size_t(w)]][size_t(j)];
      }
      if (((j + d) & 1) == 0) {
        const int64_t corr =
            d == R ? F0 : (d == R + 1 ? -F0 : phi[size_t(d)]);
        numerator +=
            2 * corr *
            (K[F1][size_t(j)] - K[F0][size_t(j)]);
      }
      assert(low_31(numerator) == 0);
    }
  }
  std::cout << "[ok] uncancelled cpp_int numerators vanish mod 2^31 for all "
            << "32 layers through j=" << CROSS_J << "\n";

  uint64_t total_violations = 0;
  for (uint64_t n : violations) total_violations += n;
  std::ostringstream certificate_material;
  certificate_material << "conditions=" << conditions
                       << ";violations=" << total_violations
                       << ";S=" << s_hash;
  for (const auto& [F, hash] : u_hashes) {
    certificate_material << ";U_" << F << "=" << hash;
  }
  for (int d = 0; d <= V; ++d) {
    certificate_material << ";d" << d << "=" << violations[size_t(d)];
  }
  const std::string certificate = sha256_text(certificate_material.str());

  const auto elapsed = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - started);
  std::cout << "conditions checked=" << conditions
            << ", total violations=" << total_violations << "\n";
  std::cout << "certificate material: " << certificate_material.str() << "\n";
  std::cout << "certificate sha256=" << certificate << "\n";
  std::cout << "elapsed_seconds=" << std::fixed << std::setprecision(3)
            << elapsed.count() << "\n";

  if (total_violations != 0) {
    std::cerr << "WINDOW VERDICT: FAIL\n";
    return 1;
  }
  std::cout << "WINDOW VERDICT: PASS\n";
  return 0;
}
