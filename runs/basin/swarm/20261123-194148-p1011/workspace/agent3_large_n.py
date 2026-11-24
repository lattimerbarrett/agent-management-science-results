import sympy as s
from fractions import Fraction as F
j=s.symbols("j")
p=s.Poly((j+3)**8*(j+1001)**2*(2*j+1002)-(j+5)**10*(2*j+1006),j)
assert all(c>=0 for c in p.all_coeffs())
w=[F(1),F(3,1000)]
for k in range(100):
    w.append(w[k]*F((k+3)**2,(k+1001)**2)*F(2*k+1006,2*k+1002))
M0=sum(w)
M2=sum(w[k]*(2*k+1+F(2*(k+1)*(k+2),999))**2 for k in range(len(w)))
t0=sum(w[J]*F(J+3,18) for J in (100,101))
t2=sum(F(8,5)*w[J]*(J+3)**5 for J in (100,101))
assert (M0+t0)*(M2+t2)<F(4,3)
print("Exact rational upper bound:",float((M0+t0)*(M2+t2)))
print("Therefore correlation squared >",float(1/((M0+t0)*(M2+t2))))
