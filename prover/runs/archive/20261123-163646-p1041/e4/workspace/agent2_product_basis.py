import itertools,math,collections,pickle

def parts(n,lo=1):
 if n==0:yield ()
 for k in range(lo,min(7,n)+1):
  for p in parts(n-k,k):yield (k,)+p

def data(p):
 t=len(p);N=1<<t;weights=[math.prod((1<<k)-1 for i,k in enumerate(p) if not z>>i&1) for z in range(N)]
 allowed=[z for z,w in enumerate(weights) if w<=334];idx={z:i for i,z in enumerate(allowed)};piv={}
 for m in range(N):
  if sum(p[i] for i in range(t) if m>>i&1)<=7:continue
  sub=m;v=0
  while True:
   if sub in idx:v^=1<<idx[sub]
   if sub==0:break
   sub=(sub-1)&m
  while v:
   i=v.bit_length()-1
   if i in piv:v^=piv[i]
   else:piv[i]=v;break
 free=[i for i in range(len(allowed)) if i not in piv];basis=[]
 for j in free:
  b=1<<j
  for i in sorted(piv):
   if (b&piv[i]).bit_count()%2:b^=1<<i
  basis.append(b)
 return [weights[z] for z in allowed],allowed,basis