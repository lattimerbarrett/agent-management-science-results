from itertools import product

# Exhaust every enumeration operator on the two-point universe.
n = 2
subsets = range(1 << n)
pairs = [(x, F) for x in range(n) for F in subsets]
operators = [tuple(p for i, p in enumerate(pairs) if mask >> i & 1)
             for mask in range(1 << len(pairs))]

def apply(op, B):
    out = 0
    for x, F in op:
        if F & ~B == 0:
            out |= 1 << x
    return out

def compose(P, Q):
    rules = set()
    for x, F in P:
        choices = [[G for y, G in Q if y == z]
                   for z in range(n) if F >> z & 1]
        for gs in product(*choices):
            U = 0
            for G in gs:
                U |= G
            rules.add((x, U))
    return tuple(rules)

composition_cases = 0
for P in operators:
    for Q in operators:
        C = compose(P, Q)
        for B in subsets:
            assert apply(C, B) == apply(P, apply(Q, B))
            composition_cases += 1
print('Composition equalities checked:', composition_cases)

# The total-degree -> cototal-degree proof uses the representative
# X join complement(X), whose complement is obtained by swapping columns.
join_cases = 0
for size in range(1, 11):
    full = (1 << size) - 1
    full_join = (1 << (2 * size)) - 1
    for X in range(1 << size):
        D = 0
        for i in range(size):
            D |= 1 << (2 * i + (0 if X >> i & 1 else 1))
        swapped = 0
        for j in range(2 * size):
            if D >> j & 1:
                swapped |= 1 << (j ^ 1)
        assert swapped == (full_join ^ D)
        join_cases += 1
print('Complement/column-swap equalities checked:', join_cases)
