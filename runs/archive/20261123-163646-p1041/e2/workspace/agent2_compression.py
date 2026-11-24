"""Checked quotient-compression identities for binary Reed--Muller words.
No assertion about the unresolved requested nonexistence is made here.
"""
import random

def degree(table):
    a=list(table); n=(len(a)-1).bit_length()
    for i in range(n):
        for x in range(1<<n):
            if x>>i&1:a[x]^=a[x^(1<<i)]
    return max((x.bit_count() for x,c in enumerate(a) if c),default=-1)

def quotient(table,v):
    n=(len(table)-1).bit_length(); p=v.bit_length()-1
    assert 0<v<1<<n
    out=[]
    for z in range(1<<(n-1)):
        x=(z&((1<<p)-1))|((z>>p)<<(p+1))
        out.append(table[x]^table[x^v])
    return out

def check(table,r):
    n=(len(table)-1).bit_length(); S={i for i,c in enumerate(table) if c}; w=len(S)
    assert degree(table)<=r
    ks=[]
    for v in range(1,1<<n):
        k=sum((x^v) in S for x in S)//2;ks.append(k)
        q=quotient(table,v)
        assert sum(q)==w-2*k
        assert degree(q)<=r-1
        if k==0:assert sum(q)==w
    assert sum(ks)==w*(w-1)//2
    if w*(w-1)//2<(1<<n)-1:assert 0 in ks

def run():
    count=0
    for n in range(1,5):
        for r in range(n):
            mons=[s for s in range(1<<n) if s.bit_count()<=r]
            for coeff in range(1<<len(mons)):
                table=[sum(bool(coeff>>i&1) and (x&s)==s for i,s in enumerate(mons))%2 for x in range(1<<n)]
                check(table,r);count+=1
    rng=random.Random(2026)
    for n in range(5,9):
        for r in range(1,n):
            mons=[s for s in range(1<<n) if s.bit_count()<=r]
            for _ in range(10):
                chosen=rng.sample(mons,min(12,len(mons)))
                table=[sum((x&s)==s for s in chosen)%2 for x in range(1<<n)]
                check(table,r);count+=1
    assert 256*255//2<2**15-1
    assert 362*361//2<2**16-1
    assert 334*333//2<2**16-1
    print('quotient identities and compression bound verified on',count,'words')

if __name__=='__main__':run()
