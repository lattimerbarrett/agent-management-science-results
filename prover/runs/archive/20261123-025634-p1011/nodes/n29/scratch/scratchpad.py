from pathlib import Path
s=Path('experiments/e1/agent2_robust_diagonal_complete.md').read_text()
a=s.index('## 4.');b=s.index('## 5.')
print(s[a:b])
print('\nScaling checks for sequential insertion f_e=e^9 F(x/e), deg F<=8:')
import sympy as S
e=S.symbols('epsilon', positive=True)
for n in [19,20,25,40]:
 print('n=',n, 'background/shape^2 = epsilon^',n-18,'; residual/shape = epsilon^',S.Rational(n-2,2)-8)
print('For rho=1/log(1/epsilon), ||D^m f_e|| is bounded by a sum of epsilon^(9-d)*log(1/epsilon)^(m-d), 2<=d<=8.')
print('Every exponent 9-d is positive; hence every fixed C^m norm tends to zero.')
print('Tail budget: sum_{l=0}^infty (r/2)*4^(-l) =',S.summation(S.Rational(1,2)*S.Rational(1,4)**S.Symbol('l',integer=True,nonnegative=True),(S.Symbol('l',integer=True,nonnegative=True),0,S.oo)))
