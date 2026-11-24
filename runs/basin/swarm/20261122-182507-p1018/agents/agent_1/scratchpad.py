# Exact sparse exterior-algebra computation; standard Python only.
def rules_for(n):
    N = n*n + 2*n - 1
    rules = [[] for _ in range(N)]

    def add(k, a, b, c):
        assert a < b
        pair = (1 << a) | (1 << b)
        # The first summand accounts for the odd Leibniz rule;
        # the other two account for putting the new pair in order.
        signmask = ((1 << k)-1) ^ ((1 << a)-1) ^ ((1 << b)-1)
        rules[k].append((pair, signmask, c))

    # Positions: f_i, then t_ab in lexicographic order, then z_i.
    for i in range(n):
        for j in range(n):
            add(i, j, n + j*n + i, 1)
    for i in range(n-1):
        add(n + i*n + i, i, n+n*n+i, 2)
    return N, rules


def differential(state, rules):
    out = {}
    for mask, coefficient in state.items():
        bits = mask
        while bits:
            bit = bits & -bits
            bits ^= bit
            k = bit.bit_length()-1
            rest = mask ^ bit
            for pair, signmask, factor in rules[k]:
                if rest & pair:
                    continue
                value = coefficient * factor
                if (rest & signmask).bit_count() & 1:
                    value = -value
                target = rest | pair
                out[target] = out.get(target, 0) + value
    return {mask: c for mask, c in out.items() if c}


expected_sizes = [
    1, 5, 24, 108, 430, 1550, 4648, 13584, 30939,
    80559, 150404, 338068, 625656, 1107598, 1638740,
    2171000, 2437335, 2481129, 2196440, 1772496,
    1277858, 826542, 479288, 245248, 116208, 48664,
    17740, 5652, 1614, 408, 88, 12, 5, 1
]

N, rules = rules_for(5)
assert N == 34
state = {1 << 4: 1}  # f_5
assert len(state) == expected_sizes[0]
for power in range(1, N):
    state = differential(state, rules)
    assert len(state) == expected_sizes[power], (power, len(state))
    if power == 32:
        assert state == {
            16642998271: 16289280,
            17171480575: -814020480,
            17179738111: -814020480,
            17179867135: -814020480,
            17179869151: -814020480,
        }
    if power >= 31:
        print('delta power', power, ':', sorted(state.items()))
assert state == {(1 << 34)-1: -3239792640}
print('s_34 =', state[(1 << 34)-1], '* D_5')
