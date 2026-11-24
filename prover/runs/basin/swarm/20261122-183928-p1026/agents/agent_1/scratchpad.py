import sympy as S
from itertools import combinations
from functools import lru_cache
from math import prod

# I. Exact finite check: complex dimensions 8,...,14.
s, x = S.symbols('s x')
q = {}
Ac = [S.S.One, s/2] + [S.bernoulli(j)/S.factorial(j)
      if j % 2 == 0 else S.S.Zero for j in range(2,15)]
for j in range(1,15):
    q[j] = S.expand(Ac[j] - sum(S.Rational(i,j)*q[i]*Ac[j-i]
                                for i in range(1,j)))
kernels=[]
spaces=0
for d in range(8,15):
    pairs=[S.Poly(x**i+x**(d-i),x) for i in range(d//2+1)]
    candidates=set()
    for p in pairs:
        for sign in (-1,1):
            candidates.add(tuple(sign*p.nth(i) for i in range(d+1)))
    for p in pairs:
        for r in pairs:
            for e in (-1,1):
                for f in (-1,1):
                    pp=e*p+f*r
                    candidates.add(tuple(pp.nth(i) for i in range(d+1)))
    candidates.discard((0,)*(d+1))
    for a in range(1,d//2+1):
        fs=[q[d],q[a]*q[d-a]]
        if d==3*a:
            fs.append(q[a]**3)
        columns=[]
        for f in fs:
            poly=S.Poly(f,s)
            H=sum(co*(1+x)**mon[0]*(1-x)**(d-mon[0])
                  for mon,co in poly.terms())
            columns.append(S.Poly(H,x))
        C=S.Matrix([[p.nth(i) for p in columns] for i in range(d+1)])
        left=C.T.nullspace()
        for v in candidates:
            vv=S.Matrix(v)
            assert any((w.T*vv)[0] != 0 for w in left), (d,a,v)
        if C.rank()<len(fs):
            kernels.append((d,a))
        spaces+=1
assert kernels==[(9,3)], kernels
assert S.expand(q[9]+3*q[3]*q[6]+S.Rational(3,2)*q[3]**3)==0
print('Finite genus check:',spaces,'spaces; only kernel:',kernels)

# II. Exact finite certificates for ALL complex dimensions >=15.
n,h,t = S.symbols('n h t')
U=2*S.sinh(t/2)/t
logU=S.series(S.log(U),t,0,14).removeO()
Un=S.series(S.exp(n*logU),t,0,14).removeO()
Rs={1:t*S.coth(t/2)/2-1,
    2:t**2/(4*S.sinh(t/2)**2)+t**2/12-1,
    3:t**3*S.cosh(t/2)/(8*S.sinh(t/2)**3)-1}
def minors_of_moments(expr):
    P=S.Poly(expr,t)
    M=[S.factor(P.nth(2*k)*S.factorial(2*k)) for k in range(7)]
    return [S.fraction(S.factor(S.det(S.Matrix(
            [[M[i+j] for j in js] for i in range(3)]))))[0]
            for js in combinations(range(5),3)]
for a in (1,2,3):
    R=S.series(Rs[a],t,0,14).removeO()
    gb=S.groebner(minors_of_moments(Un*(1+h*R)),h,n,domain=S.QQ)
    assert gb.reduce(n**2*(n-a)**2)[1]==0
    print('Moment certificate a =',a,': n^2(n-a)^2 belongs to minor ideal')
R=S.series(Rs[1],t,0,14).removeO()
gb=S.groebner(minors_of_moments(Un*R),n,domain=S.QQ)
assert gb.reduce(S.S.One)[1]==0
print('Zero-Euler a=1 certificate: minor ideal is the unit ideal')

# III. The 18-dimensional construction: symbolic localization for all N.
N,u=S.symbols('N u', positive=True)
alpha=(1,9,-10)
beta=(5,6,-11)
assert sum(alpha)==sum(beta)==0
assert sum(alpha[i]*alpha[j] for i,j in combinations(range(3),2))==-91
assert sum(beta[i]*beta[j] for i,j in combinations(range(3),2))==-91
assert prod(alpha)==-90 and prod(beta)==-330
points=[]
for triple,eps in ((alpha,1),(beta,-1)):
    for sign in (1,-1):
        ws=[S.S.One]*6+[sign*N*v for v in triple]
        cp=S.Poly(prod(1+w*u for w in ws),u)
        points.append((eps,[cp.nth(j) for j in range(10)],S.prod(ws)))
@lru_cache(None)
def parts(d,m=None):
    if d==0: return ((),)
    if m is None: m=d
    return tuple((i,)+p for i in range(min(d,m),0,-1)
                 for p in parts(d-i,i))
def residue(part):
    return S.cancel(sum(eps*S.prod(cs[j] for j in part)/e
                        for eps,cs,e in points))
low=0
for degree in range(9):
    for part in parts(degree):
        assert residue(part)==0
        low+=1
values={p:residue(p) for p in parts(9)}
nonzero={p:v for p,v in values.items() if v!=0}
assert nonzero=={(3,3,3):-201600*N**6}
print('Localization:',low,'lower-degree identities;',len(values),'Chern numbers')
print('Nonzero Chern number:',nonzero)
# Two-point G2-sphere chi_y identity, with two independent characters.
A,B,y=S.symbols('A B y')
fiber=[A,B,1/(A*B)]
def chi_term(ws):
    return S.prod((1+y/w)/(1-1/w) for w in ws)
assert S.factor(chi_term(fiber)+chi_term([1/w for w in fiber])-y*y+y)==0
print('G2-sphere chi_y identity checked.')
