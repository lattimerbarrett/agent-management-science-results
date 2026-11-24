"""Exact joint forced Schur-complement base-shift invariance."""
import sympy as s
a,b,c,r,t,w,z,B=s.symbols('a b c r t w z B')
A=s.Matrix([[a,b],[b,c]])
R=s.Matrix([r,t]);W=s.Matrix([w,z])
Rp=R+A*W
Bp=B+(R.T*W)[0]+(W.T*A*W)[0]/2
orig=B-(R.T*A.inv()*R)[0]/2
changed=Bp-(Rp.T*A.inv()*Rp)[0]/2
assert s.factor(orig-changed)==0
# This is joint in R=e-f: forcing term -f.W is automatically retained.
e1,e2,f1,f2=s.symbols('e1 e2 f1 f2')
assert s.expand(((s.Matrix([e1,e2])-s.Matrix([f1,f2])).T*W)[0]-(e1*w+e2*z-f1*w-f2*z))==0
print('Exact forced Schur base-shift identity checked for general invertible symmetric 2x2 form.')
