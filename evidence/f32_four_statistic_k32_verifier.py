#!/usr/bin/env python3
"""Verify an actual-edge K32 in a four-statistic F_32 quotient.

For a 16-set S put

    sigma(S) = (e_1(S), e_2(S), e_3(S), e_8(S) + e_1(S)^8).

For every unordered pair of the 32 claimed quotient states, the static
certificate below gives a 17-set R.  Deleting the two field elements that
index the pair gives the two required states.  This checker contains no
search code: it recomputes the field arithmetic, elementary coefficients,
and all 496 actual Johnson edges directly from the masks.
"""

from itertools import combinations


MODULUS = 0b100101  # X^5 + X^2 + 1

# Row a contains the masks for pairs (a,b), b=a+1,...,31, in that order.
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


def multiply(left: int, right: int) -> int:
    """Polynomial multiplication followed by direct long division."""

    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    assert 0 <= raw < 32
    return raw


def power(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = multiply(answer, value)
        value = multiply(value, value)
        exponent >>= 1
    return answer


def trace(value: int) -> int:
    answer = 0
    current = value
    for _ in range(5):
        answer ^= current
        current = multiply(current, current)
    assert answer in (0, 1)
    return answer


def layer(value: int) -> int:
    return int(value == 0 or trace(value) == 1)


def claimed_state(value: int) -> tuple[int, int, int, int]:
    return value, power(value, 2), power(value, 3), layer(value)


def statistic(points: frozenset[int]) -> tuple[int, int, int, int]:
    """Compute (e_1,e_2,e_3,e_8+e_1^8) from the definition."""

    assert len(points) == 16
    coefficients = [1] + [0] * 8
    for point in sorted(points):
        for degree in range(8, 0, -1):
            coefficients[degree] ^= multiply(
                point, coefficients[degree - 1]
            )
    first = coefficients[1]
    return (
        first,
        coefficients[2],
        coefficients[3],
        coefficients[8] ^ power(first, 8),
    )


def points_from_mask(mask: int) -> frozenset[int]:
    assert 0 <= mask < 1 << 32
    points = frozenset(point for point in range(32) if mask >> point & 1)
    assert len(points) == 17
    return points


def main() -> None:
    for value in range(1, 32):
        assert multiply(value, power(value, 30)) == 1

    states = tuple(claimed_state(value) for value in range(32))
    assert len(set(states)) == 32
    assert len(EDGE_WITNESS_MASK_ROWS) == 32
    assert sum(map(len, EDGE_WITNESS_MASK_ROWS)) == 32 * 31 // 2

    verified_edges = set()
    for left, right in combinations(range(32), 2):
        row = EDGE_WITNESS_MASK_ROWS[left]
        assert len(row) == 31 - left
        roots = points_from_mask(row[right - left - 1])
        assert left in roots
        assert right in roots
        left_half = roots - {left}
        right_half = roots - {right}
        assert statistic(left_half) == states[left]
        assert statistic(right_half) == states[right]
        assert len(left_half & right_half) == 15
        verified_edges.add(frozenset((states[left], states[right])))

    assert len(verified_edges) == 32 * 31 // 2
    for left, right in combinations(states, 2):
        assert frozenset((left, right)) in verified_edges

    print("F_32 four-statistic actual-edge K32 certificate: PASS")
    print("quotient vertices:", len(states))
    print("Johnson edges checked:", len(verified_edges))
    print("layer-one parameters:", tuple(a for a in range(32) if layer(a)))
    print(
        "consequence: every colouring depending only on "
        "(e1,e2,e3,e8+e1^8) needs at least 32 colours"
    )


if __name__ == "__main__":
    main()
