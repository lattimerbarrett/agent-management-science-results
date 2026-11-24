from z3 import *
# For a hypothetical element x, encode membership in two descending
# filtrations G_i <= A_i, with the same first term.
# Absence of the strict inclusion means G_i intersect A_{i+1}=G_{i+1}.
for depth in (2, 3, 8, 30):
    g = [Bool(f'g_{depth}_{i}') for i in range(depth)]
    a = [Bool(f'a_{depth}_{i}') for i in range(depth)]
    s = Solver()
    s.add(g[0] == a[0])
    for i in range(depth):
        s.add(Implies(g[i], a[i]))
    for i in range(depth-1):
        s.add(Implies(a[i+1], a[i]), Implies(g[i+1], g[i]))
        s.add(g[i+1] == And(g[i], a[i+1]))
    s.add(Or([And(a[i], Not(g[i])) for i in range(depth)]))
    print(f'depth {depth}: finite-degree discrepancy with no strict intersection = {s.check()}')
