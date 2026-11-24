from itertools import product
from pathlib import Path

def red(w):
    out=[]
    for a in w:
        if out and out[-1]==-a: out.pop()
        else: out.append(a)
    return tuple(out)
def inv(w): return tuple(-a for a in w[::-1])
def mul(*ws): return red(sum((tuple(w) for w in ws),()))
def apply(f,w): return mul(*(f[a-1] if a>0 else inv(f[-a-1]) for a in w))
def comp(f,g): return tuple(apply(f,w) for w in g)
def power(f,k):
    assert k>=0
    out=((1,),(2,))
    for _ in range(k): out=comp(out,f)
    return out
I=((1,),(2,)); S=((2,),(-1,)); T=((1,),(1,2)); R=((1,),(-2,))
Si=power(S,3); Ti=((1,),(-1,2))
rels={'S^4':power(S,4),'(ST)^3 S^-2':comp(power(comp(S,T),3),power(S,2)), 'R^2':power(R,2),'RSRS':comp(comp(comp(R,S),R),S),'RTRT':comp(comp(comp(R,T),R),T)}
for name,f in rels.items():
    witness=None
    for l in range(9):
        for w in product((1,-1,2,-2),repeat=l):
            if red(w)!=w:continue
            if all(mul(w,(i,),inv(w))==f[i-1] for i in (1,2)):
                witness=w;break
        if witness is not None:break
    assert witness is not None,(name,f)
    print(name, f, 'inner witness',witness)
