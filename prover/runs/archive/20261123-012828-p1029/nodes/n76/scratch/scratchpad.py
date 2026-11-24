import sympy as sp
# This is an identity of elements, not an application of a quasitrace
# to a noncommuting sum.
a = sp.symbols('a0:9', commutative=False)
for N in range(1,9):
    partial_sum = sp.Add(*(a[k+1]-a[k] for k in range(N)))
    assert sp.expand(partial_sum-(a[N]-a[0])) == 0
print('Element-level telescoping verified for N=1,...,8: sum b_k = a_N-a_0.')
print('Order hypotheses imply 0 <= sum b_k <= 1, uniformly in N.')
print('The supplied positive-series exhaustion theorem therefore gives tau(b_n) -> 0.')
print('A constant value eta > 0 contradicts this conclusion.')
