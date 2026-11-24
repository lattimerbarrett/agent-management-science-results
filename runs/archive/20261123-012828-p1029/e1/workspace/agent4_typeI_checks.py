import sympy as s
from fractions import Fraction
N=12
x=s.symbols("x0:"+str(N+1))
for n in range(1,N+1):
    assert s.expand(sum(x[i+1]-x[i] for i in range(n))-(x[n]-x[0]))==0
for den in range(1,101):
    for num in range(1,den+1):
        eta=Fraction(num,den)
        n=eta.denominator//eta.numerator+1
        assert n*eta>1
print("Exact trace-case telescoping and 5050 rational witnesses checked")
