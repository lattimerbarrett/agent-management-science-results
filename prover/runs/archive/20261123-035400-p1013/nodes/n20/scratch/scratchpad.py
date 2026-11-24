from fractions import Fraction
import math
# Second-order comparison for a tree-component bulk on k vertices:
# star/path wedge difference plus the gain from an edge-neutral part shift.
for r in range(3,13):
    for k in range(2,100):
        d=Fraction(2*(k-1),k)
        wedges=Fraction((k-2)*(k-3),2*k)
        score=wedges/Fraction(r-1)+(d-1)/Fraction(r-2)
        if score>=1:
            print('r=',r,'first k with template score >= 1:',k,'slope=',Fraction(k-1,k*r),'score=',score)
            break
# Exact finite partial sums sufficient to show the H8 cycle separation.
z=Fraction(7,3)
A=sum(z**t/Fraction(math.factorial(t)**2) for t in range(20))
D=sum(z**(t+2)/Fraction(math.factorial(t)*math.factorial(t+2)) for t in range(20))
print('P3 bulk in bipartite host, balanced limit:',float(A))
print('one-vertex shift limit:',float(D))
print('difference:',float(D-A))
