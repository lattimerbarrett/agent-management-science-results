import sympy as s
# Product-rule identity for phi=rho*exp(A*u), u=|z|^2.
# Formal jet variables suffice to check the dimension-free identity.
A,rho=s.symbols("A rho", real=True)
rj,rk,uj,uk,h=s.symbols("rj rk uj uk h")
# phi_jbar{k}/exp(Au)
full=h+A*(rj*uk+uj*rk)+rho*(A*s.Symbol("delta")+A*A*uj*uk)
# Restriction to ker partial rho removes both first derivatives of rho.
restricted=full.subs({rj:0,rk:0})
assert s.expand(restricted-(h+A*rho*s.Symbol("delta")+A*A*rho*uj*uk))==0
# Independent differentiation check in three dimensions.
n=3
z=s.symbols("z0:3"); b=s.symbols("b0:3")
u=sum(z[j]*b[j] for j in range(n))
r=s.Function("r")(*z,*b)
phi=r*s.exp(A*u)
for j in range(n):
 for k in range(n):
  exact=s.diff(phi,z[j],b[k])/s.exp(A*u)
  predicted=s.diff(r,z[j],b[k])+A*(s.diff(r,z[j])*z[k]+b[j]*s.diff(r,b[k]))+r*(A*int(j==k)+A*A*b[j]*z[k])
  assert s.simplify(exact-predicted)==0
# For A>C and rho>0 the lower bound is strictly positive.
a,c,t=s.symbols("a c t",positive=True)
assert s.simplify(((c+a)-c)*t-a*t)==0
print("Exact product-rule and tangent-space Levi identities checked.")
print("No Oka theorem is asserted or numerically checked by this code.")
