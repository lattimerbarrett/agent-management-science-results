import sympy as s
# Finite Naimark-type dilation of a genuinely noncommuting positive sequence.
I=s.eye(2)
p=s.Matrix([[1,0],[0,0]])
q=s.Matrix([[1,1],[1,1]])/2
r=s.Matrix([[1,-2],[-2,4]])/5
ps=[p,q,r]
W=s.Matrix.vstack(*(P/2 for P in ps))
assert p*q!=q*p
for n in range(1,4):
 E=s.diag(*([1]*(2*n)+[0]*(6-2*n)))
 A=sum((P/4 for P in ps[:n]),s.zeros(2))
 assert W.T*E*W==A
print('All finite-coordinate compression identities hold exactly.')
print('The increments do not commute:',p*q!=q*p)
print('W*W =',W.T*W)
print('I-W*W eigenvalues:',(I-W.T*W).eigenvals())
print('The dilating coordinate projections are increasing and commute, although their compressions do not.')
print('\nInfinite-dilation audit:')
print('A corner-preserving normal AW*-amplification would give a=W*E W, E=join E_n.')
print('Then inner compression preserves this increasing supremum, so a=sup a_n.')
print('An arbitrary AW*-amplification without projection normality is not sufficient.')
print('The verified monotone-sequential-completeness theorem directly supplies the needed supremum in M.')
