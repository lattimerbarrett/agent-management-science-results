import sympy as sp
# Check the algebraic partial-sum identity used to apply exhaustion.
# Positivity/order of these expressions is supplied by the hypotheses,
# and is not inferred from this symbolic check.
N = sp.symbols('N', integer=True, positive=True)
n = sp.symbols('n', integer=True)
a = sp.Function('a')
s = sp.summation(a(n+1)-a(n), (n, 0, N-1))
print('Partial-sum identity:', s)
for k in range(1, 21):
    entries = sp.symbols('a0:'+str(k+1), commutative=False)
    assert sp.expand(sum(entries[j+1]-entries[j] for j in range(k))-(entries[k]-entries[0])) == 0
print('Noncommutative telescoping checked for lengths 1 through 20.')
print('Exhaustion hypotheses: b_n >= 0; partial sums = a_N-a_0 <= 1; tau finite since tau(1)=1; tau is a 2-quasitrace.')