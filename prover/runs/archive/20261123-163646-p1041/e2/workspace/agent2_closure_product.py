import itertools
from pathlib import Path

def ver(m,d):
 masks=[s for s in range(1<<m) if s.bit_count()<=d]
 return [sum(1<<j for j,s in enumerate(masks) if x&s==s) for x in range(1<<m)]
def closure(S,vs):
 bs={}
 for p in S:
  v=vs[p]
  while v:
   k=v.bit_length()-1
   if k in bs:v^=bs[k]
   else:bs[k]=v;break
 out=set()
 for p,v in enumerate(vs):
  while v:
   k=v.bit_length()-1
   if k not in bs:break
   v^=bs[k]
  if not v:out.add(p)
 return out
checks=0
for m in range(0,4):
 for d in range(0,4):
  v=ver(m,d);vv=ver(m+1,d)
  for bits in range(1<<(1<<m)):
   S={x for x in range(1<<m) if bits>>x&1};prod=S|{x|(1<<m) for x in S}
   C=closure(S,v);CC=closure(prod,vv)
   assert CC==C|{x|(1<<m) for x in C};checks+=1
for w in (160,162,164,166):
 assert w+1<192
 assert 0<w-126<64
print('Closure-product identity exhaustive checks:',checks)
print('Periodic precursor contradiction arithmetic checked for160/162/164/166')
Path('workspace/agent2_closure_product.py').write_text(Path(__file__).read_text())
