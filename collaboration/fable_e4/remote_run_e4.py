#!/usr/bin/env python3
"""Self-contained exact analysis of the e4-refined moment-curve graphs G_r.

SEARCH/ANALYSIS CODE -- not a certificate.  See PROOF.md (Theorems A-C) for
the mathematics this implements:

  * G_r (states (a, a^2, a^3, a^4+r, lambda), actual Johnson edges) is
    exactly the union, over 17-sets R in F_32 with e1=e2=e3=0 and e4=r, of
    the labelled cliques K17 on {(a, lambda_R(a)) : a in R},
    lambda_R(a) = r a^4 + e5(R) a^3 + e6(R) a^2 + e7(R) a + e8(R).
  * Scaling gives G_1 iso G_r for every r != 0, so only G_0, G_1 matter.

This script enumerates every such R exactly (meet-in-the-middle, verified
against an alternate split and re-verified from scratch), cross-checks the
496 static K32 witness masks, computes exact clique numbers of G_0 and G_1,
decides whether any K18 with the K32's layer pattern survives for any r,
and reports DSATUR/greedy colouring upper bounds.

The inlined EDGE_WITNESS_MASK_ROWS table is copied verbatim from
evidence/f32_four_statistic_k32_verifier.py (untracked there, hence inlined).
"""

from __future__ import annotations

import random
import sys
import time
from itertools import combinations

sys.setrecursionlimit(100000)

MODULUS = 0b100101  # X^5 + X^2 + 1

