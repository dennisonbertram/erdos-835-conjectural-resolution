# Five-core families with at least three \(K_{3,3,1,1}\) cores

Date: 2026-07-27.

## Result and scope

Use
\[
 A=K_{5,1,1,1},\quad B=K_{3,3,1,1},\quad
 C=K_{3,1,1,1,1},\quad D=K_6.
\]
No family of exactly five distinct cores containing at least three
\(B\)-cores can collectively account for all seven blocked size-ten
supports in the exceptional \(r=0\) profile.

There are exactly nine capacity-sufficient type multisets in this scope:
\[
 AB^4,\ CB^4,\ DB^4,\quad
 A^2B^3,\ ACB^3,\ ADB^3,\ C^2B^3,\ CDB^3,\ D^2B^3. \tag{1}
\]
The all-\(B\) multiset has total individual reuse capacity five and needs
no enumeration.

This is a cover impossibility result, not a non-coexistence result.  It
does not address five-core families containing at most two \(B\)-cores or
families of six or more distinct cores.

## Exact subset-capacity screen

Fix a canonical \(B\)-core under \(S_{13}\).  Enumerate the remaining
cores from the exact compatible pools
\[
 |N_A(B)|=38,\quad |N_B(B)|=81,\quad
 |N_C(B)|=214,\quad |N_D(B)|=27.
\]
Partial unions are rejected as soon as they violate a necessary prefix
graph condition.  For every retained five-core union, enumerate the only
possible positive multiplicity shapes,
\[
 3+1+1+1+1\quad\text{or}\quad2+2+1+1+1,
\]
and impose the complement-capacity inequality on all 31 nonempty
subfamilies.  Every row has zero surviving multiplicity assignments.

The exact numbers of families reaching the final multiplicity test are
\[
\begin{array}{c|r@{\qquad}c|r@{\qquad}c|r}
AB^4&7{,}620&CB^4&48{,}180&DB^4&8{,}964\\
A^2B^3&6{,}210&ACB^3&118{,}584&ADB^3&20{,}808\\
C^2B^3&330{,}552&CDB^3&116{,}856&D^2B^3&8{,}550
\end{array}
\]

## Reproduction and frontier

`verify_r0_four_core_capacity.py` accepts either four or five core types
and reproduces every row deterministically.  For example,

```text
python3 -B verify_r0_four_core_capacity.py \
  3311 3311 3311 31111 31111
```

Thus an exactly-five-core total obstruction can contain at most two
\(K_{3,3,1,1}\) cores.  All other five-core type multisets remain open.
