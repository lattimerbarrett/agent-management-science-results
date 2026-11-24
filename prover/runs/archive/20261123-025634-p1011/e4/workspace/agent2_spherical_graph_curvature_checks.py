"""Symbolic audit of graph mean curvature on the round hemisphere.
The graph is latitude s=t*h over the equator, outward normal toward decreasing s.
No nonlinear gluing or dimension threshold is asserted here.
"""
import sympy as S
n,t,h,A,C,lap=S.symbols('n t h A C lap', real=True)
# A=|grad h|^2, C=Hess h(grad h,grad h).
ss=t*h
sec2=1/S.cos(ss)**2
W=S.sqrt(1+t*t*A*sec2)
H=(n-1)*S.tan(ss)/W+t*sec2*lap/W+t*t*A*sec2*S.tan(ss)/W**3-t**3*sec2**2*C/W**3
D=(n-1)*h+lap
cubic=(n-1)*(h**3/S.Integer(3)-h*A/2)+lap*(h*h-A/2)+A*h-C
assert S.simplify(S.expand(S.series(H,t,0,5).removeO())-t*D-t**3*cubic)==0
assert S.simplify(H.subs(t,-t)+H)==0
# Spherical dimension n-1 measure at stereographic infinity is ~r^{-n}dr.
# Hess h grows at most r^8, and boundary Sobolev-dual exponent is p=2(n-1)/n.
p=2*(n-1)/n
assert S.simplify((8*p-n+1)/p-(8-n/2))==0
# Thus integrability of Hess h in L^p requires 8-n/2<0, i.e. n>16.
print('PASS: exact graph curvature is odd; linear term (Delta+n-1)h; cubic coefficient checked')
print('PASS: symbolic dual-norm tail exponent =',S.factor((8*p-n+1)/p))
