import pickle,json,sys
from itertools import combinations
from collections import Counter
sys.path.insert(0,'workspace')
from agent2_checker import verify,bits
D=pickle.load(open('workspace/agent2_seed16_certificate.pkl','rb'))
fs=tuple(sorted(D['facets']));assert verify(fs,1,D['certificate'])
q,m=D['q'],D['m'];n=8*m
base=json.load(open('workspace/agent3_small_seed.json'));T0=[frozenset(t) for t in base['T0']];S={frozenset(t) for t in base['T']}
faces=set();restrictions=[]
for f in T0:
 new=[frozenset(c) for r in range(4) for c in combinations(f,r) if frozenset(c) not in faces]
 mins=[s for s in new if not any(t<s for t in new)]
 assert len(mins)==1
 restrictions.append(tuple(sorted(mins[0])))
 faces.update(frozenset(c) for r in range(4) for c in combinations(f,r))
assert len({s for s in faces if len(s)==2})==28
hist=Counter(sum(frozenset(t) in S for t in combinations(f,3)) for f in combinations(range(8),4));assert hist[3]==0
tri={sum(c) for f in fs for c in combinations(bits(f),3)};edges={sum(c) for f in fs for c in combinations(bits(f),2)}
def barrier(t):
 p=frozenset(v//m for v in t)
 return len(p)<=2 or p in S
assert len(edges)==n*(n-1)//2
assert all(barrier([v.bit_length()-1 for v in bits(t)]) for t in tri)
for f in combinations(range(n),4):assert sum(barrier(t) for t in combinations(f,3))!=3
print('INDEPENDENT AUDIT PASSED:',len(fs),'tetrahedra,',len(edges),'edges,',len(tri),'triangles; originalrecursiveverifier plusall1820barrierquadruples.')
print('basehist',dict(hist),'restrictions',restrictions)