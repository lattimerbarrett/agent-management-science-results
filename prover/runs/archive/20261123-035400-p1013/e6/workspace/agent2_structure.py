"""Elementary lower-threshold structural constants, proved in Slack #30/#40.
No claim of a full stability theorem: these bounds assume complete cross-edges.
"""
from fractions import Fraction

def t(n,r):
    q,s=divmod(n,r)
    return (n*n-(r-s)*q*q-s*(q+1)*(q+1))//2

def parameters(h,r,a):
    a=Fraction(a)
    assert h>=1 and r>=2 and 0<=a<Fraction(1,r)
    k=2
    while Fraction(k-1,k*r)<=a:k+=1
    tau_bound=k**(k-2)
    B=k*(h-1)*tau_bound
    delta=h-1
    big=B*(1+delta*(k-1))
    cyclic=(h-1)*sum(j*2**(j*(j-1)//2) for j in range(1,k))
    return dict(k=k,tree_type_bound=tau_bound,packing_vertices=B,
                large_component_vertices=big,cyclic_vertices=cyclic,
                exceptional_vertices=big+cyclic)

def check():
    checks=0
    for r in range(2,9):
        for den in range(2,12):
            for num in range(den):
                a=Fraction(num,den*r)
                p=parameters(7,r,a);k=p['k']
                assert Fraction(k-1,k*r)>a
                if k>2:assert Fraction(k-2,(k-1)*r)<=a
                # Exactly q copies of any k-vertex tree in one
                # equal Turan class add q(k-1) edges.
                for q in range(1,8):
                    n=r*k*q
                    E=t(n,r)+q*(k-1)
                    assert Fraction(E-t(n,r),n)==Fraction(k-1,k*r)
                    assert E>t(n,r)+a*n
                    checks+=1
    return checks

if __name__=='__main__':
    print('exact rational factor-density checks:',check())


def check_universal_surplus():
    checks=0
    for r in range(2,31):
        for n in range(1,1001):
            edges=t(n-1,r)+n-1
            assert edges-t(n,r)==(n+r-1)//r-1
            checks+=1
    return checks
