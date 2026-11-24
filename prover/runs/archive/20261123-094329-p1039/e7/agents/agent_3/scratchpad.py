import sympy as s
c,x,f,g=s.symbols('c x f g',real=True)
r=c+2
Ar=2*r*(c*c+x*x)+2*f*(r-1)-g*x
D=2*(c*c+x*x+s.Rational(1,4))+f
Detr=s.expand(Ar*D-r*((4*c*x-g)**2+x*x))
red=s.rem(s.Poly(Detr,x),s.Poly(x*x-(1+f-c*c),x)).as_expr()
print(s.collect(s.expand(red),[g,f]))
print('g polynomial:',s.Poly(red,g))
print('f polynomial:',s.Poly(red,f))
print('rational eigenvalue gap=',s.Rational(123,1160)-s.Rational(3,64))
