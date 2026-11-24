"""Exact GF(2) contraction/divisor ranks for every canonical form used in bootstrap."""
from itertools import combinations
from math import comb

def rk(rows):
 piv={}
 for v in rows:
  while v:
   k=v.bit_length()-1
   if k in piv:v^=piv[k]
   else:piv[k]=v;break
 return len(piv)
def masks(n,k):return [sum(1<<i for i in C) for C in combinations(range(n),k)]
def flatten(T,p,k,n):
 R={m:0 for m in masks(n,k)};C={m:i for i,m in enumerate(masks(n,p-k))}
 for t in T:
  positions=[i for i in range(n) if t>>i&1]
  for I in combinations(positions,k):
   a=sum(1<<i for i in I);R[a]^=1<<C[t^a]
 return rk(R.values())
def quad(p,mu):
 f=(1<<(p-2))-1
 return {f|(1<<(p-2+2*i))|(1<<(p-1+2*i)) for i in range(mu)}
def pair(p,mu):
 t=p-mu;f=(1<<t)-1
 return {f|(((1<<mu)-1)<<t),f|(((1<<mu)-1)<<(t+mu))}
def ann(T,p,n):
 C={m:i for i,m in enumerate(masks(n,p+1))};rows=[]
 for i in range(n):
  v=0
  for t in T:
   if not(t>>i&1):v^=1<<C[t|(1<<i)]
  rows.append(v)
 return n-rk(rows)
expected={
 4:{'min':6,'second':10,'quad6':14,'pair3':12,'pair4':12},
 5:{'min':10,'second':16,'quad6':22,'pair3':19,'pair4':20,'pair5':20},
 6:{'min':20,'second':32,'quad6':44,'pair3':38,'pair4':40,'pair5':40},
 7:{'min':35,'second':55,'quad6':75,'pair3':65,'pair4':69,'pair5':70},
}
for p in range(4,8):
 n=p+5;k=2 if p<=5 else 3
 forms={'min':{(1<<p)-1},'second':quad(p,2),'quad6':quad(p,3)}
 for mu in range(3,min(p,5)+1):forms['pair'+str(mu)]=pair(p,mu)
 actual={name:flatten(T,p,k,n) for name,T in forms.items()}
 assert actual==expected[p],(p,actual,expected[p])
 print('p',p,'contraction',k,actual)
 # Every low KT type has precisely the indicated pure common divisor space.
 assert ann(forms['second'],p,n)==p-2
 assert ann(forms['quad6'],p,n)==p-2
 for mu in range(3,min(p,5)+1):assert ann(forms['pair'+str(mu)],p,n)==p-mu
 # Primitive48-annihilator lemma: outside-support wedge has divisor dimension p-1;
 # inside-support wedge is decomposable, with divisor dimension p+1.
 if p>=6:
  T=forms['second'];outside=1<<(p+2);inside=1<<(p-2)
  assert ann({t|outside for t in T},p+1,n)==p-1
  U={t|inside for t in T if not t&inside}
  assert ann(U,p+1,n)==p+1
print('Every canonical KT contraction/divisor-rank certificate PASS')
