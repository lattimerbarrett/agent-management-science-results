"""Exact rational verification of root-coordinate connection, s=3,m=6."""
import sympy as S
from itertools import product

def check():
 z=S.symbols('z');be=-S.Rational(120,343)
 q=z**3-z-be/3;p=z**3-z-2*be/3;B2=2*be**2/9
 la=[-S.Rational(8,7),-S.Integer(1),S.Integer(0),S.Rational(3,7),S.Rational(5,7),S.Integer(1)]
 P=S.prod(z-t for t in la)
 assert S.expand(q*p-B2-P)==0
 xi=[-S.Rational(1,2),S.Rational(4,7)]
 h=S.prod(z-t for t in xi);pd=[S.diff(P,z).subs(z,t) for t in la]
 w=[S.cancel(p.subs(z,t)*h.subs(z,t)/pd[i]) for i,t in enumerate(la)]
 wp=[S.cancel(q.subs(z,t)*h.subs(z,t)/pd[i]) for i,t in enumerate(la)]
 assert sum(w)==sum(wp)==1 and all(v>0 for v in w+wp)
 # Affine coordinates theta=(coefficient of z, constant coefficient) of h.
 feats=[S.Matrix([t,1]) for t in la]
 metrics=[];cubics=[]
 for poly in [p,q]:
  metric=S.zeros(2); cubic=[[[S.Integer(0) for c in range(2)] for b in range(2)] for a in range(2)]
  for i,t in enumerate(la):
   val=S.cancel(poly.subs(z,t)/(pd[i]*h.subs(z,t)))
   metric+=val*(feats[i]*feats[i].T)
   for a,b,c in product(range(2),repeat=3):
    cubic[a][b][c]-=val/h.subs(z,t)*feats[i][a]*feats[i][b]*feats[i][c]
  metrics.append(metric);cubics.append(cubic)
 invs=[g.inv() for g in metrics]
 Gam=[[[S.cancel(sum(invs[t][a,k]*cubics[t][k][b][c] for t in range(2) for k in range(2))/2) for c in range(2)] for b in range(2)] for a in range(2)]
 J=S.Matrix([[-1,-1],[xi[1],xi[0]]]);Ji=J.inv()
 got={}
 for a,b,c in product(range(2),repeat=3):
  transformed=sum(Ji[a,k]*sum(Gam[k][u][v]*J[u,b]*J[v,c] for u,v in product(range(2),repeat=2)) for k in range(2))
  transformed+=Ji[a,1]*(1 if b!=c else 0)
  got[a,b,c]=S.cancel(transformed)
 g1=[S.cancel(-p.subs(z,t)*S.diff(h,z).subs(z,t)/P.subs(z,t)) for t in xi]
 g2=[S.cancel(-q.subs(z,t)*S.diff(h,z).subs(z,t)/P.subs(z,t)) for t in xi]
 assert J.T*metrics[0]*J==S.diag(*g1)
 assert J.T*metrics[1]*J==S.diag(*g2)
 for a,b,c in product(range(2),repeat=3):
  if b!=c: expected=0
  elif a!=b: expected=-(g1[b]/g1[a]+g2[b]/g2[a])/(2*(xi[a]-xi[b]))
  else:
   expected=sum(1/(xi[a]-xi[j]) for j in range(2) if j!=a)
   expected-=S.diff(P,z).subs(z,xi[a])/P.subs(z,xi[a])
   expected+=(S.diff(p,z).subs(z,xi[a])/p.subs(z,xi[a])+S.diff(q,z).subs(z,xi[a])/q.subs(z,xi[a]))/2
  assert S.cancel(got[a,b,c]-expected)==0,(a,b,c,got[a,b,c],expected)
 assert got[0,1,1]>0 and got[1,0,0]<0
 return got

if __name__=='__main__':
 print('Exact root connection checks passed:', check())
