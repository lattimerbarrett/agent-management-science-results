import sys,json,pickle
sys.path.insert(0,'workspace')
import agent3_lower as L
from sage.all import matrix,QQ
cols,rels,labels=pickle.load(open('workspace/agent3_fz_QQ.pkl','rb'))
mons=cols[33:]
A=matrix(QQ,[[L.exact_integral(tuple(sorted(a+b,reverse=True))) for b in L.cols] for a in mons])
assert A.rank()==43
K=A.left_kernel();assert K.dimension()==1
v=K.basis()[0]
D=json.load(open('workspace/agent3_radical.json'))
assert tuple(tuple(m) for m in D['monomials'])==tuple(mons)
assert list(v)==list(map(QQ,D['coefficients']))
assert not any(v*A)
# Its polynomial is not a consequence of the established FZ relations.
rad=[QQ(0)]*77
for a,c in zip(mons,v):rad[cols.index(a)]=c
assert matrix(QQ,rels).rank()==33
assert matrix(QQ,rels+[rad]).rank()==34
print('Verified: exact one-dimensional pairing radical; nonzero in 44-dimensional FZ quotient.')
print('This does NOT certify nonzero in the actual Chow ring.')
