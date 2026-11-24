import sympy as s
# Only the algebraic reduction is checked here; quasitracial exhaustion is
# the established analytic input, not an assertion of linearity of tau.
a = s.symbols('a0:8', commutative=False)
for N in range(1,8):
    assert s.expand(sum((a[n+1]-a[n] for n in range(N)), s.S.Zero) - (a[N]-a[0])) == 0
print('Checked: sum_{n<N} (a_{n+1}-a_n) = a_N-a_0.')
print('Thus b_n=a_{n+1}-a_n have positive partial sums bounded by 1.')
print('Established 2-quasitracial exhaustion gives tau(b_n) -> 0.')
print('Constant tau(b_n)=eta therefore forces eta=0; no positive eta is possible.')
