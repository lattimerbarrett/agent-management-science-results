import sympy as s
from fractions import Fraction
for r in range(1,9):
    t=s.symbols("t0:"+str(r))
    p=s.prod(1-z for z in t)
    w=[t[j]*s.prod(1-t[k] for k in range(j+1,r)) for j in range(r)]
    assert s.expand(p+sum(w)-1)==0
for den in range(2,60):
    for num in range(1,den):
        eta=Fraction(num,den)
        for gap in [eta,(1+eta)/2,Fraction(1)]:
            t=eta/gap
            assert eta<=t<=1 and t*gap==eta
            for r in range(1,10):
                assert (1-t)**r<=(1-eta)**r
print("Exact convex interpolation identities and geometric bounds verified")
