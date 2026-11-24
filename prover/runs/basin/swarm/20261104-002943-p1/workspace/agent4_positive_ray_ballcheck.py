from sage.all import RealBallField, matrix, vector, QQ
from pathlib import Path
R=RealBallField(256);delta=R(QQ(79)/10);C=R(64)-delta**2
ap=(R(5)+(R(8)+delta).sqrt()).sqrt();dp=(R(5)-(R(8)+delta).sqrt()).sqrt();bp=(R(5)+(R(8)-delta).sqrt()).sqrt();cp=(R(5)-(R(8)-delta).sqrt()).sqrt()
roots=[-ap,-dp,cp,bp]
def pol(x):
 y=R(1)
 for a in roots:y*=x-a
 return y
xs=[R(-3),-R(5).sqrt(),R(-1),R(1),R(5).sqrt(),R(3)]
P=vector(R,[pol(x) for x in xs]);Q=vector(R,[pol(-x) for x in xs])
# Derivative of D6 evaluated at each root.
Dp=vector(R,[R(1) for x in xs])
for i,x in enumerate(xs):
 for j,y in enumerate(xs):
  if i!=j:Dp[i]*=x-y
w=vector(R,[C*xs[i]/(Dp[i]*P[i]) for i in range(6)]);assert all(a.lower()>0 for a in w)
V=matrix(R,[[x**j for j in range(4)] for x in xs]);M=V.transpose()*matrix.diagonal(w)*V;z=vector(R,[w[i]*P[i]**2/C for i in range(6)]);N=V.transpose()*matrix.diagonal(z)*V
nu=(2*delta**2-64).sqrt();mu=(R(5)+(R(8)-nu).sqrt()).sqrt();vm=vector(R,[(-mu)**j for j in range(4)]);vp=vector(R,[mu**j for j in range(4)]);u=pol(mu);vv=pol(-mu);r=-vv/u;assert r.lower()>0
force=4*vv/C*N.inverse()*(vm-vp);ac=-C*M.inverse()*N;Frow=vector(R,[sum(w[i]*P[i]**3*V[i,j] for i in range(6)) for j in range(4)]);beta_m=-(u*(vm*ac)+vv*C*vm+Frow)/C;beta_p=-(vv*(vp*ac)+u*C*vp+Frow)/C
kap2=beta_m*force;assert kap2.lower()>500 and kap2.upper()<600
assert (beta_m*force-beta_p*force).contains_zero()
kap=kap2.sqrt();h=-force/kap;E=-(Frow*h)/C;assert E.lower()>70 and E.upper()<80
assert all((a).contains_zero() for a in V.transpose()*vector(R,[w[i]*P[i] for i in range(6)]))
print('CERTIFIED ball bounds κ²=',kap2,'r=',r,'fuel=',E)
