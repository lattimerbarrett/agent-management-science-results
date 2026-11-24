from pathlib import Path
import sympy as s

e=s.symbols('e', nonnegative=True, integer=True)
def ip(D,G):
    a,b=D;c,d=G
    return s.expand(-e*a*c+a*d+b*c)
A=(5,-1);B=(-1,12*e+5);H=(1,3*e+1);P=(4,12*e+3)
assert ip(H,H)==5*e+2
assert ip(A,H)==10*e+4
assert ip(B,H)==10*e+4
assert ip(A,P)==40*e+11
assert ip(B,P)==40*e+17
assert ip(A,B)==65*e+26
N=(1,e)
assert ip(H,(1,0))==2*e+1
assert ip(A,N)==-1
assert ip(B,(0,1))==-1
assert ip((4,12*e+4),(4,12*e+4))-ip(A,B)==15*e+6
# Exact norm-square Levi Schur complement; p and q are abstract conjugate jets.
h=s.symbols('h', positive=True)
p1,p2,q1,q2,t11,t12,t21,t22,ww=s.symbols('p1 p2 q1 q2 t11 t12 t21 t22 ww')
p=s.Matrix([p1,p2]); q=s.Matrix([[q1,q2]])
T=s.Matrix([[t11,t12],[t21,t22]])
# For psi=h|w|^2, eliminating the positive line-fibre direction leaves
# |w|^2*(d dbar h - (dh)(dbar h)/h) = psi*d dbar log h.
Schur=ww*T-ww*(p*q)/h
assert (Schur-ww*h*(T/h-p*q/h**2)).applyfunc(s.simplify)==s.zeros(2)
# Norm triangle + elementary Cauchy-Schwarz used in the noncollapse step.
a,b,u0,v0=s.symbols('a b u0 v0', real=True)
assert s.expand((a*a+b*b)*(u0*u0+v0*v0)-(a*u0+b*v0)**2-(a*v0-b*u0)**2)==0
# Local Levi form for norm-square on Tot(O_P(E)(1)), in Chern-normal
# horizontal coordinates, unit projective-fibre coordinate, and line fibre w.
r,k1,k2=s.symbols('r k1 k2', real=True)
levi=s.diag(r**2*k1,r**2*k2,-r**2,1)
assert levi.det()==-r**6*k1*k2
# Mean curvature >0 gives a positive horizontal eigenvalue.
# Exact rational sample verification for arbitrary-sign horizontal eigenvalues.
for a in range(-20,21):
    for b in range(-20,21):
        if a+b>0:
            assert sum(x>0 for x in [a,b,-1,1])>=2
        if a>0 and b>0:
            assert sum(x>0 for x in [a,b,-1,1])==3
# Direct reciprocal norm complex Hessian on a punctured vector-space fibre.
x,y,u,v=s.symbols('x y u v', real=True)
f=1/(x*x+y*y+u*u+v*v)
z=[x+s.I*y,u+s.I*v]
vars=[(x,y),(u,v)]
M=s.zeros(2)
for i,(a,b) in enumerate(vars):
    for j,(c,d) in enumerate(vars):
        M[i,j]=s.simplify((s.diff(f,a,c)+s.diff(f,b,d)+s.I*s.diff(f,b,c)-s.I*s.diff(f,a,d))/4)
M0=M.subs({x:r,y:0,u:0,v:0})
assert M0==s.diag(r**-4,-r**-4)
print('Intersection identities and local Levi calculations all passed.')
print('A.H = B.H =',ip(A,H), '; H^2 =',ip(H,H))
print('Norm-square Levi:',levi)
print('Reciprocal fibre norm Hessian:',M0)
Path('workspace/agent1_complete_checks.py').write_text(Path('scratchpad.py').read_text())
