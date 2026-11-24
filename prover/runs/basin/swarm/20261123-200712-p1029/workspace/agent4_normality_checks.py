"""Exact free-*algebra checks for the projection-normality lemma.
Relations are p^2=p, e^2=e, pe=ep=e (e <= p), q=1-p+e.
No floating point or assumptions on x are used.
"""
from fractions import Fraction

def reduce_word(w):
    # Every maximal p/e block is p if all letters p, e otherwise.
    out=[]; i=0
    while i<len(w):
        if w[i] not in ('p','e'):
            out.append(w[i]); i+=1; continue
        j=i
        while j<len(w) and w[j] in ('p','e'): j+=1
        out.append('e' if 'e' in w[i:j] else 'p'); i=j
    return tuple(out)

def add(*terms):
    ans={}
    for a in terms:
        for w,c in a.items():
            w=reduce_word(w); ans[w]=ans.get(w,Fraction())+c
    return {w:c for w,c in ans.items() if c}

def scale(c,a): return {w:c*v for w,v in a.items() if c*v}
def mul(a,b):
    ans={}
    for u,c in a.items():
        for v,d in b.items():
            w=reduce_word(u+v); ans[w]=ans.get(w,Fraction())+c*d
    return {w:c for w,c in ans.items() if c}

def verify():
    I={():Fraction(1)}
    p={('p',):Fraction(1)}; e={('e',):Fraction(1)}; x={('x',):Fraction(1)}
    q=add(I,scale(-1,p),e)
    assert mul(q,q)==q
    assert mul(mul(q,p),q)==e
    assert mul(mul(q,e),q)==e
    lhs=mul(mul(q,add(x,scale(-1,p))),q)
    rhs=mul(mul(q,add(x,scale(-1,e))),q)
    assert lhs==rhs
    assert add(I,scale(-1,q))==add(p,scale(-1,e))
    return 5

if __name__=='__main__':
    print(f'{verify()} exact noncommutative identities verified')
