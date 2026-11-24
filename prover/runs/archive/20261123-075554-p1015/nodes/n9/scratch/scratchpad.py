# Check the finite-witness composition used to transfer negative information.
from itertools import combinations
from random import Random
rng = Random(0)
U = set(range(4))
subsets = [frozenset(c) for k in range(5) for c in combinations(U, k)]
def apply(rules, B):
    return {x for x, F in rules if F <= B}
def compose(P, Q):
    out = set()
    import itertools
    for x, F in P:
        choices = [[G for y, G in Q if y == z] for z in F]
        for gs in itertools.product(*choices):
            out.add((x, frozenset().union(*gs)))
    return out
for _ in range(1000):
    P = {(rng.randrange(4), rng.choice(subsets)) for _ in range(12)}
    Q = {(rng.randrange(4), rng.choice(subsets)) for _ in range(12)}
    B = rng.choice(subsets)
    assert apply(compose(P, Q), B) == apply(P, apply(Q, B))
print('Finite-witness composition identity verified in 1000 test cases.')