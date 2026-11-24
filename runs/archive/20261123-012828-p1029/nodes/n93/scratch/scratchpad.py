import sympy as s
eta=s.symbols('eta', positive=True)
# For B_n=diag(a_n,0), the normalized matrix quasitrace is half
# the sum of the quasitraces of the diagonal entries.
print('ambient increment:', eta/2)
print('e11-corner weight:', s.Rational(1,2))
print('normalized e11-corner increment:', s.simplify((eta/2)/s.Rational(1,2)))
print('normalized e22-corner increment:', 0)
D=s.diag(s.Rational(4,5),s.Rational(1,5))
print('Illustration with ordinary normalized trace:')
print('tau(D)=',s.trace(D)/2)
print('first normalized spectral-corner value=',D[0,0])
print('second normalized spectral-corner value=',D[1,1])
print('A corner can increase, decrease, or annihilate an increment.')
