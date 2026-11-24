import sympy as s
x=s.symbols('x')
for c in range(3,21):
 odd=[p for p in s.factorint(c) if p!=2]
 if odd:
  p=int(odd[0]); q=c//p
  f=s.Poly(s.expand(sum((1+x**q)**j for j in range(p))),x)
 else:
  p=2
  f=s.Poly(x**(c//2)-2*x**(c//4)+2,x)
 coeff=f.all_coeffs()
 eis=coeff[0]==1 and all(int(a)%p==0 for a in coeff[1:]) and int(coeff[-1])%(p*p)!=0
 e=f.degree(); threshold=s.Rational(p*e,p-1)
 assert eis and threshold==c
 print(f'c={c}: p={p}, e={e}, Hilbert threshold={threshold}, Eisenstein={eis}')
