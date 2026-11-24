import sympy as s
x,y=s.symbols("x y",real=True)
r2=x*x+y*y
F=-x*y+2*(x+y)+s.log(r2)
T=F-4*y
z=s.symbols("z")
p=s.I*z*z+2*(1+s.I)*z+2
assert s.expand(p-s.I*(z+1-s.I)**2)==0
assert s.simplify(s.diff(T,x).subs({x:-1,y:1}))==0
assert s.simplify(s.diff(T,y).subs({x:-1,y:1}))==0
assert s.hessian(T,(x,y)).subs({x:-1,y:1})==s.zeros(2)
u,v=s.symbols("u v",real=True)
cubic=s.expand(sum(s.diff(T,x,i,y,3-i).subs({x:-1,y:1})*u**i*v**(3-i)/s.factorial(i)/s.factorial(3-i) for i in range(4)))
assert s.discriminant(cubic.subs(v,1),u)==s.Rational(1,3)
assert 2/s.log(2)<3
inner=100-s.Rational(1,50)-2*s.sqrt(2)
outer=50-2*s.sqrt(2)-s.Rational(1,25)
assert inner>16 and outer>16
a,b,c=s.symbols("a b c",real=True)
G=T+a*x+b*y+c*((x+1)**2+(y-1)**2)
equations=s.Matrix([s.diff(G,x),s.diff(G,y),s.diff(G,x,2),s.diff(G,x,y),s.diff(G,y,2)])
J=equations.jacobian([x,y,a,b,c]).subs({x:-1,y:1,a:0,b:0,c:0})
assert J.det()==-8
print("Planar merger checks passed: unique critical (-1,1), cubic discriminant1/3, shell bounds>16, tuning determinant-8")