EDGE_WITNESS_MASK_ROWS = (
    (0x1FD55893, 0x12DEB785, 0xDB655C49, 0xAFA05F51, 0xA9B8BD61, 0xAFA05F51, 0xC5BD4EA1, 0xC8ADE3E1, 0x793D3B81, 0xEC3E6D41, 0xF505AFA1, 0x315D9DA5, 0x6574BD61, 0x388CDF95, 0x88EEEE89, 0xA29B5BC9, 0xE9BA0B59, 0xB85FD291, 0xD30DEC99, 0xCD7C1599, 0x793D3B81, 0xF96F0961, 0x529BABC9, 0xA9B8BD61, 0x5B9BDC21, 0xA6E2E791, 0xF96F0961, 0xD8E89FA1, 0xA6E2E791, 0xC5E1CF15, 0xA9B8BD61,),
    (0x499BA72E, 0x5C8D697A, 0xA90A7DB6, 0x499BA72E, 0xEB996C4A, 0x7DD72883, 0x695CE1E6, 0xAF59E283, 0xEA7A0796, 0x13E6EA4B, 0x2E637E32, 0xD629761E, 0xE5C7CE12, 0xDB909AE3, 0x4C67D596, 0x2E637E32, 0x61D5BC53, 0xCE2CABE2, 0x695CE1E6, 0x5479B5C3, 0x7345DF42, 0x8B8BE2E3, 0xAF59E283, 0xC6D8EEC2, 0x5E43F84E, 0x5C8D697A, 0x1DD12EE3, 0xA2FE4F12, 0x56D1E752, 0xB77142E3,),
    (0xD93D548D, 0x25F7321E, 0xB4A5FA26, 0xA49BBCE4, 0x3CC333CD, 0x2A7A1FE4, 0xF0E8FA1C, 0x3C14DD5E, 0xEC6B6D14, 0xB31A32FC, 0xB4A5FA26, 0xBE0CD29E, 0xA6FCFA04, 0x650FDD46, 0x7F83526C, 0xD2EE24BC, 0xC3CFB116, 0x287EACF4, 0xAE76869C, 0xCF4153DC, 0xF885D6CC, 0x93AA6F94, 0x4B2ECFA4, 0xBE0CD29E, 0xBC9710F6, 0xB31A32FC, 0x3DEA26CC, 0xD5ECB384, 0xA6FCFA04,),
    (0xC4E50B7E, 0x2B7D9568, 0x72F34D68, 0xF5D842F8, 0x63699FA8, 0x8C8FA73C, 0x677C15CC, 0xAF56B829, 0x677C15CC, 0xB46335EC, 0x6C2B59DC, 0xEA79EA88, 0x3773B60C, 0x72F34D68, 0xA68DF92C, 0x1C1FC75C, 0x21F5173D, 0xDA75E948, 0xC45EBAB8, 0x529BABC9, 0x3773B60C, 0x72CF7168, 0xED1B36A8, 0x1C1FAECA, 0x77828BBC, 0xBCF48ACC, 0x63699FA8, 0x9BAB7A88,),
    (0x74AC63B5, 0xBE9F4854, 0x59A5DDD0, 0x453DF1D2, 0x1BAF5370, 0x81DDF698, 0xDFCD8930, 0x45DA38FC, 0xC458F79A, 0xE4D1C63E, 0xDD4DAC54, 0x4ECF1732, 0xDDC6AA1A, 0xFF448B58, 0x9FAC0F98, 0xAD76F118, 0x0FF03C3D, 0xDFCD8930, 0x2CF719F0, 0xC5FC6A34, 0x56EB9670, 0x2CF719F0, 0xCA9A5F32, 0xB2655A7C, 0xBA73D314, 0xE4D1C63E, 0xFF448B58,),
    (0x4FDA3760, 0xBEC078F8, 0xE0917F3C, 0xCD46A778, 0x966AEDE0, 0x89077F3C, 0x73DAF460, 0xBEC078F8, 0x367847F8, 0x1271BDB9, 0x131FAE3A, 0xB65267E4, 0x5DA4B9E4, 0x73DAF460, 0x73DAF460, 0x63FF09A8, 0xB3F48A3C, 0x81EB9CF8, 0xEB8B56A1, 0xAE2F9B28, 0x367847F8, 0x1EF67438, 0x5AE756B0, 0x37436EB1, 0x5479B53C, 0xFA6CA964,),
    (0x172895FE, 0xFB1C31E4, 0x7DC57252, 0xA9AADDD0, 0x383D9BCA, 0x83F7BAC0, 0x1D56F670, 0xDEC644F8, 0xDF0189FC, 0x979B7948, 0x72F34D68, 0x5D0EB94E, 0xACFC6552, 0x875C7D58, 0xB77890F4, 0x5BE3A1E8, 0xF6A333C2, 0x99A5665B, 0xE6CB9744, 0xBC9E01DD, 0xEB112BEC, 0xFC30F3C1, 0x707576D8, 0x72F34D68, 0x89347FF0,),
    (0xFA5F05A1, 0x688F67E8, 0xD5E3BC84, 0x96C93FA2, 0xFCA636C8, 0xBEC078F8, 0x6636CFA2, 0xFA9C95A8, 0x7B0F8B98, 0xBD56C585, 0x89EF2F84, 0x1ABCCEF0, 0x24747BB3, 0xDB6614F2, 0xC3C30FF1, 0xD9EA4CB2, 0xA3E2E1AE, 0x6BF298CC, 0xA669EED0, 0xAD54B9E4, 0x5792B3D2, 0x3F90C3AE, 0xFD3494AC, 0xDB6614F2,),
    (0xB57037A9, 0x4F078F6C, 0x52B3E9AC, 0x49C7756C, 0x4A4FB3E2, 0xEC37D930, 0xF8BAAB24, 0x11A5CFEC, 0xEFDA51C0, 0x56D70F2A, 0x8ECC7B38, 0x1EF9D192, 0xF1B3CB44, 0x2CFB9D88, 0x0BB637E2, 0x39A3DBB0, 0x539AAFA4, 0xEFDA51C0, 0x8E3A3F46, 0x53E71B38, 0xEFDA51C0, 0xEC37D930, 0xD0A76BB8,),
    (0xB3C1C7D2, 0xA336EB70, 0xA3955F54, 0xA336EB70, 0x9D8AFB84, 0x7156AA7C, 0x7A153BF0, 0xA363BE70, 0x82DD8EEC, 0x1D694EF8, 0x9B9D4AB2, 0x1B24FF94, 0x7CC73E84, 0x92B57FC0, 0x716F931A, 0xC73E2AD2, 0xA4D3BA69, 0x185FEE94, 0x75B03B5A, 0xF0E8FA1C, 0xC7256ED8, 0x9E54B6D8,),
    (0x3EE64CA9, 0xF59C5664, 0xD1B2EEB0, 0x801AFEFC, 0xF9AAB470, 0xFC39278A, 0x6D4FEC30, 0x59AFBE20, 0x966AEDE0, 0x2CFE07D4, 0x033FFCC1, 0x56D17E34, 0x178BBEE0, 0x815C5FEA, 0xBB2BAC54, 0x4F1A76B4, 0xCD76BC06, 0xF1DCBC90, 0x71B7742A, 0xF59C5664, 0xB9CE9D14,),
    (0x9E57F8C0, 0xA336EB70, 0xC3F56CC2, 0xF8579EC0, 0x55933FC4, 0x8A1F5EAC, 0xAEB54A6C, 0x583DEAE8, 0xC7BF290A, 0x50E4DBF8, 0xDFCD8930, 0x3DD98CAA, 0x7DB4EE40, 0x0FE8FA1C, 0x6555EED0, 0xF8579EC0, 0xDCA1CED4, 0xA7C72CB2, 0x66F56C98, 0xAADB9AB0,),
    (0x1389FDA5, 0xCA4BF38C, 0x6426FB74, 0x6E971AE2, 0x6AF65C58, 0x2DDE3961, 0x73DAF460, 0x73DAF460, 0x5E389799, 0x677C15CC, 0x9EF25DC0, 0x5D98B9D8, 0xDF38B065, 0x4597F178, 0xCD76BC06, 0xB31A32FC, 0x6470D5FC, 0xF59C5664, 0xCC2BFA1C,),
    (0x38EC6D2E, 0x2DB8FC98, 0x070B7F4E, 0xA883FBE2, 0xE9252F74, 0x4A4FB3E2, 0x6D94B5E8, 0x80E9BFE4, 0x06EE6A7C, 0xC0F330FD, 0xAB9BBA48, 0x0FDDE258, 0xC7253B72, 0x4C10FDFA, 0xF9AC6998, 0xAF592EB0, 0xE7DD6068, 0x89347FF0,),
    (0x53E2D26D, 0xEF256BA0, 0xDAB6D548, 0x87C5D794, 0x65DE4B98, 0xD575D584, 0x9FACF098, 0x7DCA72A2, 0xAFEDC380, 0x8DB2F9C8, 0x6F8BE858, 0x65DE4B98, 0xF9AFD880, 0xFC30F3C1, 0x33715F1C, 0xEC37D930, 0x9DDF5184,),
    (0x838FA7CC, 0x4C07FEB4, 0xA767B944, 0x7B69E268, 0xB4F0AF26, 0x0FA6ED4A, 0x9978BE92, 0x3BE5A878, 0xA3E2E1AE, 0x838FA7CC, 0x55E7A6B0, 0xF8579EC0, 0xD7BB8E20, 0x390CB7EA, 0x7B3CE2C2, 0xA6FCFA04,),
    (0x59EB0F19, 0xF4759B28, 0xE34F683A, 0xD4BDDD10, 0xD5B9E684, 0xF6C53C54, 0x56D7AA70, 0x3773B60C, 0x77A384F4, 0x2F3B91B8, 0xEE2D4D2A, 0x3F03C0FD, 0xFE4516AC, 0xE34F683A, 0xCE896774,),
    (0x9ADE8754, 0xBE8B6538, 0x2F1A5DCC, 0x4FF7806C, 0x4AE3F8C9, 0x57AB7A44, 0x9737F1A0, 0xB3C78AF0, 0xEFDA51C0, 0x4FF7806C, 0x336AB7E0, 0xEFDA51C0, 0x72F34D68, 0xBEA3E461,),
    (0x25BF91C9, 0x7C37CE84, 0x16BF52C6, 0xDCE5B582, 0xE4BE48B6, 0xCDF497A0, 0xD62FA25A, 0xDC0DB93C, 0x7C37CE84, 0x936F87D0, 0xB9377330, 0x67A4379C, 0xFF448B58,),
    (0x73DAF460, 0xB4EE42BC, 0x59ED4B68, 0x8F8F29E4, 0x5FAFA051, 0xCBFBE048, 0x65DE4B98, 0x6B5E23E8, 0xD6DCD922, 0xE58F3760, 0xF44FB60C, 0xB46C537A,),
    (0x94B345FA, 0x7EF96A20, 0xFCFC0C0D, 0x1DFC3C4A, 0x9BBA34E4, 0xBF34BAC0, 0x7FB531A0, 0xB6F701D8, 0x6E15C7E8, 0xD29FD138, 0x80BFA4FC,),
    (0xE1E20CFE, 0x1DBD4D8A, 0x53AFD186, 0x033FFCC1, 0x1DFC5A2C, 0x4FF7806C, 0x16BF52C6, 0x7E638E0B, 0xF06ADE4A, 0xE6E91AD8,),
    (0x7DCA72A2, 0x3FD26AE0, 0x7A5ED930, 0xF67B4438, 0xC9CC6FA8, 0x585D9D33, 0x277778B0, 0x76C1ECF0, 0x8CF24FA6,),
    (0x3DD98CAA, 0xCF968173, 0x2CF719F0, 0x59ED87A4, 0x75B03B5A, 0x33F53668, 0xD2E178B5, 0xB18EF9C8,),
    (0x4FEA198E, 0x77B4D44C, 0x3F3F3031, 0x3574E1AE, 0x33CCC33D, 0xD3642FCC, 0xF98DA3B0,),
    (0x367847F8, 0x5B139B78, 0x137FD0B2, 0xBAA16BE8, 0x56D1E752, 0xCEAB7A22,),
    (0xCDA2E5D1, 0x576D4A71, 0xEFDA51C0, 0xCE2C3D74, 0xDC5B9E18,),
    (0x9F36ED10, 0x2FCEF414, 0xF8CBC836, 0xFD61C1AC,),
    (0x71B7742A, 0xDBC9B238, 0xD910D6EE,),
    (0xF6AC6698, 0xB12BF992,),
    (0xD79A18F1,),
    (),
)


