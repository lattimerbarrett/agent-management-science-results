import sympy as S
k,a,r,d,X,Y,u=S.symbols('k a r d X Y u',positive=True);s=1-r;K=k-1;A=1-(k-2)*d;lam=K*d
c1=(2*(X+Y)-u*u/r-(X*X/s+(Y-u)**2/r)/K)/k;c2=(2*(X+Y)+k*K*a-X*X/s-Y*Y/r)/k
F0=K*a*(1-K*d)+1/(k*A);B=k-K*K*d;corr=d/(k*A)*(2*u-B*u*u/r)
err=A/k*((X-s/A)**2/s+(Y-(r+d*u)/A)**2/r)
assert S.factor(lam*c1+(1-lam)*c2-F0-corr+err)==0
assert 16*10**6>3*2309**2 and 9*10**6<2*2122**2
assert S.Rational(187,1000)>S.Rational(31,200)+S.Rational(1061,1000)*S.Rational(31,100)**3
x,z=S.symbols('x z',positive=True)
g=2*z*(1+x)/S.sqrt(1+2*x)-z*z*(1+x)
assert S.simplify(S.diff(g,x,2)-2*z*(1-x)/(1+2*x)**S.Rational(5,2))==0
assert S.Rational(1,2)-9*S.Rational(1,4)/(4*S.sqrt(2))>0
assert S.Rational(28,1000)-S.Rational(531,1000)*S.Rational(3,10)**3>0
print('Mixed k>=4 complete-square, convexity, and exact radical bounds checked.')
