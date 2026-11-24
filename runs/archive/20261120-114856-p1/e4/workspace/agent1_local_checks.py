import sympy as S
# Exact verification of two-step reflected-Newton local expansion on a finite design.
e=S.symbols('e')
a=[S.Matrix(x) for x in [(1,0),(0,1),(-1,-1),(2,1),(-2,-1)]]
w=[S.Rational(1,5)+e*S.Rational(v,30) for v in [1,2,-1,1,-3]]
def params(w):
 m=sum((wi*ai for wi,ai in zip(w,a)),S.zeros(2,1))
 G=sum((wi*ai*ai.T for wi,ai in zip(w,a)),S.zeros(2))
 u=G.inv()*m
 d=(m.T*u)[0]
 return m,G,u,d
def step(w):
 m,G,u,d=params(w)
 return [S.cancel(wi*(1-(ai.T*u)[0])**2/(1-d)) for wi,ai in zip(w,a)]
def trunc(x,n=5):return S.series(x,e,0,n).removeO().expand()
def truncw(w,n=5):return [trunc(x,n) for x in w]
m,G,u,d=params(w)
w1=truncw(step(w))
w2=truncw(step(w1))
u2=params(w2)[2]
for j in range(2):
 diff=trunc(u2[j]-u[j])
 print('u2-u component',j,diff)
 assert all(diff.coeff(e,k)==0 for k in range(4))
# Two-step tangent drift to second order, with exact rational Taylor checking.
z=[(ai.T*u)[0] for ai in a]
H2=sum((wi*ai*zi**2 for wi,ai,zi in zip(w,a,z)),S.zeros(2,1))
v=G.inv()*H2
for i in range(len(w)):
 predicted=2*w[i]*(d-z[i]**2+(a[i].T*v)[0])
 diff=trunc(w2[i]-w[i]-predicted,3)
 assert diff==0,(i,diff)
print('PASS: quadratic tangent drift and cubic cancellation of normal u, exact rational coefficients')
