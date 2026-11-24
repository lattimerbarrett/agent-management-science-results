import sympy as S
from pathlib import Path
x=S.symbols('x');v=S.Matrix(S.symbols('v0:3'));nodes=list(map(S.Rational,[-8,-7,-4,-1,1,4,7,8]));p=x**4-65*x*x+424;tau=x**3-S.Rational(65,2)*x;pp=S.diff(p,x)
Is=[];Ts=[]
for sign in [1,-1]:
 rows=[];ws=[]
 for z in nodes:
  if p.subs(x,z)!=sign*360:continue
  row=S.Matrix([z**j/pp.subs(x,z) for j in range(3)]);w=tau.subs(x,z)/pp.subs(x,z);rows.append(row);ws.append(w)
 I=sum((row*row.T/w for row,w in zip(rows,ws)),S.zeros(3))
 T=-sum((row*(row.dot(v))**2/w**2 for row,w in zip(rows,ws)),S.zeros(3,1))
 Is.append(I);Ts.append(T)
Ip,Im=Is;Tp,Tm=Ts;Cp,Cm=Ip.inv(),Im.inv();d=S.Rational(1,2)
Sm=(1-d)*Ip+(1+d)*Im;N=(1-d)*Cp+(1+d)*Cm
ours=S.simplify(Sm.inv()*((1-d)*Tp+(1+d)*Tm+2*d*N.inv()*(Cp*Tp-Cm*Tm)))
H=Ip-Im;levi=S.simplify(H.inv()*(Tp-Tm)/2)
psi=S.Matrix(S.symbols('a0:3'));V=S.Matrix(S.symbols('b0:3'))
res=S.simplify(ours-levi-psi.dot(v)*v-(v.T*H*v)[0]*V)
eq=[]
for f in res:eq+=S.Poly(f,list(v)).coeffs()
sol=S.solve(eq,list(psi)+list(V));print('projectivenull solve',sol)
# Also check whether ours is LeviCivita of weighted metric plus/minus anyconstant combo.
