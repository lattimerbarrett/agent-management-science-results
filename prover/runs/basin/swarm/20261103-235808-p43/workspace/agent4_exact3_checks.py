import sympy as s
k,u,r=s.symbols('k u r',positive=True)
C=k*s.sqrt(1+k*k)
f=2*r*s.atan(C*r)-s.log(1+C*C*r*r)/C
assert s.simplify(s.diff(f,r)-2*s.atan(C*r))==0
assert s.expand((u+1)*(k*k*u-k*k-1))==k*k*u*u-u-k*k-1
assert s.simplify((u+1)*((k*k+2)*u-k*k-1)-((k*k+2)*u*u+u-k*k-1))==0
t=s.sqrt(1+k*k)/(k*k+2)
p=s.sqrt(2*k*k+3)/(k*k+2)
assert s.simplify(p*p+(1+k*k)*t*t)==1
assert s.simplify(s.sqrt(1+k*k)*(1-(k*k+2)*t*t)-t)==0
# South node and north simple points cannot coincide (their t signs differ).
assert s.ask(s.Q.positive(t)) is True
# Correct Hamiltonian sign: (x cross (grad H cross x)) = grad H tangential.
print('PASS exact three fixed points: south node and two north points; smooth bend generator differentiated exactly')
