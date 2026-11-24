import sympy as S
x,t,z=S.symbols('x t z');a,b,c=S.symbols('a b c');f0,f1,f2,g0,g1,g2=S.symbols('f0 f1 f2 g0 g1 g2')
f=x**3+f2*x**2+f1*x+f0;g=x**3+g2*x**2+g1*x+g0;q=a*x*x+b*x+c
ft=f.subs(x,t);gt=g.subs(x,t);qt=q.subs(x,t)
Fdiff=S.div(f-ft,x-t,x)[0];Gdiff=S.div(g-gt,x-t,x)[0];Qdiff=S.div(q-qt,x-t,x)[0]
rhs=-Qdiff+qt/2*(Fdiff/ft+Gdiff/gt)
assert S.cancel(rhs.subs(x,t)+S.diff(q,x).subs(x,t)-qt/2*(S.diff(ft,t)/ft+S.diff(gt,t)/gt))==0
assert S.cancel(rhs.subs(x,z)/(z-t)+q.subs(x,z)/(z-t)**2-qt/(2*(z-t)**2)*(f.subs(x,z)/ft+g.subs(x,z)/gt))==0
assert S.cancel(S.expand(rhs).coeff(x,2)-qt/2*(1/ft+1/gt))==0
assert S.cancel(S.expand(rhs).coeff(x,1)+a+t*S.expand(rhs).coeff(x,2)-qt/2*((f2+2*t)/ft+(g2+2*t)/gt))==0
print('PASS generic-cubic exact intrinsicquadraticconnection, kineticintegral, probeCauchyidentity, canonicaltwomomentcoordinates')
