"""Exact Weyl-dimension checks for irreducible homogeneous bundles.
This does NOT establish that arbitrary low-rank uniform bundles are homogeneous.
It verifies the list of possible irreducible GL(n) modules under the rank cutoff,
modulo determinant twists, conditional on the geometric classification.
"""
from itertools import combinations_with_replacement
from fractions import Fraction

def dim_GL(partition):
    n=len(partition)
    d=Fraction(1)
    for i in range(n):
        for j in range(i+1,n):
            d*=Fraction(partition[i]-partition[j]+j-i,j-i)
    assert d.denominator==1
    return d.numerator

def candidates(n):
    cutoff=2*n-1
    # If lambda_1 >= cutoff, dim >= lambda_1+1 > cutoff.
    # This elementary bound follows already from one root SL(2) string.
    out=[]
    for asc in combinations_with_replacement(range(cutoff),n-1):
        p=tuple(reversed(asc))+(0,)
        d=dim_GL(p)
        if d<=cutoff:
            out.append((p,d))
    return sorted(out)

expected={
 2:[((0,0),1),((1,0),2),((2,0),3)],
 3:[((0,0,0),1),((1,0,0),3),((1,1,0),3)],
 4:[((0,0,0,0),1),((1,0,0,0),4),((1,1,0,0),6),((1,1,1,0),4)]
}
if __name__=='__main__':
    for n in (2,3,4):
        found=candidates(n)
        assert found==expected[n],(n,found)
        print('GL(%d), rank < %d:'%(n,2*n),found)
