from fractions import Fraction as Q
import sympy as s
# H0(z,w)=(w, a*z+w*w), a=1/10.
a=Q(1,10)
# If |w|>=max(|z|,2), then |w_new| >= |w|²-a|z|
# >= (2-a)|w|, while |z_new|=|w|, preserving escape cone.
assert 2-a>1
# Sink at 0: linear eigenvalues satisfy lambda²=a, hence modulus sqrt(a)<1.
assert 0<a<1
# For all 0<eps<1, write r=sqrt(1-eps), R=sqrt(1+eps).
# C=(eps+R+3)/r gives C*r-eps=R+3>max(R,2).
eps=s.symbols('eps',positive=True)
r=s.sqrt(1-eps); R=s.sqrt(1+eps)
C=(eps+R+3)/r
assert s.simplify(C*r-eps-(R+3))==0
assert s.ask(s.Q.positive(R+3-2))
# Concrete FAT eps=.9, C=20. Certify with rational bounds r>3/10,R<14/10.
e=Q(9,10); c=20
assert Q(3,10)**2 < 1-e
assert Q(14,10)**2 > 1+e
lower=c*Q(3,10)-e
assert lower>2 and lower>Q(14,10)
# Linear shear Phi(z,w)=(z,w-Cz), inverse=(z,w+Cz), fixes 0.
z,w,cc=s.symbols('z w cc')
assert s.expand((w-cc*z)+cc*z)==w
print('Certified: every solid torus eps in (0,1) avoids an attracting Henon basin after a linear shear.')
print('For eps=9/10,C=20: lower bound |w-Cz| >', lower)
