import sympy as s
C, delta, eta, d=s.symbols('C delta eta d', positive=True)
coefficient=eta/d
assert s.simplify(coefficient*d)==eta
print('Normalized increment: b_n=(eta/tau(p_n))*p_n, so tau(b_n)=eta.')
print('If eta<=delta/C and tau(p_n)>=delta, then coefficient<=1/C.')
print('Hence sum_(n<N)b_n <= C^(-1)sum_(n<N)p_n <=1.')
print('Trace obstruction: N*delta <= sum tau(p_n) = tau(sum p_n) <= C.')
for c,dl in [(2,s.Rational(1,4)),(3,s.Rational(1,3)),(10,s.Rational(2,5))]:
    N=s.floor(c/dl)+1
    assert N*dl>c
    print(f'C={c}, delta={dl}: N={N} gives N*delta={N*dl}>C.')
print('Without additivity the equality in the trace obstruction is unavailable.')
print('The bounds do not decide existence of a least upper bound in M_sa.')
