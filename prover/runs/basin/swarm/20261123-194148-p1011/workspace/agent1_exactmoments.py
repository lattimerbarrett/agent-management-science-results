import sympy as s
j,N,X=s.symbols('j N X'); w=s.symbols('w')

def xpoly(poly,n):
 poly=s.Poly(s.cancel(poly),j); result=0
 while not poly.is_zero:
  d=poly.degree()
  assert d%2==0, (d,poly)
  c=poly.LC(); term=c*(j*(j+n+2))**(d//2)
  result+=c*X**(d//2);poly=s.Poly(s.expand(poly.as_expr()-term),j)
 return s.expand(result)

def moments(n,maxr):
 total=[]
 for start,ws in [(0,s.Integer(1)),(1,w)]:
  M=[]
  for r in range(maxr+1):
   R=((j+2)*(j+n+2))**r
   A=s.cancel(((j+3)**2*R-(j+n-1)**2*R.subs(j,j-2))/(2*j+n+2))
   a=s.Poly(xpoly(A,n),X)
   rhs=-ws*s.Rational((start+n-1)**2,2*start+n+2)*(start*(start+n))**r
   value=(rhs-sum(a.nth(i)*M[i] for i in range(r)))/a.nth(r)
   M.append(s.factor(value))
  total.append(M)
 return [s.factor(a+b) for a,b in zip(*total)]

def Cexact(n,d=3):
 Ms=moments(n,2*d)
 ratios=[s.Integer(1)]
 for p in range(2,2+d):
  ratios.append(s.expand(ratios[-1]*(X+p*(n+2-p))/(2*p*s.Rational(n+1-2*p,2))))
 gs=[]
 for q in range(d+1):
  c=s.Rational(q*(2*q+n+1),n-1);g=0
  for e,coef in [(q-1,c),(q,c-1-2*q)]:
   if e<0:continue
   for p in range(e+1):g+=coef*s.binomial(e,p)*2**p*(-1)**(e-p)*ratios[p]
  gs.append(s.expand(g))
 def integrate(p):
  p=s.Poly(p,X);return s.factor(sum(p.nth(k)*Ms[k] for k in range(p.degree()+1)))
 C=s.Matrix(d+1,d+1,lambda a,b:integrate(gs[a]*gs[b]));return C

for n in [17,18,19]:
 C=Cexact(n)
 wexact=s.simplify(8*s.Rational(n+4,(n+1)**2)/s.pi*s.gamma(s.Rational(n+3,2))**2/(s.gamma(s.Rational(n+2,2))*s.gamma(s.Rational(n+4,2))))
 CC=C.subs(w,wexact)
 D=s.Matrix(4,4,lambda a,b:(a+b+1)*CC[a,b])
 print('n',n,'w1',wexact)
 print('C/C00',s.N(CC/CC[0,0],7))
 print('principal minor signs:',[s.sign(s.N(D[:k,:k].det(),30)) for k in range(1,5)])
 print('det D =',s.factor(D.det()))
from pathlib import Path
