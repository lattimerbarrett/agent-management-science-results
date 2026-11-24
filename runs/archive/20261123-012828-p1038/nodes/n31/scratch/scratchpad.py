import sympy as s
T,x,y,p,q=s.symbols('T x y p q',real=True)
# m=2, a=b=1, lower axial point at the virtual cone apex.
# p=(R-r)/(d+sqrt(d^2+(R-r)^2));
# q=(R+r)/(d+sqrt(d^2+(R+r)^2)).  Then 0<p<q<1.
A=s.Poly((1+T)*(1-p*T)*(1+q*T)*(T+p)*(T+x),T)
B=s.Poly((1+T)*(T+p)*(T+q)*(T+p)*(T+y),T)
D=[]
for residue in [0,1]:
 cols=[residue+2*j for j in range(3)]
 ax=[1,-2*p**2,p**4] if residue==0 else [1,-x**2-y**2,x**2*y**2]
 mat=s.Matrix([ax,[A.nth(j) for j in cols],[B.nth(j) for j in cols]])
 det=s.factor(mat.det());D.append(det)
 print('Residue',residue,'exact symbolic determinant:')
 print(det)
 # Search for an algebraic dependence at p=1/5,q=1/3.
 detnum=s.factor(det.subs({p:s.Rational(1,5),q:s.Rational(1,3)}))
 print('p=1/5,q=1/3:',detnum)
 # For physical upper points, x>1 and y>1. Test a positive-gap expansion.
 X,Y=s.symbols('X Y',nonnegative=True)
 shifted=s.Poly(s.expand(detnum.subs({x:1+X,y:1+Y})),X,Y)
 print('All coefficients positive after x=1+X,y=1+Y:',all(co>0 for co in shifted.coeffs()))
# The exact physical relation for r=2,R=7,d=12.
curve=2*(x*x-1)*y-7*(y*y-1)*x-24*x*y
print('physical coupling polynomial:',curve)
# At the virtual apex x=y=p the lower height is -24/5.
print('lower apex coupling check:',s.factor(curve.subs({x:s.Rational(1,5),y:s.Rational(1,5)})))
# Exact linear-dependence condition is det(block)=0; no numerical near-zero used.
