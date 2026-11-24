from itertools import combinations, product
# Finite check of the translation: replace every axiom (e,F)
# in the source operator by (y,F) for EVERY output y.
U = range(3)
finite_sets = [frozenset(c) for k in range(4) for c in combinations(U,k)]
checks = 0
for e in U:
    # All possible rows of axioms with output e.
    for mask in range(1 << len(finite_sets)):
        row = [F for i,F in enumerate(finite_sets) if mask >> i & 1]
        translated_axioms = [(y,F) for F in row for y in U]
        for A in finite_sets:
            source_diagonal = any(F <= A for F in row)
            for j in U:
                target_diagonal = any(y == j and F <= A for y,F in translated_axioms)
                assert source_diagonal == target_diagonal
                assert (not source_diagonal) == (not target_diagonal)
                checks += 1
print(f'{checks} checks: both diagonal membership and its complement are preserved.')