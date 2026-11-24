"""Exact feasible certificates for the proposed projection Johnson LP.
These DO NOT exhibit Reed--Muller words. They prove this LP relaxation
cannot exclude the five projection weights under the stated constraints.
All Johnson dual-Hahn inequalities, not a truncated selection, are checked.
"""
from math import comb
from fractions import Fraction

def C(n,k):return comb(n,k) if 0<=k<=n else 0

def P(v,k,j,l):
    return sum((-1)**t*C(l,t)*C(k-l,j-t)*C(v-k-l,j-t) for t in range(min(l,j)+1))

CERTIFICATES={288:{32:1071,16:3024},296:{24:3410,8:685},304:{32:1662,16:2433},308:{36:791,20:3304},312:{24:3939,16:156}}

def verify():
    # Full small-scheme normalization checks of the eigenpolynomial formula.
    for v,k in ((8,3),(10,4)):
        for l in range(k+1):
            pp=[P(v,k,j,l) for j in range(k+1)]
            assert sum(pp)==(comb(v,k) if l==0 else 0)
            qs=[Fraction(pp[j],C(k,j)*C(v-k,j)) for j in range(k+1)]
            norm=sum(Fraction(C(k,j)*C(v-k,j))*qs[j]**2 for j in range(k+1))
            assert norm==Fraction(comb(v,k),C(v,l)-C(v,l-1))
    v=M=4096
    for k,profile in CERTIFICATES.items():
        assert all(a>=0 and isinstance(a,int) for a in profile.values())
        assert 1+sum(profile.values())==M
        assert k+sum(i*a for i,a in profile.items())==k*k
        assert all(i<=56 and i%4==0 for i in profile)
        assert all(k-i in {248,252,256,272,288,296,304,308,312,316} for i in profile)
        minimum=None
        for l in range(1,k+1):
            value=Fraction(1)
            for i,a in profile.items():
                j=k-i
                value+=a*Fraction(P(v,k,j,l),C(k,j)*C(v-k,j))
            assert value>=0,(k,l,value)
            if l>1:minimum=value if minimum is None else min(minimum,value)
        print('Exact feasible certificate: projection weight',k,'profile',profile)
    print('ALL Johnson inequalities and exact first moments verified.')
if __name__=='__main__':verify()