def _mul(left: int, right: int) -> int:
    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    return raw


MUL = tuple(tuple(_mul(a, b) for b in range(32)) for a in range(32))


def fpow(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = MUL[answer][value]
        value = MUL[value][value]
        exponent >>= 1
    return answer


def trace(value: int) -> int:
    answer, current = 0, value
    for _ in range(5):
        answer ^= current
        current = MUL[current][current]
    return answer


def layer(value: int) -> int:
    return int(value == 0 or trace(value) == 1)


def stats_from_mask(mask: int) -> tuple:
    e = [1] + [0] * 8
    for p in range(32):
        if mask >> p & 1:
            for d in range(8, 0, -1):
                e[d] ^= MUL[p][e[d - 1]]
    return tuple(e[1:9])


POPCOUNT = tuple(bin(m).count("1") for m in range(1 << 16))


def half_tables(elems):
    n = len(elems)
    stats = [None] * (1 << n)
    full_of = [0] * (1 << n)
    stats[0] = (0,) * 8
    for m in range(1, 1 << n):
        lb = m & -m
        i = lb.bit_length() - 1
        x = elems[i]
        p = stats[m ^ lb]
        stats[m] = tuple(
            p[d - 1] ^ MUL[x][1 if d == 1 else p[d - 2]] for d in range(1, 9)
        )
        full_of[m] = full_of[m ^ lb] | (1 << x)
    return stats, full_of


def enumerate_r_sets(elems_a, elems_b):
    sa, fa = half_tables(elems_a)
    sb, fb = half_tables(elems_b)
    buckets = {}
    for m in range(1 << 16):
        st = sb[m]
        key = (POPCOUNT[m], st[0], st[1], st[2])
        buckets.setdefault(key, []).append((m, st))
    records = [[] for _ in range(32)]
    for m in range(1, 1 << 16):
        sza = POPCOUNT[m]
        szb = 17 - sza
        if not 1 <= szb <= 16:
            continue
        a1, a2, a3, a4, a5, a6, a7, a8 = sa[m]
        b1 = a1
        b2 = a2 ^ MUL[a1][a1]
        b3 = a3 ^ MUL[a2][b1] ^ MUL[a1][b2]
        for mb, st in buckets.get((szb, b1, b2, b3), ()):
            b4, b5, b6, b7, b8 = st[3], st[4], st[5], st[6], st[7]
            e4 = a4 ^ MUL[a3][b1] ^ MUL[a2][b2] ^ MUL[a1][b3] ^ b4
            e5 = (a5 ^ MUL[a4][b1] ^ MUL[a3][b2] ^ MUL[a2][b3]
                  ^ MUL[a1][b4] ^ b5)
            e6 = (a6 ^ MUL[a5][b1] ^ MUL[a4][b2] ^ MUL[a3][b3]
                  ^ MUL[a2][b4] ^ MUL[a1][b5] ^ b6)
            e7 = (a7 ^ MUL[a6][b1] ^ MUL[a5][b2] ^ MUL[a4][b3]
                  ^ MUL[a3][b4] ^ MUL[a2][b5] ^ MUL[a1][b6] ^ b7)
            e8 = (a8 ^ MUL[a7][b1] ^ MUL[a6][b2] ^ MUL[a5][b3]
                  ^ MUL[a4][b4] ^ MUL[a3][b5] ^ MUL[a2][b6]
                  ^ MUL[a1][b7] ^ b8)
            records[e4].append((fa[m] | fb[mb], e5, e6, e7, e8))
    return records


def lambda_of(r, tail, a):
    e5, e6, e7, e8 = tail
    t = MUL[r][a] ^ e5
    t = MUL[t][a] ^ e6
    t = MUL[t][a] ^ e7
    return MUL[t][a] ^ e8


def build_graph(records_r, r):
    vid, verts = {}, []
    cliques = []
    for mask, e5, e6, e7, e8 in records_r:
        members = []
        for a in range(32):
            if mask >> a & 1:
                key = (a, lambda_of(r, (e5, e6, e7, e8), a))
                if key not in vid:
                    vid[key] = len(verts)
                    verts.append(key)
                members.append(vid[key])
        cliques.append(tuple(members))
    n = len(verts)
    neigh = [0] * n
    for mem in cliques:
        for i, j in combinations(mem, 2):
            neigh[i] |= 1 << j
            neigh[j] |= 1 << i
    return verts, neigh, cliques, vid


def edge_count(neigh):
    return sum(bin(m).count("1") for m in neigh) // 2


def class_span_core(verts, neigh, need):
    n = len(verts)
    alive = (1 << n) - 1
    changed = True
    while changed:
        changed = False
        m = alive
        while m:
            lb = m & -m
            v = lb.bit_length() - 1
            m ^= lb
            nb = neigh[v] & alive
            classes = set()
            while nb:
                l2 = nb & -nb
                classes.add(verts[l2.bit_length() - 1][0])
                nb ^= l2
            if len(classes) < need:
                alive ^= lb
                changed = True
    return alive


def max_clique(neigh, initial_best=0):
    n = len(neigh)
    best = initial_best
    best_set = 0
    if n == 0:
        return best, best_set

    def expand(cand, cur, size):
        nonlocal best, best_set
        order, bound = [], []
        un = cand
        colour = 0
        while un:
            colour += 1
            avail = un
            while avail:
                lb = avail & -avail
                v = lb.bit_length() - 1
                order.append(v)
                bound.append(colour)
                un ^= lb
                avail &= ~(neigh[v] | lb)
        for idx in range(len(order) - 1, -1, -1):
            if size + bound[idx] <= best:
                return
            v = order[idx]
            newcand = cand & neigh[v]
            if newcand:
                expand(newcand, cur | (1 << v), size + 1)
            elif size + 1 > best:
                best = size + 1
                best_set = cur | (1 << v)
            cand &= ~(1 << v)

    expand((1 << n) - 1, 0, 0)
    return best, best_set


def induced(neigh, keep_ids):
    pos = {v: i for i, v in enumerate(keep_ids)}
    sub = [0] * len(keep_ids)
    for i, v in enumerate(keep_ids):
        nb = neigh[v]
        while nb:
            lb = nb & -nb
            u = lb.bit_length() - 1
            nb ^= lb
            if u in pos:
                sub[i] |= 1 << pos[u]
    return sub


def dsatur(neigh):
    n = len(neigh)
    colours = [-1] * n
    sat = [set() for _ in range(n)]
    degs = [bin(neigh[v]).count("1") for v in range(n)]
    for _ in range(n):
        v = max(
            (u for u in range(n) if colours[u] < 0),
            key=lambda u: (len(sat[u]), degs[u]),
        )
        c = 0
        while c in sat[v]:
            c += 1
        colours[v] = c
        nb = neigh[v]
        while nb:
            lb = nb & -nb
            sat[lb.bit_length() - 1].add(c)
            nb ^= lb
    return colours


def greedy_random(neigh, rng):
    n = len(neigh)
    order = list(range(n))
    rng.shuffle(order)
    colours = [-1] * n
    for v in order:
        used = set()
        nb = neigh[v]
        while nb:
            lb = nb & -nb
            c = colours[lb.bit_length() - 1]
            if c >= 0:
                used.add(c)
            nb ^= lb
        c = 0
        while c in used:
            c += 1
        colours[v] = c
    return colours


def edge_pair_set(verts, neigh):
    pairs = set()
    for i in range(len(verts)):
        nb = neigh[i]
        while nb:
            lb = nb & -nb
            j = lb.bit_length() - 1
            nb ^= lb
            if j > i:
                pairs.add(frozenset((verts[i], verts[j])))
    return pairs


def covering_mask(records_r, r, a, la, b, lb_):
    for mask, e5, e6, e7, e8 in records_r:
        if mask >> a & 1 and mask >> b & 1:
            tail = (e5, e6, e7, e8)
            if lambda_of(r, tail, a) == la and lambda_of(r, tail, b) == lb_:
                return mask
    return None


def main():
    t0 = time.time()

    def say(*args):
        print(f"[{time.time()-t0:7.1f}s]", *args, flush=True)

    # Stage 1: enumeration + alternate-split completeness check.
    records = enumerate_r_sets(list(range(16)), list(range(16, 32)))
    counts = [len(records[r]) for r in range(32)]
    say("R-set counts per r:", counts, "total:", sum(counts))
    records_alt = enumerate_r_sets(list(range(0, 32, 2)),
                                   list(range(1, 32, 2)))
    for r in range(32):
        assert sorted(records[r]) == sorted(records_alt[r]), r
    say("alternate-split enumeration IDENTICAL")
    assert len({counts[r] for r in range(1, 32)}) == 1

    # Stage 2: from-scratch verification of every record.
    for r in range(32):
        for mask, e5, e6, e7, e8 in records[r]:
            assert bin(mask).count("1") == 17
            st = stats_from_mask(mask)
            assert st[0] == st[1] == st[2] == 0
            assert st[3] == r and st[4:] == (e5, e6, e7, e8)
    say("every record re-verified from scratch")

    # Stage 3: K32 witness masks cross-check.
    mask_sets = [set(m for m, *_ in records[r]) for r in range(32)]
    k32_r_used = set()
    n_checked = 0
    for a in range(32):
        row = EDGE_WITNESS_MASK_ROWS[a]
        assert len(row) == 31 - a
        for off, mask in enumerate(row):
            b = a + off + 1
            st = stats_from_mask(mask)
            assert st[0] == st[1] == st[2] == 0
            r = st[3]
            k32_r_used.add(r)
            assert mask in mask_sets[r]
            tail = st[4:]
            assert lambda_of(r, tail, a) == layer(a)
            assert lambda_of(r, tail, b) == layer(b)
            n_checked += 1
    assert n_checked == 496
    say("all 496 K32 witness masks consistent; r values used:",
        sorted(k32_r_used))

    # Stage 4: build all graphs; verify scaling isomorphism for r != 0.
    graphs = {}
    for r in range(32):
        graphs[r] = build_graph(records[r], r)
    for r in (0, 1):
        verts, neigh, cliques, _ = graphs[r]
        say(f"G_{r}: {len(verts)} vertices, {edge_count(neigh)} edges, "
            f"{len(cliques)} R-cliques")
    verts1, neigh1, _, _ = graphs[1]
    base_pairs = edge_pair_set(verts1, neigh1)
    for r in range(2, 32):
        c = fpow(r, 8)
        assert fpow(c, 4) == r
        c8 = fpow(c, 8)
        vr, nr, _, _ = graphs[r]
        assert {(MUL[c][a], MUL[c8][lam]) for a, lam in verts1} == set(vr)
        mapped = {
            frozenset(((MUL[c][a1], MUL[c8][l1]),
                       (MUL[c][a2], MUL[c8][l2])))
            for (a1, l1), (a2, l2) in base_pairs
        }
        assert mapped == edge_pair_set(vr, nr)
    say("scaling isomorphism G_1 -> G_r verified edge-by-edge, all r != 0")

    # Stage 5: exact clique number of G_0 and G_1.
    for r in (0, 1):
        verts, neigh, cliques, vid = graphs[r]
        core = class_span_core(verts, neigh, 17)
        core_size = bin(core).count("1")
        say(f"G_{r}: 17-class-span core size = {core_size}")
        if core_size == 0:
            omega = 17 if cliques else 0
            say(f"G_{r}: NO K18 (empty core); omega = {omega}")
        else:
            keep = []
            m = core
            while m:
                lb = m & -m
                keep.append(lb.bit_length() - 1)
                m ^= lb
            sub = induced(neigh, keep)
            om, wset = max_clique(sub, initial_best=17)
            if om > 17:
                omega = om
                wit = [verts[keep[i]] for i in range(len(keep))
                       if wset >> i & 1]
                say(f"G_{r}: K{om} FOUND, omega = {om}")
                say("witness states (a,lambda):", sorted(wit))
                say("certificate pair coverings (a b mask_hex):")
                for (a, la), (b, lb_) in combinations(sorted(wit), 2):
                    mk = covering_mask(records[r], r, a, la, b, lb_)
                    assert mk is not None
                    print(f"  {a} {b} {mk:08X}", flush=True)
            else:
                omega = 17
                say(f"G_{r}: core has no K18; omega = 17")

    # Stage 6: does the K32 layer pattern retain a K18 for any r?
    say("layer pattern:", [layer(a) for a in range(32)])
    h_omegas = []
    h_best = (0, None, None)
    for r in range(32):
        verts, neigh, cliques, vid = graphs[r]
        keep = [vid[(a, layer(a))] for a in range(32)
                if (a, layer(a)) in vid]
        sub = induced(neigh, keep)
        om, wset = max_clique(sub)
        h_omegas.append(om)
        if om > h_best[0]:
            wit = [verts[keep[i]] for i in range(len(keep)) if wset >> i & 1]
            h_best = (om, r, sorted(wit))
    say("omega(H_r) for r=0..31:", h_omegas)
    say("max omega(H_r):", h_best[0], "at r =", h_best[1],
        "witness:", h_best[2])

    # Stage 7: colouring upper bounds for G_0, G_1.
    rng = random.Random(835)
    for r in (0, 1):
        verts, neigh, cliques, _ = graphs[r]
        cols = dsatur(neigh)
        best_cols = cols
        best = max(cols) + 1
        say(f"G_{r}: DSATUR colours = {best}")
        for _ in range(200):
            cols = greedy_random(neigh, rng)
            used = max(cols) + 1
            if used < best:
                best = used
                best_cols = cols
        say(f"G_{r}: best of DSATUR + 200 random greedy = {best}")
        if best <= 17:
            say(f"G_{r}: 17-COLOURING FOUND; vertex:colour table follows")
            print(";".join(f"{a},{lam}:{c}" for (a, lam), c
                           in zip(verts, best_cols)), flush=True)

    say("ALL-STAGES-COMPLETE")


if __name__ == "__main__":
    main()
