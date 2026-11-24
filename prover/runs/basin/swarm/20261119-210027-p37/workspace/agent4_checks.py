"""Independent finite checks for ordered symmetric chain bound and d=9 family count."""
from math import comb
from itertools import combinations

def ordered_scd(n):
    chains=[[0]]
    for j in range(n):
        bit=1<<j
        out=[]
        for C in chains:
            if len(C)>1:
                out.append([x|bit for x in C[:-1]])
            out.append(C+[C[-1]|bit])
        chains=out
    return chains

def check_scd(n):
    chains=ordered_scd(n)
    assert len(chains)==comb(n,n//2)
    flat=[x for C in chains for x in C]
    assert len(flat)==len(set(flat))==1<<n
    earlier=set()
    for C in chains:
        assert C[0].bit_count()+C[-1].bit_count()==n
        assert all(a&b==a and b.bit_count()==a.bit_count()+1 for a,b in zip(C,C[1:]))
        for a,b in zip(C,C[2:]):
            assert any(a&y==a and y&b==y and y not in (a,b) for y in earlier)
        earlier.update(C)
    return True

def d9_star_count():
    good=[sum(1<<i for i in A) for A in combinations(range(9),4)
          if all(0<len(set(A)&set(range(3*j,3*j+3)))<3 for j in range(3))]
    assert len(good)==81
    total=0
    for T in range(1,1<<9):
        count=sum((A&T)==T for A in good)
        total+=(-1 if T.bit_count()%2==0 else 1)*(1<<count)
    assert total==618474403306
    assert total>229809982112+1
    return total

if __name__=='__main__':
    for n in range(13):
        assert check_scd(n)
    print('Ordered SCD and skip property verified for n=0..12')
    print('d9 intersecting-star-subfamily count =',d9_star_count())


def odd_star_size(d):
    """Largest star among middle-level sets rainbow on balanced 3 blocks."""
    from itertools import product
    from math import prod
    assert d%2==1 and d>=9
    q,r=divmod(d,3)
    bs=[q+(i<r) for i in range(3)]
    m=d//2
    return max(sum(prod(comb(b-(i==g),k-(i==g))
                        for i,(b,k) in enumerate(zip(bs,ks)))
                   for ks in product(*[range(1,b) for b in bs])
                   if sum(ks)==m) for g in range(3))

def check_odd_bounds(D7=2414682040998):
    from fractions import Fraction
    # lambda(d-1)<=D(d-2); D(j+1)<=D(j)^2/2+D(j)/2<=D(j)^2.
    # D7 exact needs its independent separate certificate.
    assert odd_star_size(11)==164
    assert odd_star_size(13)==690
    assert (D7*(D7+1)//2)*((D7*(D7+1)//2)+1)//2 < 2**164
    assert D7**16 < 2**690
    for d in (15,17,19):
        L=odd_star_size(d)
        W=comb(d-2,(d-2)//2)
        assert 2**L > 3**W
    # d>=21, m>=10, min block size>=7. Union-bound constant >5/3>log2(3).
    lower=Fraction(20,11)*(1-Fraction(1,64)-4*Fraction(11,20)**7)
    assert lower>Fraction(5,3)
    assert 2**5>3**3
    return lower
