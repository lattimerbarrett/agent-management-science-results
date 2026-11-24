from pathlib import Path
root=Path('experiments/e4')
print('Available e4 files:')
print('\n'.join(str(p) for p in root.rglob('*') if p.is_file()))
print('\nBasic obstruction: for every eta>0, N=floor(1/eta)+1 gives N*eta>1.')
from fractions import Fraction
for eta in [Fraction(1,2),Fraction(1,3),Fraction(1,10)]:
 N=eta.denominator//eta.numerator+1
 print('eta =',eta,'N =',N,'N*eta =',N*eta)
 assert N*eta>1