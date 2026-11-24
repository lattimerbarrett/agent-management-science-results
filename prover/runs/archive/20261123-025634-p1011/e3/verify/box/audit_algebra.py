import sys
sys.path.insert(0,'workspace')
import sympy as s
from agent2_finite_maxima_certificates import blocks
for n in [19,40,41,60]:
 q=blocks(n,J=1);d=n-1
 a=s.factor(q[1][1,1]-s.Rational(2,d)*(q[2][0,1]+q[2][0,0]))
 b=s.factor(q[3][0,0]-s.Rational(d,2)*q[2][0,1]+s.Rational(d+4,2)*q[2][0,0])
 print(n,a,b)
# Derive coefficient of all linear geometric/cutoff terms in physical variables.
n,r=s.symbols('n r', positive=True);H=s.Function('H')(r);chi=s.Function('chi')(r)
a=(n-2)/2;B=(n-2)/(2*(n-1))
# E_1(chi z,z) integrated angularly, prior integration by parts.
z=r**(2-n)
E=-H*s.diff(chi*z,r)*s.diff(z,r)*r**(n-2)+B*(s.diff(H,r,2)+(n-2)/r*s.diff(H,r))*chi*z*z*r**(n-2)
# Integrate H'' and H' onto chi z^2 (all chi' boundary terms vanish).
Eafter=-H*s.diff(chi*z,r)*s.diff(z,r)*r**(n-2)+B*H*(s.diff(chi*z*z*r**(n-2),r,2)-s.diff((n-2)*chi*z*z*r**(n-3),r))
L=a*B*r**(-(n-2))*(2*H/r-s.diff(H,r))
# Cchi integrated H' by parts
Cafter=a*B*H*(2*s.diff(chi,r)*r**(1-n)+s.diff(s.diff(chi,r)*r**(2-n),r))
print('Nchi coefficient equality',s.simplify(a*Eafter-Cafter))
