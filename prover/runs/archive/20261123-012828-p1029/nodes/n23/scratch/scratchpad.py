import sympy as s
x,n=s.symbols('x n', real=True, positive=True)
# For integers n>=2, f_n ramps on [1/2,1/2+1/n].
I=s.integrate(n*(x-s.Rational(1,2)),(x,s.Rational(1,2),s.Rational(1,2)+1/n)) + s.Rational(1,2)-1/n
L2err=s.integrate((1-n*(x-s.Rational(1,2)))**2,(x,s.Rational(1,2),s.Rational(1,2)+1/n))
print('Integral f_n =',s.simplify(I))
print('Squared L2 distance to indicator_(1/2,1] =',s.simplify(L2err))
print('Integral(f_(n+1)-f_n) =',s.factor(I.subs(n,n+1)-I))
