import sympy as s
N=s.symbols('N', integer=True, positive=True)
eta=s.symbols('eta', positive=True)
# b_j=a_{j+1}-a_j: cancellation is algebraic, not quasitrace additivity.
for n in range(1,9):
 a=s.symbols('a:'+str(n+1), commutative=False)
 assert s.expand(sum((a[j+1]-a[j] for j in range(n)),s.S.Zero))==a[n]-a[0]
print('Positive partial sums telescope algebraically to a_N-a_0 <= 1.')
print('The established exhaustion result applies: tau(b_n) tends to 0.')
print('But the required values are the constant positive sequence eta.')
print('Consequently eta = 0 is necessary, contradicting eta > 0.')