import sympy as S
# Check scalar dual-mean difference formula symbolically using abstract weighted samples.
l=S.symbols('l0:4');w=S.symbols('w0:4',positive=True);a,b=S.symbols('a b')
# Assume a = E_w lambda, so sum w(l-a)=0. For q'' ~ q ((l-a)/(l-b))²,
# numerator of theta''-b is sum w (l-a)²/(l-b).
# divide identity (l-a)^2/(l-b)=(l-a)+(b-a)*(l-a)/(l-b).
for z in l: assert S.cancel((z-a)**2/(z-b)-(z-a)-(b-a)*(z-a)/(z-b))==0
print('s2 dual mean recurrence rational identity verified')
# Check cofactor normalized p map n=4 for numerical rational example exactly.
x=list(map(S.Rational,[-3,-1,1,3]));p=list(map(S.Rational,[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]));d=[S.prod(a-b for b in x if b!=a) for a in x]
def F(p):
 M=S.Matrix([[sum(p[k]*x[k]**(i+j) for k in range(4)) for j in range(2)] for i in range(2)])
 c=M.inv()*S.Matrix([-sum(p[k]*x[k]**(i+2) for k in range(4)) for i in range(2)])
 f=[a*a+c[1]*a+c[0] for a in x];o=[p[i]*f[i]**2 for i in range(4)];return [S.factor(z/sum(o)) for z in o]
u=[1/(d[i]**2*p[i]) for i in range(4)];theta=sum(u[i]*x[i] for i in range(4))/sum(u)
o=[(x[i]-theta)**2/(d[i]**2*p[i]) for i in range(4)];o=[S.factor(z/sum(o)) for z in o]
assert o==F(p)
print('n4 reciprocal mean update checked exactly:',o)
