import os
for root, dirs, files in os.walk('experiments/e1'):
    for name in files:
        if name.endswith(('.md','.txt','.py')): print(os.path.join(root,name))
import sympy as s
x,y,p,r,a=s.symbols('x y p r a', real=True)
z=s.Matrix([x,y,p,r]); V=x**3/3-x*y**2-a*x
P=p-s.diff(V,x); R=r-s.diff(V,y)
F=s.Matrix([x+P,y-R,P,R]); J=F.jacobian(z)
O=s.zeros(4); O[:2,2:]=s.eye(2); O[2:,:2]=-s.eye(2)
print('Return map:',list(F))
print('Symplectic defect:',s.simplify(J.T*O*J-O))
print('Fixed equations reduced: p=r=0, x^2-y^2=a, 2xy=0')
print('det(D F-I) at p=r=0:',s.factor((J-s.eye(4)).det()))
print('At a=0 the unique fixed point is origin; at a>0 exactly two real fixed points (plus/minus sqrt(a),0,0,0).')
print('Jacobian at origin for a=0:',J.subs({x:0,y:0,p:0,r:0,a:0}))