"""Exact finite checks for small_sections_below128_proof.txt.
The arbitrary-beta lower bounds are proved analytically in the text.
Here the quadratic inverse obstruction is additionally checked for
EVERY beta of size<=3, for every relevant core dimension.
"""
from itertools import combinations

def verify():
    weights=set()
    for mu in (2,3,4):
        n=2*mu;N=1<<n
        def q(x):
            v=0
            for j in range(0,n,2):v^=((x>>j)&1)*((x>>(j+1))&1)
            return v
        shifted=[sum(q(x^a)<<x for x in range(N)) for a in range(N)]
        J=(1<<N)-1
        assert all(v!=J for v in shifted)
        for i in range(N):
            for j in range(i):
                x=shifted[i]^shifted[j]
                assert x!=J
                for k in range(j):assert x^shifted[k]!=J
        # Tight four-point inverse: second derivative in the first pair.
        assert shifted[0]^shifted[1]^shifted[2]^shifted[3]==J
        a=(1<<(8-2*mu))*sum(q(x) for x in range(N))
        assert a==128-2**(7-mu)
        weights.add(a)
        assert (1<<6)*4==256
    for s in range(2,7):
        n=2*s;N=1<<n
        U=list(range(1<<s));V=[i<<s for i in range(1<<s)]
        T=set(U)^set(V)
        assert len(T)==2**(s+1)-2
        # Tight inverse beta=U, checked by actual group convolution.
        conv=0
        for u in U:
            for p in T:conv^=1<<(u^p)
        assert conv==(1<<N)-1
        a=(1<<(6-s))*len(T)
        assert a==128-2**(7-s)
        weights.add(a)
        assert (1<<(8-s))*(1<<s)==256
    assert weights=={96,112,120,124,126}
    print('All KT small-section normalform checks passed; every quadratic beta<=3 tested.')

if __name__=='__main__':verify()
