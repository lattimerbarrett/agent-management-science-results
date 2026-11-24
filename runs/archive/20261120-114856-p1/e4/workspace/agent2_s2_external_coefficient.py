import sympy as S
from pathlib import Path
x,z,t=S.symbols('x z t');s=2
q=x*x+2*x-3;r=x*x-2*x-3;P4=S.expand(q*r-1);M4=S.expand(r*x);P=S.expand((x-z)*P4);M=S.expand((x-z)*M4)
def moments(P,M,n):
 se=S.series((M/P).subs(x,1/t),t,0,n+1).removeO().expand();return [S.cancel(se.coeff(t,j+1)) for j in range(n)]
def deriv(P,M,q,dM):
 n=S.degree(P,x);ms=moments(P,M,5);ds=moments(P,dM,5);G=S.Matrix(2,2,lambda i,j:ms[i+j]);rhs=S.Matrix([sum(co*ds[j+mon[0]] for mon,co in S.Poly(q,x).terms()) for j in range(2)])
 dc=-G.inv()*rhs;dq=dc[0]+dc[1]*x
 a,rem=S.div(q*M,P,x);h=S.Poly(rem,x).nth(n-3)
 da,dt=S.div(S.expand(dq*M+q*dM),P,x);dh=S.Poly(dt,x).nth(n-3)
 dnext=S.expand((dq*rem+q*dt)/h-q*rem*dh/h**2)
 dR=S.cancel(-dt.subs(x,0)/S.diff(rem,x).subs(x,0)+S.Poly(da,x).nth(0))
 return dnext,dR
D=S.expand(P4-(x-z)*M4)
# Use core perturbation 1 to enforce deltaR=0.
N=S.expand((x-z)*x)
DN,RN=deriv(P,M,q,N);DD,RD=deriv(P,M,q,D)
Dadjust=S.expand(D-RD/RN*N)
Dnext,Rzero=deriv(P,M,q,Dadjust);assert S.cancel(Rzero)==0
_,Rnext=deriv(P,S.expand((x-z)*q*x),r,Dnext)
neutral=S.Poly((q*r+1).subs(x,z),z)
num,den=S.fraction(S.cancel(Rnext+12/z))
assert S.rem(num,neutral.as_expr(),z)==0
print('External forcing coefficient c_beta=-4 q(zeta)/(zeta-beta), exact symbolic s2 sample: PASS')
