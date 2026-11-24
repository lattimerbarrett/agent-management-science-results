"""Finite checks used by agent2_slice128_special_proof.txt.
The text file is the proof; these are exact independent checks of all
small polynomial/convolution and numerical steps that are enumerated.
"""
from itertools import combinations

def degree(truth,n):
    a=list(truth)
    for i in range(n):
        for x in range(1<<n):
            if x>>i&1:a[x]^=a[x^(1<<i)]
    return max([x.bit_count() for x,v in enumerate(a) if v] or [-1])

def rank(rows):
    p={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k in p:x^=p[k]
            else:p[k]=x;break
    return len(p)

def verify():
    # All quadratic3-variable forms, convolution by q=x1x2+x3.
    mon=[0,1,2,4,3,5,6]
    q=[((x&1)*((x>>1)&1))^((x>>2)&1) for x in range(8)]
    for coef in range(128):
        b=[sum(((coef>>i)&1)*int((x&m)==m) for i,m in enumerate(mon))%2 for x in range(8)]
        conv=[sum(q[t]*b[x^t] for t in range(8))%2 for x in range(8)]
        b3=coef>>3&1;b12=coef>>4&1;b13=coef>>5&1;b23=coef>>6&1
        assert all(conv)==bool(b13==b23==0 and b3^b12==1)
    # Shortened degree<=d codes on the six-point rank4 quadric in4variables.
    Q=[x for x in range(16) if ((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1))]
    assert len(Q)==6
    for d,count in enumerate((1,1,2,32)):
        got=set()
        for sub in range(64):
            S=frozenset(x for i,x in enumerate(Q) if sub>>i&1)
            if degree([int(x in S) for x in range(16)],4)<=d:got.add(S)
        assert len(got)==count
        if d==3:
            expected={frozenset(x for x in Q if ((a&x).bit_count()%2)^c) for a in range(16) for c in range(2)}
            assert got==expected
    # The null4 code on5 variables is exactly the repetition code.
    rows=[]
    for k in range(5):
        for T in combinations(range(5),k):
            m=sum(1<<i for i in T)
            rows.append(sum(int((x&m)==m)<<x for x in range(32)))
    assert rank(rows)==31
    assert all(row.bit_count()%2==0 for row in rows)
    # Every weighted lower bound and final Diophantine check.
    for E in (66,70,74,78):
        assert E//2<48
        R=E-64
        assert R<=14 and R+2*(R//2)<32
        assert 2*32+2*16>E
        assert 6*16>E and 6*16+2*8>E
        assert 14*8>E and 14*8+2*4>E
        assert not any(30*a+32*b==E for a in range(4) for b in range(4))
    print('All exact finite checks for128-slice special lemma passed.')

if __name__=='__main__':verify()
