from itertools import product
from functools import lru_cache
from fractions import Fraction

# Free associative polynomials, represented by coefficient dictionaries.
def add(a, b, scale=1):
    out = a.copy()
    for word, coeff in b.items():
        out[word] = out.get(word, 0) + scale * coeff
        if out[word] == 0:
            del out[word]
    return out

def mul(a, b):
    out = {}
    for u, x in a.items():
        for v, y in b.items():
            out[u+v] = out.get(u+v, 0) + x*y
    return {w: c for w, c in out.items() if c}

def bracket(a, b):
    return add(mul(a, b), mul(b, a), -1)

def lyndon(w):
    return all(w < w[i:]+w[:i] for i in range(1, len(w)))

@lru_cache(None)
def standard_bracket(w):
    assert lyndon(w)
    if len(w) == 1:
        return {w: 1}
    for i in range(1, len(w)):
        if lyndon(w[i:]):
            return bracket(standard_bracket(w[:i]), standard_bracket(w[i:]))
    raise AssertionError('No Lyndon suffix')

def exact_column_rank(columns):
    pivots = {}
    for col in columns:
        col = {key: Fraction(value) for key, value in col.items() if value}
        while col:
            lead = min(col)
            if lead not in pivots:
                coefficient = col[lead]
                pivots[lead] = {k: v/coefficient for k, v in col.items()}
                break
            coefficient = col[lead]
            col = add(col, pivots[lead], -coefficient)
    return len(pivots)

for degree in range(1, 9):
    words = [w for w in product(range(2), repeat=degree) if lyndon(w)]
    columns = []
    for w in words:
        p = standard_bracket(w)
        column = {}
        for i in range(2):
            for word, coeff in bracket(p, {(i,): 1}).items():
                column[(i, word)] = coeff
        columns.append(column)
    rank = exact_column_rank(columns)
    assert rank == len(words)
    print(f'degree {degree}: dim L = {len(words)}, exact rank of ad = {rank}')
