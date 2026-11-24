# Audit the induction by exhaustive finite nested-set models.
# A_1 = G_1, G_i subset A_i, and both chains descend.
from itertools import product
U = frozenset(range(3))
sets = [frozenset(x for x in U if mask & (1 << x)) for mask in range(8)]
counterexamples = 0
models = 0
for A2, A3, G2, G3 in product(sets, repeat=4):
    A = [U, A2, A3]
    G = [U, G2, G3]
    if not (A3 <= A2 and G3 <= G2 and G2 <= A2 and G3 <= A3):
        continue
    if all(G[c+1] == (G[c] & A[c+1]) for c in range(2)):
        models += 1
        if G != A:
            counterexamples += 1
print('Models with no strict inclusions:', models)
print('Models in which the filtrations differ:', counterexamples)
print('Substitution: if G_c=A_c and A_(c+1) is contained in A_c,')
print('then G_c intersect A_(c+1) = A_(c+1).')