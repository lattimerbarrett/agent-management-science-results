"""Necessary weight check for FOUR COORDINATE seven-flat indicators.
IMPORTANT: coordinate-direction arrangements ONLY, not arbitrary four flats.
For span12 or13, common direction0, and no pair direction intersection>=6,
all affine offsets give XOR weight>=320. This is not the missing K theorem.
"""
import itertools
triples=[7,11,13,14];pairs=[3,5,9,6,10,12]
def compositions(s,k):
 if k==1:yield (s,);return
 for a in range(s+1):
  for b in compositions(s-a,k-1):yield (a,)+b

def verify(n):
 count=0;minimum=999
 for ts in itertools.product(range(8),repeat=4):
  T=sum(ts)
  if T>14:continue
  base=[sum(ts[j] for j,m in enumerate(triples) if m>>i&1) for i in range(4)]
  if max(base)>7:continue
  P=28-n-2*T
  if P<0:continue
  for ps in compositions(P,6):
   deg=[base[i]+sum(ps[j] for j,m in enumerate(pairs) if m>>i&1) for i in range(4)]
   if max(deg)>7:continue
   # Force union direction span n and each arm dimension7.
   singles=[7-d for d in deg]
   assert sum(ts)+sum(ps)+sum(singles)==n
   pints=[ps[j]+sum(ts[k] for k,m in enumerate(triples) if m&p==p) for j,p in enumerate(pairs)]
   if max(pints)>5:continue
   forbidden={0}
   # On a pair atom, the two inactive flats can be equal or different.
   for j,p in enumerate(pairs):
    if ps[j]:
     edgebit=1<<pairs.index(15^p)
     forbidden|={g|edgebit for g in forbidden}
   # On a singleton atom, three inactive offsets can be equal, two equal,
   # or all different (the latter requires atom dimension>=2).
   for i,dim in enumerate(singles):
    if not dim:continue
    comp=[j for j in range(4) if j!=i];opts=[0]
    for z in comp:
     opts.append(sum(1<<j for j,p in enumerate(pairs) if p>>z&1 and not p>>i&1))
    if dim>=2:opts.append(sum(1<<j for j,p in enumerate(pairs) if not p>>i&1))
    forbidden={g|o for g in forbidden for o in opts}
   # For coordinate flats, every compatible family of pairwise consistent
   # coordinate constraints is globally consistent; hence all intersections
   # are determined by this forbidden-pair graph.
   for g in forbidden:
    w=512-2*sum(1<<p for j,p in enumerate(pints) if not g>>j&1)
    w+=4*sum(1<<t for k,t in enumerate(ts) if all(not g>>j&1 for j,p in enumerate(pairs) if p&triples[k]==p))
    w-=8 if g==0 else 0
    assert w>=320
    count+=1;minimum=min(minimum,w)
 print('n=',n,'checked',count,'coordinate Venn/offset profiles; min weight',minimum)
 return count
if __name__=='__main__':
 assert verify(12)==57465
 verify(13)
