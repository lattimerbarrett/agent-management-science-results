import numpy as np,json,sympy as sp
from math import comb,factorial
from collections import Counter
from functools import lru_cache
from sage.all import GF,matrix,QQ
from pathlib import Path
P=1000000007;W=25;q=sp.Rational(1,2);b=pow(2,P-2,P)
def conv(a,b):
 # avoid np.convolve overflow at largeprime by doing Python exactsum
 c=[0]*W
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b[:W-i]):c[i+j]=(c[i+j]+int(x)*int(y))%P
 return np.array(c,dtype=np.int64)
def unit():
 c=np.zeros(W,dtype=np.int64);c[0]=1;return c
G=[unit()]
for A in range(1,25):
 c=G[-1].copy();c[1:]=(c[1:]+((b+A-1)%P)*G[-1][:-1])%P;G.append(c)
C=[np.zeros(W,dtype=np.int64)]
for n in range(1,13):
 c=G[2*n].copy()
 for k in range(1,n):c=(c-(comb(n-1,k-1)%P)*conv(C[k],G[2*(n-k)]))%P
 C.append(c)
def parts(n,lo=1):
 if not n:yield ()
 for a in range(lo,n+1):
  for t in parts(n-a,a):yield(a,)+t
PP=[list(parts(i)) for i in range(13)]
H=[{():1}]
for n in range(1,13):
 out={}
 for k in range(1,n+1):
  mult=comb(n-1,k-1)
  for ks,a in H[n-k].items():
   for j in range(13-sum(ks)):
    cf=int(C[k][k+j])*((-1)**(j+1))*(48 if not j else 1)%P
    kk=tuple(sorted(ks+((j,) if j else ())))
    out[kk]=(out.get(kk,0)+a*cf*mult)%P
 H.append(out)
A={}
for j in range(1,13):
 qq=(-1)**(j-1)*sp.bernoulli(j+1,q)/j/(j+1);A[j]=int(qq.p)*pow(int(qq.q),P-2,P)%P
@lru_cache(None)
def E(ks):
 v=1
 for j,n in Counter(ks).items():v=v*pow(A[j],n,P)*pow(factorial(n)%P,P-2,P)%P
 return v
row={ks:0 for ks in PP[12]}
for ks,a in H[12].items():
 for ls in PP[12-sum(ks)]:
  kl=tuple(sorted(ks+ls));row[kl]=(row[kl]+a*E(ls))%P
ER=[row[ks] for ks in PP[12]];FR=[H[12].get(ks,0) for ks in PP[12]]
p=json.load(open('workspace/pairing25_agent2.json'));F=GF(P);M=matrix(F,p['matrix']);R=matrix(F,[ER,FR]);V=R*M
print('E F soclepairingrank',V.rank());print('pairingsfirstE/F',V[0,0],V[1,0]);print('differencezero',not any(V[0]-V[1]),'sumzero',not any(V[0]+V[1]))
f=json.load(open('workspace/agent3_fz25.json'));FZ=matrix(F,[[F(QQ(x)) for x in rr] for rr in f['rows']]);print('EFplusFZrank',FZ.stack(R).rank())
json.dump({'prime':P,'monomials':PP[12],'E':ER,'F':FR},open('workspace/agent2_spinEuler_critical25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_spinEuler_critical25.py').write_text(Path(__file__).read_text())
