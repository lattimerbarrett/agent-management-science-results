"""Compute lambda(7) from all upsets of B5; no tabulated inputs."""
import numpy as np
from agent3_D7 import ideals_B4

def reverse32(n):
    return int(format(n,'032b')[::-1],2)

def compute_lambda7():
    # Build all 7581 ideals of B5 as pairs (I0,I1), I1 subset I0.
    L4=ideals_B4()
    ideals5=[I0|(I1<<16) for I0 in L4 for I1 in L4 if I0&I1==I1]
    assert len(ideals5)==7581
    F=np.array([(1<<32)-1-I for I in ideals5],dtype=np.uint64)
    reverse=np.array([reverse32(int(U)) for U in F],dtype=np.uint64)
    count=0;D6=0
    for F0 in F:
        nested=(F0 & F)==F0
        D6+=int(np.count_nonzero(nested))
        count+=int(np.count_nonzero(nested & ((F0 & reverse)==0)))
    # Upsets of B6 are pairs F0 subset F1 of B5 upsets.
    # They are intersecting iff F0 has no set disjoint from an F1 set,
    # equivalently F0 misses complement(F1), by upward closure.
    return count,D6

if __name__=='__main__':
    lam,D6=compute_lambda7()
    assert lam==1422564
    assert 2*783558>lam+1
    print('computed lambda7, D6:',lam,D6)
