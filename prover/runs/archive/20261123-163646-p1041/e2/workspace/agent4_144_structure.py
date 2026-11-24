"""Exact finite linear algebra for the 144-point quadric graph-lift seed.
This proves a property of this seed and its graph lifts, not of all codewords.
"""
import sys,itertools
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese
Q=[x for x in range(64) if sum(((x>>(2*i))&1)*((x>>(2*i+1))&1) for i in range(3))%2==0]
S=[x for x in range(256) if x%64 in Q]
assert len(Q)==36 and len(S)==144

def rank(vectors):
    bs={}
    for v in vectors:
        while v:
            j=v.bit_length()-1
            if j in bs:v^=bs[j]
            else:bs[j]=v;break
    return len(bs)

def eval_rank(points,m,d):
    V=veronese(m,d)
    return rank(V[x] for x in points)

# Tensor decomposition: these ranks imply K=K0(Q)+<u,v>.
assert eval_rank(Q,6,2)==21
assert eval_rank(Q,6,3)==35
assert eval_rank(Q,6,4)==36
V=veronese(8,4)
basis={};K=[]
for i,x in enumerate(S):
    v=V[x];c=1<<i
    while v:
        j=v.bit_length()-1
        if j not in basis:basis[j]=(v,c);break
        w,b=basis[j];v^=w;c^=b
    if not v:K.append(c)
assert len(K)==17
idx={x:i for i,x in enumerate(S)}
for v in [64,128]:
    for h in K:
        assert len({(h>>i&1)^(h>>idx[x^v]&1) for i,x in enumerate(S)})==1
assert all((h&k).bit_count()%2==0 for h in K for k in K)
print('Verified ranks21/35/36, Kdim17, constant radical derivatives, and selforthogonality.')
