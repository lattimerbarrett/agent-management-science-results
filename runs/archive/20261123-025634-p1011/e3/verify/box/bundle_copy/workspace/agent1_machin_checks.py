import sympy as s
x=s.Rational(1,5)
t=x
for _ in range(3):
    t=s.cancel((t+x)/(1-t*x))
u=s.Rational(1,239)
assert s.cancel((t-u)/(1+t*u))==1
# 0<4atan(1/5)-atan(1/239)<4/5<1<pi/2.
assert 4*(x-x**3/3)-u>0
# Strictly alternating decreasing arctan series brackets each angle.
def bracket(q,N=60):
    z=s.Rational(1,q)
    a=sum((-1)**j*z**(2*j+1)/s.Integer(2*j+1) for j in range(N))
    b=a+(-1)**N*z**(2*N+1)/s.Integer(2*N+1)
    return min(a,b),max(a,b)
a,b=bracket(5);c,d=bracket(239)
lo,hi=16*a-4*d,16*b-4*c
assert lo>3 and hi<4 and hi-lo<s.Rational(1,10)**80
print('Exact Machin tangent identity and 80-digit rational pi bracket checked.')
