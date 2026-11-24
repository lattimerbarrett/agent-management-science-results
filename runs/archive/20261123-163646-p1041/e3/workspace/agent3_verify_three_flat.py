"""Necessary intersection arithmetic for sums of three affine 7-flats.
This DOES NOT assert all low RM weights have such a decomposition.
"""
from itertools import product

def possible_three_flat_weights():
    sizes=[0]+[1<<i for i in range(8)]
    out=set()
    for p,q,r,t in product(sizes,repeat=4):
        if t>min(p,q,r): continue
        # Each pair of intersections is contained in one 128-point flat.
        if max(p+q-t,p+r-t,q+r-t)>128: continue
        if t:
            # In a common translate, dimensions obey dim(E+F)<=7.
            if max(p*q,p*r,q*r)>128*t: continue
        elif min(p,q,r)>0:
            # Pair intersections are disjoint cosets inside each flat.
            # Let h=dim of common direction space. Then
            # log2(p)+log2(q)-h <=6 and 2**h<=min(p,q,r).
            if max(p*q,p*r,q*r)>64*min(p,q,r): continue
        out.add(384-2*(p+q+r)+4*t)
    return out

def verify():
    got={w for w in possible_three_flat_weights() if 256<w<336}
    expected={272,288,296,304,308,312,314,316,318,320,324,328,332}
    assert got==expected,(got,expected)
    assert not got.intersection({322,326,330,334})
    print('All sums of three affine 7-flat indicators have no forbidden weight in (256,336).')
    print('WARNING: additional structural theorem is needed to apply this to arbitrary Reed-Muller words.')
if __name__=='__main__':verify()
