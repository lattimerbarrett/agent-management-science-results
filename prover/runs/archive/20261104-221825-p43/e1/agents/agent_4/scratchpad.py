import sympy as s
from pathlib import Path
# basis a1,a2,b1,b2; algebraic intersection a_i . b_j=delta_ij
I=s.eye(2); Z=s.zeros(2); J=Z.row_join(I).col_join((-I).row_join(Z))
a=s.eye(4)[:,:2]; b=s.eye(4)[:,2:]
def twist(v):
    # x -> x + (x.J.v) v, column convention
    return s.eye(4)+v*(J*v).T
v1=b[:,0];v2=b[:,1];v12=v1+v2
T1=twist(v1);T2=twist(v2);T12=twist(v12)
phi=T12*T1.inv()*T2.inv()
g=phi*a
assert phi.T*J*phi==J
assert g.T*J*g==s.zeros(2)
assert g==s.Matrix([[1,0],[0,1],[0,1],[1,0]])
for name,x,y in [('alpha-beta',a,b),('alpha-gamma',a,g),('beta-gamma',b,g)]:
    pairing=x.T*J*y
    assert abs(pairing.det())==1
    print(name, 'intersection=', pairing.tolist(), 'det=',pairing.det())
Q=s.Matrix([[0,1],[1,0]])
assert Q.det()==-1
assert Q.eigenvals()=={-1:1,1:1}
assert (Q.inv()==Q)
print('phi=',phi.tolist())
print('gamma=',g.tolist())
print('Hopf intersection form=',Q.tolist(),'signature=0, even=True, rank=2')
# Check local index-two germ f=x^3-3xy^2+u^2-v^2 deformation.
x,y,u,v,c=s.symbols('x y u v c',real=True)
f=x**3-3*x*y*y+u*u-v*v-3*c*c*x
grad=s.Matrix([s.diff(f,z) for z in (x,y,u,v)])
H=s.hessian(f,(x,y,u,v))
for sign in [-1,1]:
    p={x:sign*c,y:0,u:0,v:0}
    assert grad.subs(p)==s.zeros(4,1)
    assert s.factor(H.subs(p).det())==144*c*c
print('Local cubic splitting: two criticals (+c,0,0,0),(-c,0,0,0); Hessian determinant 144*c^2 each.')
# Generic capsule dilation identity for h=A(u)*v+s*t.
z, vv, ss, tt=s.symbols('z vv ss tt',real=True)
AA=s.Function('A')(z); aa=s.Function('a')(z)
bb=1-aa*s.diff(AA,z)/AA
hh=AA*vv+ss*tt
YY=[aa,bb*vv,ss/2,tt/2]
assert s.simplify(sum(YY[i]*s.diff(hh,q) for i,q in enumerate([z,vv,ss,tt]))-hh)==0
print('Global capsule symbolic identity Y(h)=h verified.')
Path('workspace/agent4_trisection_checks.py').write_text(Path('scratchpad.py').read_text())
