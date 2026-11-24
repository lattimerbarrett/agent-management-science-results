from mpmath import iv
from math import comb
iv.dps=30

def Cmat(n,l,d,N=3000):
 a=iv.mpf(n+2*l-3)/2;alpha=a+iv.mpf('.5');T=n+2*l-2;DD=n+l-1;start=max(0,2-l)
 def B(j):return iv.gamma(j+l)**2*iv.gamma(j+T)*(j+alpha)/(iv.gamma(j+1)*iv.gamma(j+DD)**2)
 def beta(j):
  k=j+l
  return 2*iv.gamma(iv.mpf(k+n+1)/2)*iv.gamma(iv.mpf(k)/2)/(iv.gamma(iv.mpf(k+n)/2)*iv.gamma(iv.mpf(k-1)/2))
 Bfirst=B(start);betafirst=beta(start)
 I=2**(2*a-l+1)*iv.gamma(a+1)*iv.gamma(a-l+1)/iv.gamma(2*a-l+2)*(1 if start==0 else l*(2*a+1)/(2*a-l+2))
 h=iv.pi*2**(1-2*alpha)*iv.gamma(start+2*alpha)/(iv.factorial(start)*(start+alpha)*iv.gamma(alpha)**2)
 norm=I**2/h/betafirst
 ws=[iv.mpf(0),iv.mpf(0)];ws[start%2]=iv.mpf(1);ws[(start+1)%2]=B(start+1)/Bfirst*betafirst/beta(start+1)
 C=[[iv.mpf(0) for q in range(d+1)] for p in range(d+1)]
 for j in range(start,N):
  R={l:iv.mpf(1)}
  for p in range(l,l+d):R[p+1]=R[p]*(j+p)*(j+n+2*l-2-p)/(2*p*(a-p))
  gs=[]
  for q in range(d+1):
   c=iv.mpf(q*(2*q+n+2*l-3))/(n-1);g=iv.mpf(0)
   for e,coef in [(q-1,c),(q,c+1-l-2*q)]:
    if e>=0:
     for p in range(e+1):g+=coef*comb(e,p)*2**p*(-1)**(e-p)*R[l+p]
   gs.append(g)
  for u in range(d+1):
   for v in range(u,d+1):C[u][v]+=ws[j%2]*gs[u]*gs[v]
  Brat=iv.mpf(((j+l)*(j+l+1))**2*(j+T)*(j+T+1))/((j+1)*(j+2)*((j+DD)*(j+DD+1))**2)*(j+alpha+2)/(j+alpha)
  betarat=iv.mpf((j+l+n+1)*(j+l))/((j+l+n)*(j+l-1))
  ws[j%2]*=Brat/betarat
 Kw=2*betafirst/Bfirst*(1+iv.mpf(n+2*l)/N)**(3*l-2)
 Kr={l:iv.mpf(1)}
 for p in range(l,l+d):Kr[p+1]=Kr[p]*(1+iv.mpf(p)/N)*(1+iv.mpf(n+2*l-2-p)/N)/(2*p*(a-p))
 Kgs=[]
 for q in range(d+1):
  c=iv.mpf(q*(2*q+n+2*l-3))/(n-1);bound=iv.mpf(0)
  for e,coef in [(q-1,c),(q,c+1-l-2*q)]:
   if e>=0:
    for p in range(e+1):bound+=abs(coef)*comb(e,p)*2**p*Kr[l+p]/N**(2*(q-p))
  Kgs.append(bound)
 for u in range(d+1):
  for v in range(u,d+1):
   exponent=n-2*l-2*u-2*v
   err=Kw*Kgs[u]*Kgs[v]/(exponent*(N-1)**exponent)
   C[u][v]=(C[u][v]+iv.mpf([-1,1])*err)*norm;C[v][u]=C[u][v]
 return C

def quad(P,C,Q):return sum(P[i]*C[i][j]*Q[j] for i in range(len(P)) for j in range(len(Q)))
if __name__=='__main__':
 n=19;m=18;lam=iv.mpf(['.94993','.94994'])
 P=[iv.mpf(x)*lam**(2*i) for i,x in enumerate(['1','-.46283557','.05655270','-.00140805'])]
 C1=Cmat(n,1,3);C2=Cmat(n,2,3);C3=Cmat(n,3,2)
 for rho in [iv.mpf(0),iv.mpf(1)]:
  R1=[P[i]*(2+iv.mpf(4*i)/(m+2)) for i in range(4)]
  R3=[2*i*P[i] for i in range(1,4)]
  R2=[i*P[i]*((2+8*rho)+4*(1+4*rho)*(i-1)/(m+4)) for i in range(1,4)]
  H=-((m+2)*rho/2*quad(R1,C1,R1)+(1+2*m*rho/(m+2))/(m+4)*quad(R3,C3,R3)+quad(P,C2,R2))/C2[0][0]
  print('rho',rho,'Hessian/C200',H,flush=True)
  assert bool(H>0)
