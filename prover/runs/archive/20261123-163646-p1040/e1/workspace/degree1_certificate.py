"""Exact degree-one Johnson-map check for Magnus generators.
No theorem about degrees >=2 is asserted by this computation.
"""
from itertools import combinations

def multiply(a,b,degree=2):
    c={}
    for u,x in a.items():
        for v,y in b.items():
            if len(u)+len(v)<=degree:
                w=u+v;c[w]=c.get(w,0)+x*y
    return {w:x for w,x in c.items() if x}

def expansion(word):
    out={():1}
    for s in word:
        i=abs(s)-1
        factor={():1,(i,):1} if s>0 else {():1,(i,):-1,(i,i):1}
        out=multiply(out,factor)
    return out

def generators(n):
    # Return (name, changed index, image word) with indices 0-based.
    for i in range(n):
        for j in range(n):
            if i!=j:
                yield ('K',i,j),i,(j+1,i+1,-j-1)
        for j,k in combinations([j for j in range(n) if j!=i],2):
            yield ('C',i,j,k),i,(i+1,j+1,k+1,-j-1,-k-1)

def check(n):
    basis={(i,j,k) for i in range(n) for j,k in combinations(range(n),2)}
    images=[]
    for name,i,word in generators(n):
        d=expansion(word+(-i-1,));d[()]-=1
        d={u:x for u,x in d.items() if x}
        assert d and all(len(u)==2 for u in d)
        nonzero=[]
        for j,k in combinations(range(n),2):
            a=d.get((j,k),0)
            assert d.get((k,j),0)==-a
            if a: nonzero.append(((i,j,k),a))
        assert len(nonzero)==1
        key,sgn=nonzero[0]
        assert sgn in (-1,1)
        assert d=={(key[1],key[2]):sgn,(key[2],key[1]):-sgn}
        images.append(key)
    assert len(images)==len(set(images))==len(basis)==n*n*(n-1)//2
    assert set(images)==basis
    return len(images)

if __name__=='__main__':
    for n in range(2,13):
        print(n,check(n),'signed-permutation columns checked')
