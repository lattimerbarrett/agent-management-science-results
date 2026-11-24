"""Exact exterior computation supporting a conditional slice obstruction.
Lemma: On V=F2^12, let beta be decomposable6 and gamma be a moment6
form of a weight112 RM(6,12) word. If q(beta+gamma)=1, then its
apolar length is>=162. (Uses classical KTA112 normalforms.)

TypeII gamma=p+q with6-spaces intersectingdimension3. q(beta+gamma)=1
means beta complements exactly one ofp,q. Normalize beta,p to complementary
coordinate6-spaces. The third q orbit has intersectiondimensions(k,3),
k=1,2,3; these are exactly the first three computed cases below.

TypeI gamma hasessentialspaceM8 and is Hodge-dual there to an alternating
2-form ofrank6. Pairing beta with gamma nontrivially forces beta to
projectsurjectivelyontotheoutside4-space and P=beta∩M to be a nondegenerate
2-plane for that alternatingform. Shearsremove the outsidegraph and
isometrytransitivity sendsP to<e0,e1>; this gives the finalcanonicalcase.

Thus beta+gamma cannotbe the sixth momentform of a null5 set of
weight<=158, since apolarlength<=supportweight by the blocktriangular
momentmatrix argument.
"""
from itertools import combinations

def rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def wedge(form,vector):
    out=set()
    for mask in form:
        for i in range(12):
            if vector>>i&1 and not(mask>>i&1):
                j=mask|(1<<i)
                if j in out:out.remove(j)
                else:out.add(j)
    return out

def hilbert(form):
    h=[]
    for k in range(7):
        indices={sum(1<<i for i in a):j for j,a in enumerate(combinations(range(12),6-k))}
        rows=[]
        for a in combinations(range(12),k):
            s=sum(1<<i for i in a);r=0
            for t in form:
                if s&t==s:r^=1<<indices[t^s]
            rows.append(r)
        h.append(rank(rows))
    return h

def verify():
    alpha={0x3f,0xfc0}
    observed=[]
    for a in (1,2,3):
        b=3;c=3-a
        vectors=[1<<i for i in range(a)]+[1<<(6+i) for i in range(b)]
        vectors +=[(1<<(a+i))^(1<<(6+b+i)) for i in range(c)]
        third={0}
        for v in vectors:third=wedge(third,v)
        h=hilbert(alpha^third)
        observed.append(sum(h))
        assert sum(h)>158
    assert observed==[168,166,162]
    gamma={sum(1<<i for i in a) for a in ((2,3,4,5,6,7),(0,1,4,5,6,7),(0,1,2,3,6,7))}
    beta={sum(1<<i for i in (0,1,8,9,10,11))}
    h=hilbert(gamma^beta)
    assert h==[1,12,42,60,42,12,1]
    assert sum(h)==170
    print('Conditional64+112 topform obstruction verified: lengths',observed+[170])

if __name__=='__main__':verify()
