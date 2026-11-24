import sympy as s
z=s.symbols('z'); pi=z-1
d=s.rem(1+pi**2,z*z+z+1,z)
norm=s.resultant(z*z+z+1,d,z)
print('For K=Q_3(zeta_3), pi=zeta_3-1:')
print('d=1+pi^2=',d)
print('Norm_K/Q3(d)=',norm,'; residue mod 9 =',int(norm)%9)
print('Hence cyclotomic reciprocity gives a nontrivial (zeta_3,d)_3.')
print('This verifies the symbol, not the class-three quotient.')
from pathlib import Path
print('\nRank-three propagation proof:\n')
print(Path('experiments/e3/agent3_propagation.md').read_text())