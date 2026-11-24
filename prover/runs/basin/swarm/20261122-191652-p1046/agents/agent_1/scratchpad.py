import sympy as S
s,v=S.symbols('s v')
Q=S.Rational(2)

def simp(x): return S.cancel(x)
def zero(x): return simp(x)==0
def meq(A,B):
    assert A.shape==B.shape
    assert all(zero(x-y) for x,y in zip(A,B))

E=S.Matrix([[1-v**2*s/2,v*(1-s)],[-v*(1-s),2*s-v**2]])
O=S.Matrix([[2*s-v**2/4,v*(1-2*s)/2],[-v*(1-2*s)/2,1-v**2*s/2]])/s
delta=(2-v**2)**2/2
epsilon=(4-v**2)**2/8
assert zero(E.det()-delta*s)
assert zero(O.det()-epsilon/s)

def Phi(F,r):
    I=F.inv().applyfunc(simp)
    return S.Matrix([[I[0,0].subs(s,Q**(2*r)*s),I[1,0].subs(s,Q**r*s)],
                     [I[0,1].subs(s,Q**r*s),I[1,1]]]).applyfunc(simp)
meq(Phi(E,1),O/delta)
meq(Phi(O,-1),E.subs(v,v/2)/epsilon)
# For v=2^(-k), the two exceptional factors are positive for every k>=0:
u=S.symbols('u', real=True)
assert S.ask(S.Q.positive(2-u),S.Q.nonnegative(u)&S.Q.nonnegative(1-u))
assert S.ask(S.Q.positive(4-u),S.Q.nonnegative(u)&S.Q.nonnegative(1-u))

# Exact skew Laurent arithmetic: dict i -> f_i(s), representing sum f_i(s)c^i.
# Thus c*s=2*s*c. The parameter v is central.
def clean(a): return {i:simp(f) for i,f in a.items() if not zero(f)}
def add(a,b):
    d=dict(a)
    for i,f in b.items(): d[i]=d.get(i,0)+f
    return clean(d)
def neg(a): return {i:-f for i,f in a.items()}
def mul(a,b):
    d={}
    for i,f in a.items():
        for j,g in b.items():
            d[i+j]=d.get(i+j,0)+f*g.subs(s,Q**i*s)
    return clean(d)
def elt(f): return clean({0:S.sympify(f)})
def power_c(i): return {i:S.Integer(1)}
def eq(a,b): assert not add(a,neg(b))
def mm(A,B):
    return [[add(mul(A[i][0],B[0][j]),mul(A[i][1],B[1][j])) for j in range(2)] for i in range(2)]
def tr(A): return [[A[j][i] for j in range(2)] for i in range(2)]
def eqm(A,B):
    for i in range(2):
        for j in range(2): eq(A[i][j],B[i][j])
def R(F,r):
    # diag(c^r,1) F diag(c^-r,1)
    return [[elt(F[0,0].subs(s,Q**r*s)),mul(elt(F[0,1].subs(s,Q**r*s)),power_c(r))],
            [mul(elt(F[1,0]),power_c(-r)),elt(F[1,1])]]
I=[[elt(1),{}],[{},elt(1)]]
c,ci,a=power_c(1),power_c(-1),elt(1-s)
eq(mul(c,elt(s)),mul(elt(2*s),c))
A=[[a,mul(c,a)],[neg(mul(a,ci)),neg(mul(mul(c,a),ci))]]
eqm(A,R(E.subs(v,1),1))
# Check the singular transpose factorization used to explain the initial stage.
col=[elt(1),c]; row=[a,neg(mul(a,ci))]
eqm(tr(A),[[mul(col[i],row[j]) for j in range(2)] for i in range(2)])
# Verify inverses and inverse-transposes in the actual noncommutative algebra.
for F,r in [(E,1),(O,-1)]:
    B=R(F,r); Bi=R(F.inv().applyfunc(simp),r)
    eqm(mm(B,Bi),I); eqm(mm(Bi,B),I)
    eqm(tr(Bi),R(Phi(F,r),-r))

# Verify the path commutation formulas on exponent vectors.
# t^a*t^b=2^(-sum a[i+1]*b[i])*t^(a+b).
def comm_exp(a,b):
    return sum(b[i+1]*a[i]-a[i+1]*b[i] for i in range(len(a)-1))
for n in range(2,22,2):
    N=n+3
    unit=lambda i: tuple(int(j==i-1) for j in range(N))
    z=tuple(int(j<n and j%2==0) for j in range(N))
    cvec=tuple(int(j<=n and j%2==0) for j in range(N))
    for i in range(1,n+2): assert comm_exp(cvec,unit(i))==0
    assert comm_exp(z,unit(n))==1
    assert comm_exp(cvec,unit(n+2))==1
    for i in range(1,n+1): assert comm_exp(unit(n+2),unit(i))==0

# Exact additional iterates, independently of the closed-form induction.
F=E.subs(v,1); r=1; lam=S.Integer(1)
for k in range(8):
    vk=S.Rational(1,2)**k
    meq(F,lam*E.subs(v,vk))
    assert not zero(F.det())
    G=Phi(F,r); assert not zero(G.det())
    meq(G,O.subs(v,vk)/(lam*delta.subs(v,vk)))
    F=Phi(G,-r)
    lam=simp(lam*delta.subs(v,vk)/epsilon.subs(v,vk))

# Universal dimension recurrence in the reflection argument.
r=S.symbols('r',integer=True,positive=True)
a,b=r-1,r
assert (b,S.expand(b-a))==(r,1)
for depth in range(1,101):
    a,b=0,1
    for j in range(depth-1,0,-1): a,b=b,2*b-a
    assert (a,b)==(depth-1,depth)
    a,b=b,b-a
    assert (a,b)==(depth,1)
print('All exact checks passed: universal identities, skew inverses, path relations, 16 iterates, and reflection recurrence.')
