from mpmath import iv
from math import comb
from pathlib import Path
iv.dps=30

def certify(n,l,d,N=10000):
 p0=max(1,l);start=max(0,2-l);qs=list(range(max(0,2-l),d+1));size=len(qs)
 if size<2:return True,[]
 a=iv.mpf(n+2*l-3)/2;alpha=a+iv.mpf('.5');T=n+2*l-2;DD=n+2*l-p0-1
 def B(j):return iv.gamma(j+p0)**2*iv.gamma(j+T)*(j+alpha)/(iv.gamma(j+1)*iv.gamma(j+DD)**2)
 def beta(j):
  k=j+l
  return 2*iv.gamma(iv.mpf(k+n+1)/2)*iv.gamma(iv.mpf(k)/2)/(iv.gamma(iv.mpf(k+n)/2)*iv.gamma(iv.mpf(k-1)/2))
 Bfirst=B(start);betafirst=beta(start)
 ws=[iv.mpf(0),iv.mpf(0)];ws[start%2]=iv.mpf(1);ws[(start+1)%2]=B(start+1)/Bfirst*betafirst/beta(start+1)
 D=[[iv.mpf(0) for q in qs] for p in qs]
 for j in range(start,N):
  R={p0:iv.mpf(1)}
  for p in range(p0,l+d):R[p+1]=R[p]*(j+p)*(j+n+2*l-2-p)/(2*p*(a-p))
  gs=[]
  for q in qs:
   c=iv.mpf(q*(2*q+n+2*l-3))/(n-1);g=iv.mpf(0)
   for e,coef in [(q-1,c),(q,c+1-l-2*q)]:
    if e>=0:
     for p in range(e+1):
      P=l+p
      if P>=p0:g+=coef*comb(e,p)*2**p*(-1)**(e-p)*R[P]
   gs.append(g)
  for u,p in enumerate(qs):
   for v,q in enumerate(qs[u:],u):D[u][v]+=ws[j%2]*(2*l-2+2*p+2*q)*gs[u]*gs[v]
  Brat=iv.mpf(((j+p0)*(j+p0+1))**2*(j+T)*(j+T+1))/((j+1)*(j+2)*((j+DD)*(j+DD+1))**2)*(j+alpha+2)/(j+alpha)
  betarat=iv.mpf((j+l+n+1)*(j+l))/((j+l+n)*(j+l-1))
  ws[j%2]*=Brat/betarat
 Kw=2*betafirst/Bfirst*(1+iv.mpf(n+2*l)/N)**(3*p0-2)
 Kr={p0:iv.mpf(1)}
 for p in range(p0,l+d):Kr[p+1]=Kr[p]*(1+iv.mpf(p)/N)*(1+iv.mpf(n+2*l-2-p)/N)/(2*p*(a-p))
 Kgs=[]
 for q in qs:
  c=iv.mpf(q*(2*q+n+2*l-3))/(n-1);bound=iv.mpf(0)
  for e,coef in [(q-1,c),(q,c+1-l-2*q)]:
   if e>=0:
    for p in range(e+1):
     P=l+p
     if P>=p0:bound+=abs(coef)*comb(e,p)*2**p*Kr[P]/N**(2*(l+q-P))
  Kgs.append(bound)
 for u,p in enumerate(qs):
  for v,q in enumerate(qs[u:],u):
   exponent=n-2*l-2*p-2*q
   err=(2*l-2+2*p+2*q)*Kw*Kgs[u]*Kgs[v]/(exponent*(N-1)**exponent)
   D[u][v]+=iv.mpf([-1,1])*err;D[v][u]=D[u][v]
 piv=[]
 for k in range(size):
  pivot=D[k][k];piv.append(pivot)
  if not bool(pivot>0):return False,piv
  for p in range(k+1,size):
   for q in range(p,size):D[p][q]-=D[p][k]*D[q][k]/pivot;D[q][p]=D[p][q]
 return True,piv

out=[]
for n in range(3,19):
 for l in range(0,(n-1)//2+1):
  d=(n-2*l-1)//4
  qstart=max(0,2-l)
  if d<qstart:continue
  good,piv=certify(n,l,d,N=10000)
  out.append((n,l,d,good,[str(p) for p in piv]))
  print(n,l,d,good,flush=True)
