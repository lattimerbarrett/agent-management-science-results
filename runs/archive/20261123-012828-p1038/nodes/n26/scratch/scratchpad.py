import sympy as s
T=s.symbols('T')
a=s.symbols('a',integer=True,positive=True)
t=s.Rational(1,2)
G=(1-t*T)**2
GU=(1-3*T)*(1-s.Rational(4,3)*T)
# a lower axial heights confluent at -3/4; one upper height 4/3.
# For degree <= a+2 the lower-row quotient is represented by
# leading coefficient, evaluation at T=2, and derivative at T=2.
factor=(s.Rational(5,2))**a
U=T**a*GU
A=(1-t*T)*(T+t)**a*(T+3)
B=(T+t)**(a+1)*(T+s.Rational(4,3))
rows=[]
for p,lc in [(U,s.Integer(4)),(A,-t),(B,s.Integer(1))]:
 rows.append([lc,s.simplify(p.subs(T,2)),s.simplify(s.diff(p,T).subs(T,2))])
K=s.Matrix(rows)
print('Hermite quotient matrix:')
print(K)
print('determinant:',s.factor(K.det()))
print('determinant after positive scaling:',s.simplify(K.det()/factor**2))
for n in range(1,8):
 print('a =',n,'det =',s.factor(K.det().subs(a,n)))
# General confluent identity: divisibility by (1-t*T)^2 is equivalent
# to value and first derivative vanishing at T=1/t.
p0,p1,p2,p3,u=s.symbols('p0 p1 p2 p3 u',nonzero=True)
p=p0+p1*T+p2*T**2+p3*T**3
rem=s.rem(p,(1-u*T)**2,T)
interp=p.subs(T,1/u)+s.diff(p,T).subs(T,1/u)*(T-1/u)
print('Hermite remainder identity:',s.simplify(rem-interp)==0)
