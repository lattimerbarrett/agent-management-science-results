from itertools import combinations
from math import comb
n=12
triples=[sum(1<<i for i in I) for I in combinations(range(n),3)]
index={m:i for i,m in enumerate(triples)}
def flatten(terms):
    return [sum(1<<index[t^I] for t in terms if t&I==I) for I in triples]
def rank(rows):
    basis={}
    for row in rows:
        while row:
            k=row.bit_length()-1
            if k in basis: row^=basis[k]
            else:
                basis[k]=row
                break
    return len(basis)
alpha=[15|(3<<4),15|(3<<6)]
betaI=[15|(3<<4),15|(3<<6),15|(3<<8)]
betaII=[7|(7<<3),7|(7<<6)]
gamma=[63,63<<6]
ranks=[rank(flatten(x)) for x in [alpha,betaI,betaII,gamma]]
assert ranks==[32,44,38,40],ranks
S=flatten(alpha)
intersections=[]
for a in [2,3,4]:
    b=6-a
    W=list(range(a))+list(range(4,4+b))
    exterior=[1<<index[sum(1<<i for i in I)] for I in combinations(W,3)]
    dim=rank(S)+rank(exterior)-rank(S+exterior)
    formula=comb(a,3)+comb(a,2)*b+(a if b==4 else 0)
    assert dim==formula
    intersections.append(dim)
assert intersections==[6,10,16]
# Symmetric-matrix rank-sum inequality with bounded image intersections.
assert 32+38-2*comb(5,3)==50>40 # betaII
assert 32+44-2*max(intersections)==44>40 # betaI
print('Checked exterior obstruction: no degree6 leading forms of weights96,112,126 sum to0.')
