import numpy as np,json,sympy as sp,time
from math import comb,factorial
from functools import lru_cache
from sage.all import GF,matrix,QQ
from pathlib import Path
P=1000003;W=27;q=sp.Rational(7,16);b=int((1-q).p)*pow(int((1-q).q),P-2,P)%P
start=time.time()
def conv(a,b):return np.convolve(a,b)[:W]%P
def unit():
 c=np.zeros(W,dtype=np.int64);c[0]=1;return c
G=[unit()]
for A in range(1,29):
 c=G[-1].copy();c[1:]=(c[1:]+((b+A-1)%P)*G[-1][:-1])%P;G.append(c)
C=[np.zeros(W,dtype=np.int64)]
for n in range(1,15):
 c=G[2*n].copy()
 for k in range(1,n):c=(c-(comb(n-1,k-1)%P)*conv(C[k],G[2*(n-k)]))%P
 C.append(c)

def parts(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in parts(n-a,a):yield(a,)+t
PP=[list(parts(i)) for i in range(13)]
# H_n polynomial kappa push of c(F_D) with n weight-2 labelled slots.
H=[{():1}]
for n in range(1,15):
 out={}
 for k in range(1,n+1):
  mult=comb(n-1,k-1)
  for ks,a in H[n-k].items():
   for j in range(13-sum(ks)):
    if k+j>=W:continue
    coeff=int(C[k][k+j])*((-1)**(j+1))*(48 if j==0 else 1)%P
    kk=tuple(sorted(ks+((j,) if j else ())))
    out[kk]=(out.get(kk,0)+a*coeff*mult)%P
 H.append(out)
A={}
for j in range(1,13):
 qq=(-1)**(j-1)*sp.bernoulli(j+1,q)/j/(j+1)
 A[j]=int(qq.p)*pow(int(qq.q),P-2,P)%P
@lru_cache(None)
def E(ks):
 from collections import Counter
 v=1
 for j,n in Counter(ks).items():v=v*pow(A[j],n,P)*pow(factorial(n)%P,P-2,P)%P
 return v
row={ks:0 for ks in PP[12]}
for ks,a in H[14].items():
 for ls in PP[12-sum(ks)]:
  kl=tuple(sorted(ks+ls));row[kl]=(row[kl]+a*E(ls))%P
r=[row[ks] for ks in PP[12]];f=json.load(open('workspace/agent3_fz25.json'));F=GF(P);M=matrix(F,[[F(QQ(x)) for x in rr] for rr in f['rows']]);MR=M.stack(matrix(F,[r]));print('CRITICAL POSITIVE SPIN relation nonzero',sum(bool(x) for x in r),'combinedrank',MR.rank(),flush=True)
json.dump({'prime':P,'q':str(q),'monomials':PP[12],'row':r},open('workspace/agent2_posspin_7over16.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_posspin_7over16.py').write_text(Path(__file__).read_text())
