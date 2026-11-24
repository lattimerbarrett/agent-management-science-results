# Quantum ring basis M,A,B,P; q shifts action by -Omega.
# Products: A^2=B^2=q M, AB=P, AP=q B, BP=q A, P^2=q^2 M.
from fractions import Fraction
Omega=1
c={'M':Fraction(0),'A':Fraction(-1,2),'B':Fraction(-1,2),'P':Fraction(-1)}
checks=[('A*A',c['M']-1,c['A']),('B*B',c['M']-1,c['B']),('A*B',c['P'],c['A']),('B*A',c['P'],c['B']),('A*P',c['B']-1,c['P']),('B*P',c['A']-1,c['P'])]
for name,left,right in checks:
 print(name,':',left,'<',right,':',left<right)
print('These elementary strict inequalities alone permit two action cosets modulo Omega.')
print('Therefore three capped spectral carriers must not simply be counted as three geometric fixed points. The verified applicable degenerate cup-length theorem is the required stronger input for the lower bound of three.')
