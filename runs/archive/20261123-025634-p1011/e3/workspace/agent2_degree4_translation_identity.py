import sympy as s
d,b,x,q00,q01,q11=s.symbols('d b x q00 q01 q11',positive=True)
q1=s.Rational(2)/d*(q01+q00)
q3=d/2*q01-(d+4)/2*q00
Cfull=4*b*(d+2)/2*((d+4)/(d+2))**2*q1+4*(1/(d+4)+2*d*b/((d+4)*(d+2)))*q3
H=x*(-(2+8*b)*q00+x*((2+8*b)*q01+Cfull))
A=2+8*b;C=-2+32*b/d
claim=x*x*(-A*(2*q01-3*q11*x)+C*(q00+4*q01/(d+4)))
assert s.simplify(H-claim+x*(2+8*b)*(q00-4*q01*x+3*q11*x*x))==0
print('Exact translation-Hessian reduction identity verified')
