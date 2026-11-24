from mpmath import iv
from pathlib import Path
iv.dps=35
N=10000
v=[iv.mpf(1),-iv.mpf(46284)/100000,iv.mpf(5655)/100000,-iv.mpf(1408)/1000000]
b0=2*iv.gamma(11)/(iv.gamma(iv.mpf('10.5'))*iv.gamma(iv.mpf('.5')))
b1=2*iv.gamma(iv.mpf('11.5'))*iv.gamma(iv.mpf('1.5'))/iv.gamma(11)
weights=[iv.mpf(1),iv.mpf(23)/100*b0/b1]
sumq=iv.mpf(0)
from math import comb
for j in range(N):
 w=weights[j%2]
 R=[iv.mpf(1)]
 for p in range(2,5): R.append(R[-1]*(j+p)*(j+21-p)/(2*p*(10-p)))
 gs=[]
 for q in range(4):
  c=iv.mpf(q*(2*q+20))/18
  g=iv.mpf(0)
  for e,coef in [(q-1,c),(q,c-1-2*q)]:
   if e>=0:
    for p in range(e+1):g+=coef*comb(e,p)*2**p*(-1)**(e-p)*R[p]
  gs.append(g)
 S=sum(v[q]*gs[q] for q in range(4)); T=sum(q*v[q]*gs[q] for q in range(4))
 sumq+=w*(2*S*S+4*S*T)
 weights[j%2]*=iv.mpf((j+3)**2)/((j+20)**2)*iv.mpf(2*j+25)/(2*j+21)
print('partial',sumq)
# Absolute tail estimate derived from log-convexity of Gamma and rational factors
Kw=2*b0*iv.factorial(20)/4200*(1+iv.mpf(20)/N)**5
Kr=[iv.mpf(1)]
for p in range(2,5):Kr.append(Kr[-1]*(1+iv.mpf(p)/N)*(1+iv.mpf(21-p)/N)/(2*p*(10-p)))
Kgs=[]
for q in range(4):
 c=iv.mpf(q*(2*q+20))/18
 bound=iv.mpf(0)
 for e,coef in [(q-1,c),(q,c-1-2*q)]:
  if e>=0:
   for p in range(e+1):bound+=abs(coef)*comb(e,p)*2**p*Kr[p]/N**(2*(q-p))
 Kgs.append(bound)
Ks=sum(abs(v[q])*Kgs[q]/N**(2*(3-q)) for q in range(4))
tail=14*Kw*Ks*Ks/(3*(N-1)**3)
print('absolute tail upper',tail)
print('whole upper enclosure',sumq+iv.mpf([-1,1])*tail)
