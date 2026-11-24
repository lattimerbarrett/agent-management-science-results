import sympy as s
# Audit a direct projection-lattice construction: taking meets of all
# lower spectral cuts gives the spectral supremum, not necessarily the
# ordinary-order supremum.  Test even a comparable two-term chain.
a=s.diag(s.Rational(1,3),0)
b=s.Matrix([[2,1],[1,1]])/3
lm=(3-s.sqrt(5))/6
lp=(3+s.sqrt(5))/6
I=s.eye(2)
qminus=s.simplify((lp*I-b)/(lp-lm))
qplus=I-qminus
spectral_envelope=s.simplify(s.Rational(1,3)*qminus+lp*qplus)
difference=s.simplify(spectral_envelope-b)
print('b-a positive: trace =', s.trace(b-a), ', det =', (b-a).det())
print('spectral meet construction exceeds the actual least upper bound b:')
print('trace(envelope-b) =', s.simplify(s.trace(difference)))
print('det(envelope-b) =', s.simplify(difference.det()))
assert s.simplify(s.trace(difference)-(s.sqrt(5)-1)/6)==0
assert s.simplify(difference.det())==0
print('Conclusion: projection completeness alone supplies the wrong supremum;')
print('the supplied constant-gap regularity result must be used specifically.')
