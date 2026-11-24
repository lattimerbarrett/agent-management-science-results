import json,itertools
TRIANGLES=[21, 38, 74, 67, 176, 200, 82, 137, 97, 69, 152, 146, 41, 131, 28, 44, 133, 164, 22, 76, 112]
MARKERS=[48, 1712, 160, 1648, 1904, 1874, 1889, 1392, 353, 1861, 96, 297, 1633, 80, 33, 837, 1577, 1065, 594, 2224, 9, 68, 40, 1362, 66, 1456, 1859, 1426, 658, 323, 325, 5, 65, 579, 144, 3, 2194, 18, 130, 643, 387, 393, 2179, 2185, 2200, 1161, 1432, 136, 1176, 24, 389, 129, 901, 2181, 2212, 132, 932, 1700, 1580, 1068, 1052, 1308, 36, 1302, 812, 12, 534, 844, 796, 20, 1868, 1100, 72, 1866, 790, 6, 1098, 1224, 1992, 806, 550, 2248, 1574, 192, 789, 34, 586, 10, 277, 1301, 17]
priority={x:i for i,x in enumerate(MARKERS)}
O=[]
for f in itertools.combinations(range(16),4):
    counts=[sum(v//2==i for v in f) for i in range(8)]
    origins=sum(1<<i for i in range(8) if counts[i])
    if origins.bit_count()==2:
        marker=origins
    elif origins in TRIANGLES:
        p=next(i for i in range(8) if counts[i]==2)
        marker=origins+256*(p+1)
    else:continue
    O.append((priority[marker],f))
O=[sum(1<<v for v in f) for _,f in sorted(O)]
assert len(O)==280
k=2

nodes=[];cache={}
def simplex(F):
 key=('s',F)
 if key not in cache:cache[key]=len(nodes);nodes.append(key)
 return cache[key]
def split(s,D,L):
 key=('d',s,D,L)
 if key not in cache:cache[key]=len(nodes);nodes.append(key)
 return cache[key]
def full_add(N,F):
 node=nodes[N]
 assert node[0]=='d',('fullboundaryon simplex impossible',node,F)
 _,s,D,L=node
 if s&F==s:
  tau=F^s
  assert 1<=tau.bit_count()<=k+1
  return split(s,D,split(tau,L,simplex(0)))
 return split(s,full_add(D,F),L)
def subs(F):
 s=F
 while True:
  yield s
  if not s:return
  s=(s-1)&F
root=simplex(O[0]);faces=set(subs(O[0]))
for F in O[1:]:
 R=0
 for v in range(16):
  if F>>v&1 and F^(1<<v) in faces:R|=1<<v
 assert R not in faces
 if R.bit_count()<=k+1:root=split(R,root,simplex(F^R))
 else:
  assert R==F and all(s in faces for s in subs(F) if s!=F)
  root=full_add(root,F)
 faces.update(subs(F))
# Independent tree verifier from recursive definition, no shelling shortcuts.
verified={}
def verify(N):
 if N in verified:return verified[N]
 node=nodes[N]
 if node[0]=='s':answer=frozenset([node[1]])
 else:
  _,s,D,L=node;DF=verify(D);LF=verify(L)
  assert 1<=s.bit_count()<=k+1
  assert all(not(s&g) for g in LF)
  assert all(f&s!=s for f in DF)
  SF={s|g for g in LF};answer=frozenset(set(DF)|SF)
  sizes={f.bit_count() for f in answer};assert len(sizes)==1
  assert {f.bit_count() for f in DF}==sizes
  for F in SF:
   for v in range(16):
    if s>>v&1:
     H=F^(1<<v)
     assert any(H&g==H for g in DF),(N,s,F,H)
 verified[N]=answer
 return answer
assert verify(root)==frozenset(O)
print('EXPLICIT2DECOMPOSITION VERIFIED','nodes',len(nodes),'reachable',len(verified),'facets',len(O),'root',root,flush=True)

# Literal subset/maximal-intersection verification of every forbidden first step.
old=set().union(*(set(subs(f)) for f in O))
assert set(i for f in O for i in range(16) if f>>i&1)==set(range(16))
blocked=0
for vertices in itertools.combinations(range(16),4):
    F=sum(1<<v for v in vertices)
    if F in O:continue
    intersection=[s for s in subs(F) if s in old]
    maximal=[s for s in intersection if not any(t!=s and s&t==s for t in intersection)]
    assert any(s.bit_count()<3 for s in maximal)
    blocked+=1
assert blocked==1540
print('All 1540 missing tetrahedra blocked; b(3,2)>=1, contrary to requested value 0.')
