import sympy as s
from pathlib import Path
a,b,c,d=s.symbols('a b c d',real=True)
t=c*c+d*d
R2=a*a+b*b+t
r=-2*s.sqrt(3)*a-a*a-b*b+2*t-t*t
p2=-a*a-b*b+2*t
E=-t*t-4*s.sqrt(3)*a*(p2-t*t)+(p2-t*t)**2
Re_g=-s.sqrt(3)*a+3*(a*a-b*b)
assert s.expand((r+r*r)-(2*Re_g+5*(a*a+b*b)+2*t+E))==0
delta=s.Rational(1,100)
err=16*delta+5*delta**2+8*delta**3+4*delta**4+delta**6
rbound=4*delta+2*delta**2+delta**4
assert err<s.Rational(1,2)
assert rbound<1
eta=delta**2/16
assert eta<delta**2/8
text='''Explicit obstruction for the n=2 version of the candidate. Put q=(sqrt(3),0), x=z-sqrt(3)=a+ib, w=c+id, t=|w|^2, R^2=|x|^2+t. On the exterior, r=-rho<0. Let s0=r+r^2 and g(x)=-sqrt(3)x+3x^2. Exact expansion:
s0=2Re g+5|x|^2+2t+E,
E=-t^2-4sqrt(3)a(-|x|^2+2t-t^2)+(-|x|^2+2t-t^2)^2.
For R<delta=1/100, |r|<4delta+2delta^2+delta^4<1, hence s0<0. Also |E| <= R^2(16delta+5delta^2+8delta^3+4delta^4+delta^6)<R^2/2. Therefore 2Re g+(3/2)R^2<0. The strictly psh function h=Re g+R^2/4 satisfies h<-R^2/2. For eta=delta^2/16, define u=max(h,-eta) on exterior intersect B(q,delta), and u=-eta elsewhere. On the collar delta/2<R<delta one has h<-delta^2/8<-eta, so the gluing is psh and continuous. Along the outward normal x>0,w=0, h tends to 0. Thus u is bounded continuous psh and nonconstant, directly certifying that this same candidate is not Oka in n=2. This adds no missing Oka implication in n>=3.\n'''
Path('workspace/agent3_explicit_n2_peak.txt').write_text(text)
print('PASS exact Taylor decomposition and rational bounds',err,rbound,eta)
print(text)
