from itertools import combinations
from functools import lru_cache
from pathlib import Path

K={21,38,74,67,176,200,82,137,97,69,152,146,41,131,28,44,133,164,22,76,112}
M=[48,1712,160,1648,1904,1874,1889,1392,353,1861,96,297,1633,80,33,837,1577,1065,594,2224,9,68,40,1362,66,1456,1859,1426,658,323,325,5,65,579,144,3,2194,18,130,643,387,393,2179,2185,2200,1161,1432,136,1176,24,389,129,901,2181,2212,132,932,1700,1580,1068,1052,1308,36,1302,812,12,534,844,796,20,1868,1100,72,1866,790,6,1098,1224,1992,806,550,2248,1574,192,789,34,586,10,277,1301,17]
priority={m:i for i,m in enumerate(M)}
def bits(f):return [1<<v for v in range(16) if f>>v&1]
def face(c):return sum(1<<v for v in c)
def subsets(f):
 s=f
 while True:
  yield s
  if not s:return
  s=(s-1)&f

def maximal(fs):
 fs=set(fs)
 return frozenset(f for f in fs if not any(f!=g and f&g==f for g in fs))

def data(f):
 counts=[sum(bool(f&(1<<(2*i+j))) for j in range(2)) for i in range(8)]
 support=sum(1<<i for i,c in enumerate(counts) if c)
 return counts,support

def key(f):
 c,s=data(f)
 marker=s if s.bit_count()==2 else s+256*(c.index(2)+1)
 return priority[marker],tuple(v for v in range(16) if f>>v&1)

allF={face(c) for c in combinations(range(16),4)}
facets={f for f in allF if data(f)[1].bit_count()==2 or data(f)[1] in K}
order=sorted(facets,key=key)
assert len(order)==280
assert {v for f in facets for v in range(16) if f>>v&1}==set(range(16))

# Literal intersections, not a restriction-face shortcut.
for i,f in enumerate(order[1:],1):
 I=maximal(f&g for g in order[:i])
 assert I and all(h.bit_count()==3 for h in I)
for f in allF-facets:
 I=maximal(f&g for g in facets)
 assert any(h.bit_count()<3 for h in I)

# Produce an explicit 2-decomposition DAG.
nodes=[]
def simplex(f):
 nodes.append(('s',f));return len(nodes)-1
def split(s,D,L):
 nodes.append(('d',s,D,L));return len(nodes)-1
def full_add(N,f):
 node=nodes[N];assert node[0]=='d'
 _,s,D,L=node
 if s&f==s:
  t=f^s;assert 1<=t.bit_count()<=3
  return split(s,D,split(t,L,simplex(0)))
 return split(s,full_add(D,f),L)

root=simplex(order[0]);old=set(subsets(order[0]))
for f in order[1:]:
 R=sum(v for v in bits(f) if f^v in old)
 assert R not in old
 if R.bit_count()<=3:root=split(R,root,simplex(f^R))
 else:
  assert R==f and set(subsets(f))-{f}<=old
  root=full_add(root,f)
 old.update(subsets(f))

# Verify the DAG directly against the problem's recursive definition.
@lru_cache(None)
def verify(N):
 node=nodes[N]
 if node[0]=='s':return frozenset([node[1]])
 _,s,D,L=node;DF=verify(D);LF=verify(L)
 assert 1<=s.bit_count()<=3
 assert all(g&s==0 for g in LF)
 fs=DF|frozenset(s|g for g in LF)
 assert len({f.bit_count() for f in fs})==1
 deletion=maximal([f for f in fs if f&s!=s]+[f^v for f in fs if f&s==s for v in bits(s)])
 link=maximal(f^s for f in fs if f&s==s)
 assert deletion==DF and link==LF
 assert {f.bit_count() for f in DF}=={f.bit_count() for f in fs}
 return fs
assert verify(root)==facets
print('Verified:',len(facets),'facets, explicit 2-decomposition,',len(allF-facets),'blocked missing facets.')
