import sympy as S

# The invertible projective coordinate change from the Veronese conic.
T=S.Matrix([[1,1,0],[0,1,1],[0,-1,0]])
assert T.det()==1
s,t,u,v=S.symbols('s t u v')
a=s*u; b=(s*v+t*u)/2; c=t*v
Z=T*S.Matrix([a,b,c])
q=lambda Z:S.expand(Z[0]*Z[1]+Z[0]*Z[2]+Z[1]*Z[2])
assert S.factor(q(Z))==-(s*v-t*u)**2/4
# No base points: verify all four affine charts algebraically.
for subs,variables in [({s:1,u:1},(t,v)),({s:1,v:1},(t,u)),
                       ({t:1,u:1},(s,v)),({t:1,v:1},(s,u))]:
    G=S.groebner([z.subs(subs) for z in Z],*variables)
    assert list(G)==[1]
z,w=S.symbols('z w')
assert S.det(S.Matrix([z*w,(z+w)/2]).jacobian([z,w]))==(w-z)/2

# On the diagonal the map parametrizes the branch conic.
P=S.Matrix([s*(s+t),t*(s+t),-s*t])
assert all(S.expand(e)==0 for e in Z.subs({u:s,v:t})-P)
assert q(P)==0
assert P.subs({s:1,t:0})==S.Matrix([1,0,0])
assert P.subs({s:0,t:1})==S.Matrix([0,1,0])
assert P.subs({s:1,t:-1})==S.Matrix([0,0,1])

# Exact critical-point calculation on the conic, t=1, s=x+i*y.
x,y=S.symbols('x y', real=True)
r=x*x+y*y
N=S.expand(r*(1-((x+1)**2+y*y)))
D=S.expand((r+1)*((x+1)**2+y*y)+r)
A=S.expand(-(S.diff(N,x)*D-N*S.diff(D,x))/2)
B=S.expand(-(S.diff(N,y)*D-N*S.diff(D,y))/(2*y))
assert S.expand(A-x*B-r*(2*r+1))==0
assert S.factor(A.subs(y,0))==3*x*x*(x+1)*(x*x+x+1)
# D>0: its two nonnegative summands cannot vanish together.
assert D.subs({x:0,y:0})==1
# On the real axis the last quadratic is strictly positive.
assert S.expand((x+S.Rational(1,2))**2+S.Rational(3,4)-(x*x+x+1))==0

# Cohomology ring Q[alpha,beta]/(alpha^2,beta^2): nonzero length-2 product.
alpha,beta=S.symbols('alpha beta')
G=S.groebner([alpha**2,beta**2],alpha,beta)
assert G.reduce(alpha*beta)[1]==alpha*beta
for monomial in [alpha**3,alpha**2*beta,alpha*beta**2,beta**3]:
    assert G.reduce(monomial)[1]==0
print('All exact algebraic checks passed.')
print('Critical points on the branch conic: [s:t]=[1:0], [0:1], [1:-1].')
