"""Checked geometric span bound for XOR of three affine six-flats.
Any such XOR of weight <=156 has affine span <=13.
The cutoff cannot be replaced by158: explicit full-span14 counterexample.
This does NOT assert arbitrary low RM words are triple-flat XORs.
"""
from itertools import product

def gf2rank(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j not in piv:piv[j]=x;break
            x^=piv[j]
    return len(piv)

def flat(bs,offset=0):
    pts={offset}
    for b in bs:pts|={x^b for x in list(pts)}
    return pts

def verify():
    U=flat([1<<i for i in range(6)])
    V=flat([1<<i for i in [0,1,2,3,6,7]])
    W=flat([1<<i for i in range(8,14)],1<<4)
    S=U^V^W
    assert (len(U&V),len(U&W),len(V&W),len(U&V&W))==(16,1,0,0)
    assert len(S)==158
    o=next(iter(S));assert gf2rank([x^o for x in S])==14
    # Three nonempty pair intersections, nonempty triple.
    for p,q,r,a in product(range(7),repeat=4):
        if min(p,q,r)<a:continue
        if max(p+q-a,p+r-a,q+r-a)>6:continue
        w=192-2*((1<<p)+(1<<q)+(1<<r))+4*(1<<a)
        if 0<w<=156:assert 18-p-q-r+a<=13
    # Triangle of nonempty pairs but empty triple. Directional common
    # intersection h, and an extra cycle relation in W intersection(U+V).
    for p,q,r,h in product(range(7),repeat=4):
        if min(p,q,r)<h:continue
        if max(p+q-h,p+r-h,q+r-h)>5:continue
        w=192-2*((1<<p)+(1<<q)+(1<<r))
        if 0<w<=156:assert 18-p-q-r+h-1<=13
    # Path of exactly two nonempty pair intersections.
    for p,q in product(range(7),repeat=2):
        w=192-2*((1<<p)+(1<<q))
        if 0<w<=156:assert 18-p-q<=13
    # One edge: intersection must have dimension at least5.
    for p in range(7):
        w=192-2*(1<<p)
        if 0<w<=156:assert p>=5
    # Exact Parseval check: if every even hyperplane section is >=158,
    # every nontrivial Fourier coefficient has absolute value <=w-316.
    # Parseval contradicts this already at N=2^14 and ever more for larger N.
    for w in [322,326,330,334]:
        t=w-316;N=1<<14
        assert w-t*t>0
        assert N*w-w*w>(N-1)*t*t
    print('All triple-six-flat span<=13 arithmetic cases checked through156.')
    print('Explicit158 word has support affine span14; cutoff158 would be false.')

if __name__=='__main__':verify()
