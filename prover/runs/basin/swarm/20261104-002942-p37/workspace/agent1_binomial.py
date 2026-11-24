from math import comb
from fractions import Fraction

def coefficients(groups, special=False):
    out=[1]
    for j,g in enumerate(groups):
        p=[0]+[comb(g-1,i-1) if special and j==0 else comb(g,i) for i in range(1,g)]+[0]
        q=[0]*(len(out)+g)
        for a,x in enumerate(out):
            for b,y in enumerate(p): q[a+b]+=x*y
        out=q
    return out

def exponent(d):
    groups=sorted([d//3+(i<d%3) for i in range(3)])
    if d%2==0: return coefficients(groups)[d//2]//2
    return coefficients(groups,True)[d//2]

def check():
    # finite cases of binomial lemma, and exact rational uniform estimates
    for d in [14,15,16,17,19]:
        assert 5*exponent(d)>8*comb(d-2,(d-2)//2)
    even=Fraction(17,9)*Fraction(29,32)
    odd=Fraction(20,11)*(1-Fraction(1,64)-2*(Fraction(11,20)**7+Fraction(1,128)))
    assert even>Fraction(8,5) and odd>Fraction(8,5)
    assert 2**8>3**5
    for d in range(14,501):
        assert 5*exponent(d)>8*comb(d-2,(d-2)//2)
    print('Binomial lemma: finite exceptions and uniform rational estimates verified; additional d14..500 sanity checks passed.')
    print('Uniform estimates:',even,odd)
    print('Small capacities:',[(d,exponent(d)) for d in range(9,14)])
if __name__=='__main__':check()
