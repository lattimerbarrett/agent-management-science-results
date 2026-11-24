from itertools import combinations, product

# An enumeration operator on a finite universe is represented by a set
# of pairs (output, bit-mask of a finite oracle witness).
def apply_operator(axioms, oracle):
    return frozenset(x for x, witness in axioms if witness <= oracle)

def compose(outer, inner):
    by_output = {}
    for y, witness in inner:
        by_output.setdefault(y, []).append(witness)
    result = set()
    for x, needed in outer:
        lists = [by_output.get(y, []) for y in sorted(needed)]
        for witnesses in product(*lists):
            result.add((x, frozenset().union(*witnesses)))
    return result

def powerset(n):
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]

# All distinct operators on a two-element universe, in their canonical
# representation by inclusion-minimal witnesses.
def all_operators(n):
    subsets = powerset(n)
    antichains = []
    for mask in range(1 << len(subsets)):
        family = [subsets[i] for i in range(len(subsets)) if mask & (1 << i)]
        if all(not (a < b or b < a) for a, b in combinations(family, 2)):
            antichains.append(family)
    return [frozenset((x, f) for x in range(n) for f in families[x])
            for families in product(antichains, repeat=n)]

def main():
    subsets = powerset(2)
    ops = all_operators(2)
    assert len(ops) == 36
    composition_checks = 0
    monotonicity_checks = 0
    for op in ops:
        for a, b in product(subsets, repeat=2):
            if a <= b:
                assert apply_operator(op, a) <= apply_operator(op, b)
                monotonicity_checks += 1
    for outer, inner in product(ops, repeat=2):
        composed = compose(outer, inner)
        for oracle in subsets:
            assert apply_operator(composed, oracle) == apply_operator(
                outer, apply_operator(inner, oracle))
            composition_checks += 1
    # Check the hierarchy-closure calculation CONDITIONAL on a Pi_2 witness.
    # Edges encode sigma_m subset sigma_(m+1) and sigma_m subset dual_(m+1).
    max_m = 12
    reached = {('Pi', 2)}
    while True:
        new = set(reached)
        for label, m in reached:
            if m < max_m:
                new.add((label, m+1))
                new.add(('Sigma' if label == 'Pi' else 'Pi', m+1))
        if new == reached:
            break
        reached = new
    expected = {('Pi', m) for m in range(2, max_m+1)} | {
        ('Sigma', m) for m in range(3, max_m+1)}
    assert reached == expected
    print({'distinct_operators': len(ops),
           'monotonicity_checks': monotonicity_checks,
           'composition_checks': composition_checks,
           'conditional_hierarchy_closure_checked_through': max_m})

if __name__ == '__main__':
    main()
