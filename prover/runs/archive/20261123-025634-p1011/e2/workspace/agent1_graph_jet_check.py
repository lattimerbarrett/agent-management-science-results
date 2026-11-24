import sympy as s
from pathlib import Path
ys=s.symbols('y0:20'); lam,z,b,tau,mu=s.symbols('lam z b tau mu',real=True)
r2=sum(y*y for y in ys)
P=sum(y*y for y in ys[:10])-sum(y*y for y in ys[10:])
f=tau*mu*P*(lam**4+z*lam**2*r2+b*r2*r2)
origin={y:0 for y in ys}
assert all(s.diff(f,y).subs(origin)==0 for y in ys)
H=s.hessian(f,ys).subs(origin)
A=s.diag(*([1]*10+[-1]*10))
assert H==2*tau*mu*lam**4*A
assert s.trace(H)==0
assert A*A==s.eye(20)
print('Exact dimension21 graph jet checks: gradient0, tracefree Hessian=2 tau mu lambda^4 A, A^2=I.')
