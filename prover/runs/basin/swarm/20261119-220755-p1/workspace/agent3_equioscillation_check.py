import sympy as sp
xs=list(map(sp.Integer,[-3,-2,-1,1,2,3]));Vs=sp.Matrix([[1,x,x*x] for x in xs]);Ds=sp.diag(*[(x**3-7*x)/6 for x in xs]);Ms=Vs.T*Vs/6;u0,u1,u2=sp.symbols('u0 u1 u2');us=sp.Matrix([u0,u1,u2]);ls=Vs*us;es=(us.T*Ms*us)[0];Bs=Vs.T*Ds*ls.applyfunc(lambda x:x*x)/6
qs=(sp.ones(6,1)*es-ls.applyfunc(lambda x:x*x)+Ds*Vs*Ms.inv()*Bs)/3
mom=sp.Matrix([xs,[x*x for x in xs]])*qs
print('EXACT MOMENTS',list(map(sp.factor,mom)))
assert sp.factor(mom[0]+sp.Rational(800,147)*u1*(u0+7*u2))==0
assert sp.factor(mom[1]+sp.Rational(400,63)*(u1*u1+7*u2*u2+2*u0*u2))==0
