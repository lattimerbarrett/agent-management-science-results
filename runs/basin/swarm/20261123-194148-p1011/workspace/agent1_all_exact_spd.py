from pathlib import Path
import sympy as s
source=Path('workspace/agent1_exactmoments.py').read_text()
exec(source.split('for n in [17,18,19]:')[0])
K=s.symbols('K')

def universal_C(n,ell,d):
 start=max(0,2-ell);base=max(1,ell);a=s.Rational(n+2*ell-3,2)
 ratios={base:s.Integer(1)}
 if ell==0:ratios[0]=s.Integer(0)
 for p in range(base,ell+d):
  ratios[p+1]=s.expand(ratios[p]*(K+(p-ell)*(n-2-p+ell))/(2*p*(a-p)))
 gs=[]
 for q in range(start,d+1):
  c=s.Rational(q*(2*q+n+2*ell-3),n-1);g=0
  for e,coef in [(q-1,c),(q,c+1-ell-2*q)]:
   if e<0:continue
   for p in range(e+1):g+=coef*s.binomial(e,p)*2**p*(-1)**(e-p)*ratios[ell+p]
  gs.append(s.factor(g))
 if ell>=2:R=s.prod(K-r*(r+n-2) for r in range(2,ell))
 elif ell==1:R=1/(K-(n-1))
 else:R=K/(K-(n-1))
 polys=[[s.Poly(s.cancel(R*f*g).subs(K,X+2*n),X) for f in gs] for g in gs]
 M=moments(n,max(p.degree() for row in polys for p in row))
 return s.Matrix(len(gs),len(gs),lambda i,j:s.factor(sum(polys[i][j].nth(k)*M[k] for k in range(polys[i][j].degree()+1))))
pilo=s.Rational('3.14159265358979323846264338327950288419716939937510')
pihi=s.Rational('3.14159265358979323846264338327950288419716939937511')
def atan_bounds(q,N=40):
 lo=sum((-1)**k*s.Rational(1,(2*k+1)*q**(2*k+1)) for k in range(N))
 return lo,lo+s.Rational(1,(2*N+1)*q**(2*N+1))
a5,b5=atan_bounds(5);a239,b239=atan_bounds(239)
assert pilo<16*a5-4*b239 and 16*b5-4*a239<pihi

def w_interval(n):
 exact=s.simplify(8*s.Rational(n+4,(n+1)**2)/s.pi*s.gamma(s.Rational(n+3,2))**2/(s.gamma(s.Rational(n+2,2))*s.gamma(s.Rational(n+4,2))))
 endpoints=[exact.subs(s.pi,p) for p in [pilo,pihi]]
 return min(endpoints),max(endpoints)
def positive(expr,lo,hi):
 P=s.Poly(expr,w);lower=0
 for (k,),c in P.terms():lower+=c*(lo if c>0 else hi)**k
 assert lower>0
 return float(lower)

if __name__=='__main__':
 count=0
 for n in range(5,19):
  for ell in range((n-1)//2+1):
   start=max(0,2-ell);d=(n-2*ell-1)//4
   if d<start:continue
   C=universal_C(n,ell,d);inds=list(range(start,d+1));sz=len(inds)
   D=s.Matrix(sz,sz,lambda i,j:(ell-1+inds[i]+inds[j])*C[i,j])
   lo,hi=w_interval(n)
   bounds=[positive(s.factor(D[:k,:k].det()),lo,hi) for k in range(1,sz+1)]
   count+=1
   print(n,ell,d,'exact SPD',bounds)
 print('CERTIFIED',count,'blocks, including singleton blocks')
