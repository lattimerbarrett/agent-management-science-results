"""Independent derivation audit of agent2's mixed-clique certificate."""
import sympy as S
p,r,h,x,y=S.symbols('p r h x y');s=1-r;xx=[x,y,1-x-y]
tau=s*(1-p)/p;nu=(p+h-2)/(p*s)
mu=[(2*tau-r)/3+r*t for t in xx]
q=[t/2 for t in mu]
M=S.zeros(3)
for i in range(3):M[i,i]=S.Rational(1,3)+nu*s*xx[i]
for k in range(3):
 ij=[i for i in range(3) if i!=k];M[ij[0],ij[1]]=M[ij[1],ij[0]]=q[k]
A=2*p;B=6*(p+h-2);C=2*s*(1-p)-p*r;D=3*p*r
N=S.Matrix([[A+B*xx[0],C+D*xx[2],C+D*xx[1]],
            [C+D*xx[2],A+B*xx[1],C+D*xx[0]],
            [C+D*xx[1],C+D*xx[0],A+B*xx[2]]])
assert all(S.cancel(v)==0 for v in 6*p*M-N)
d=2-2*r+p*r;e=3*p*r
for k in range(3):assert S.cancel(2*p*(1+3*q[k])-(d+e*xx[k]))==0
assert S.cancel(sum(mu)-2*tau)==0
base=2*p*s*(1-p)/3+(p+h-2)*r*(p*p/3-r)/(p*s)
assert S.cancel((p*p/3)*sum(mu)+nu*r*(p*p/3-r)-base)==0
# The domain triangle for the symmetric invariants.
X,Y,Z=S.symbols('X Y Z');ss=X+Y+Z;e2=X*Y+X*Z+Y*Z;e3=X*Y*Z
assert S.expand(ss*e2-9*e3-(X*(Y-Z)**2+Y*(Z-X)**2+Z*(X-Y)**2))==0
A0,B0,C0=S.symbols('A0 B0 C0',nonnegative=True)
schur=S.expand(ss**3+9*e3-4*ss*e2)
assert S.expand(schur.subs({X:A0+B0+C0,Y:B0+C0,Z:C0})-(A0*A0*(A0+2*B0+C0)+B0*C0*(A0+B0)))==0
print('INDEPENDENT symbolic dual scaling, B denominator, base, and invariant-domain identities all verified.')
if __name__=='__main__':
 import agent2_mixed_certificate
 agent2_mixed_certificate.main()
