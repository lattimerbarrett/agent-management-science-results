import json,itertools,time,pickle
n=13;S=set(json.load(open('T316_projection_example.json')))
# Veronese columns, indexed by squarefree monomials of degrees <=5.
mons=[sum(1<<j for j in t) for d in range(6) for t in itertools.combinations(range(n),d)]
V=[0]*(1<<n)
for i,mask in enumerate(mons):
 free=((1<<n)-1)^mask;t=free
 while True:
  V[mask|t]|=1<<i
  if not t:break
  t=(t-1)&free
basis={}
for p in S:
 v=V[p]
 while v:
  j=v.bit_length()-1
  if j not in basis:basis[j]=v;break
  v^=basis[j]
def reduce(v):
 for j in sorted(basis,reverse=True):
  if v>>j&1:v^=basis[j]
 return v
out=[(p,reduce(V[p])) for p in range(1<<n) if p not in S]
D={v:p for p,v in out};print('support',len(S),'rank',len(basis),'outside',len(out),'one point relation',0 in D,flush=True)
t=time.time();found=None
for i,(p,v) in enumerate(out):
 for q,w in out[:i]:
  x=v^w
  if x in D:
   r=D[x]
   if r!=p and r!=q:found=(p,q,r);break
 if found:break
print('three point relation',found,'elapsed',time.time()-t)
