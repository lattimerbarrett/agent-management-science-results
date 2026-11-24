from mpmath import iv
from math import comb
from pathlib import Path
iv.dps=30

def certify(n,N=10000):
 a=iv.mpf(n+1)/2
 beta0=2*iv.gamma(iv.mpf(n+3)/2)/(iv.gamma(iv.mpf(n+2)/2)*iv.gamma(iv.mpf('.5')))
 beta1=2*iv.gamma(iv.mpf(n+4)/2)*iv.gamma(iv.mpf('1.5'))/iv.gamma(iv.mpf(n+3)/2)
 B1B0=iv.mpf(4*(n+2)*(n+4))/((n+1)**2*(n+2)) # simplify? actual 4*(n+2)^2*((n+4)/(n+2))/(n+1)^2/(n+2)=4*(n+4)/(n+1)^2
 B1B0=iv.mpf(4*(n+4))/(n+1)**2
 ws=[iv.mpf(1),B1B0*beta0/beta1]
 D=[[iv.mpf(0) for j in range(4)] for i in range(4)]
 for j in range(N):
  R=[iv.mpf(1)]
  for p in range(2,5):R.append(R[-1]*(j+p)*(j+n+2-p)/(2*p*(a-p)))
  gs=[]
  for q in range(4):
   c=iv.mpf(q*(2*q+n+1))/(n-1);g=iv.mpf(0)
   for e,coef in [(q-1,c),(q,c-1-2*q)]:
    if e>=0:
     for p in range(e+1):g+=coef*comb(e,p)*2**p*(-1)**(e-p)*R[p]
   gs.append(g)
  for p in range(4):
   for q in range(p,4):D[p][q]+=ws[j%2]*(2+2*p+2*q)*gs[p]*gs[q]
  ws[j%2]*=iv.mpf((j+3)**2)/((j+n+1)**2)*iv.mpf(2*j+n+6)/(2*j+n+2)
 # w <= Kw*j^(3-n), j>=N, via beta>=j/2
 Kw=2*beta0*iv.factorial(n+1)/((n+1)**2*iv.mpf(n+2)/2)*(1+iv.mpf(n+1)/N)**5
 Kr=[iv.mpf(1)]
 for p in range(2,5):Kr.append(Kr[-1]*(1+iv.mpf(p)/N)*(1+iv.mpf(n+2-p)/N)/(2*p*(a-p)))
 Kgs=[]
 for q in range(4):
  c=iv.mpf(q*(2*q+n+1))/(n-1);bound=iv.mpf(0)
  for e,coef in [(q-1,c),(q,c-1-2*q)]:
   if e>=0:
    for p in range(e+1):bound+=abs(coef)*comb(e,p)*2**p*Kr[p]/N**(2*(q-p))
  Kgs.append(bound)
 for p in range(4):
  for q in range(p,4):
   exponent=n-4-2*p-2*q
   err=(2+2*p+2*q)*Kw*Kgs[p]*Kgs[q]/(exponent*(N-1)**exponent)
   D[p][q]+=iv.mpf([-1,1])*err;D[q][p]=D[p][q]
 # Interval LDL positive pivots certify positive definiteness.
 piv=[]
 for k in range(4):
  pivot=D[k][k];piv.append(pivot)
  for p in range(k+1,4):
   for q in range(p,4):
    D[p][q]-=D[p][k]*D[q][k]/pivot;D[q][p]=D[p][q]
 print(n,'pivots',piv)
for n in [17,18]:certify(n)
