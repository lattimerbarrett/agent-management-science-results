import sys
from fractions import Fraction
from itertools import product
sys.path.insert(0,'workspace')
from agent3_embedding_checks import tree_example, check_embedding
r,c=tree_example()
print([check_embedding(t,r,c) for t in [3,4]])
# Independently count ideals by exhaustive subset enumeration for small grids,
# checking the exact plane-partition product used in the finite-range bound.
def pp(a,b,c):
    v=Fraction(1)
    for i in range(1,a+1):
        for j in range(1,b+1):
            v*=Fraction(i+j+c-1,i+j-1)
    assert v.denominator==1
    return v.numerator
for dims in [(1,1,1),(1,2,3),(2,2,2),(2,2,3)]:
    pts=list(product(*(range(x) for x in dims)))
    below=[]
    for p in pts:
        below.append(sum(1<<j for j,q in enumerate(pts) if all(x<=y for x,y in zip(q,p))))
    count=0
    for mask in range(1<<len(pts)):
        if all(mask&below[i]==below[i] for i in range(len(pts)) if mask>>i&1):
            count+=1
    assert count==pp(*dims)
    print('grid',dims,'exact ideals',count)
