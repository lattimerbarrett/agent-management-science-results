"""Exact mod2 involutory Magnus leading-term checks for rank3 witnesses.
Letters 0,1,2 are a,b,c; ring has a^2=b^2=c^2=0.
This verifies the algebraic detector; Fox-map proof is separate.
"""
def add(x,y):return x^y

def mul(x,y):
    z=set()
    for u in x:
        for v in y:
            if u and v and u[-1]==v[0]:continue
            w=u+v
            if w in z:z.remove(w)
            else:z.add(w)
    return z

def lie(x,y):return add(mul(x,y),mul(y,x))

def alternating(m,start):return tuple(start+(i%2) if start==1 else start-(i%2) for i in range(m))

if __name__=='__main__':
    a={(0,)};b={(1,)};c={(2,)};s=b^c
    u=a^b;v=a^c
    P=lie(lie(v,u),a)
    assert P=={(2,1,0),(1,2,0),(0,2,1),(0,1,2)}
    assert P==lie(lie(a,s),s)
    for degree in range(3,257):
        assert P
        # Unique endpoint monomial in ad_s^(degree-1)(a).
        word=(0,)+tuple(1+i%2 for i in range(degree-1))
        assert word in P
        expected=4*(2**((degree-1).bit_count()))-4
        assert len(P)==expected,(degree,len(P),expected)
        if degree<=12:print('degree',degree,'nonzero_terms',len(P))
        P=lie(P,s)
    print('ALL RANK3 PROPAGATION CHECKS THROUGH DEGREE256 PASSED')
