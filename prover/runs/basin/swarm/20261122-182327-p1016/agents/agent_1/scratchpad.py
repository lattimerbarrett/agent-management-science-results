import itertools, numpy as np
from sympy import Matrix
names=['a','b','U','V','W','Z','A','B','K','L']
Q=np.array([[1,0,1,1,0,0,-1,0,0,0],[0,1,0,0,1,1,0,-1,0,0],[0,0,0,1,0,1,0,0,-2,0],[0,0,1,0,1,0,0,0,0,-2]],dtype=int)
def facets(cols):
    arr=Q[:,cols]; out=set()
    for inds in itertools.combinations(range(len(cols)),3):
        ns=Matrix(arr[:,inds].T).nullspace()
        if len(ns)!=1:continue
        v=ns[0]; v=v* __import__('sympy').ilcm(*[x.q for x in v]); v=np.array(v,dtype=int).flatten()
        vals=v@arr
        if np.all(vals>=0):pass
        elif np.all(vals<=0):v=-v
        else:continue
        from functools import reduce
        from math import gcd
        v=v//reduce(gcd,v)
        out.add(tuple(v))
    return sorted(out)
mov=set()
for i in range(10):mov.update(facets([j for j in range(10) if j!=i]))
assert mov=={(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)}
print('MOV positive-orthant certificate passed')
# Toric fan for (2,2)
import sympy as s
verts=[s.eye(4)[:,i] for i in range(4)]
edges=list(itertools.combinations(range(4),2))
rays=verts+[(verts[i]+verts[j])/2 for i,j in edges]
ei={e:4+i for i,e in enumerate(edges)}
d=[ei[(0,2)],ei[(1,3)]]
ring=[ei[e] for e in [(0,1),(0,3),(2,3),(1,2)]]
tets=[tuple([i]+[ei[tuple(sorted((i,j)))] for j in range(4) if j!=i]) for i in range(4)]
tets += [tuple(d+[ring[i],ring[(i+1)%4]]) for i in range(4)]
perm=[1,0,3,2]
rperm=[perm[i] for i in range(4)]+[ei[tuple(sorted((perm[i],perm[j])))] for i,j in edges]
assert {frozenset(t) for t in tets}=={frozenset(rperm[i] for i in t) for t in tets}
for t in tets: assert abs(s.Matrix.hstack(*[rays[i] for i in t]).det())==s.Rational(1,8)
h=[0]*4+[-1]*6
for i in d:h[i]=s.Rational(-6,5)
for t in tets:
    c=s.Matrix.hstack(*[rays[i] for i in t]).T.inv()*s.Matrix([h[i] for i in t])
    assert all((c.dot(rays[j])==h[j] if j in t else c.dot(rays[j])<h[j]) for j in range(10))
cones={frozenset(c) for t in tets for k in range(5) for c in itertools.combinations(t,k)}
fixed=[c for c in cones if {rperm[i] for i in c}==set(c)]
print('fixed toric cones', [sorted(c) for c in fixed])
T=s.zeros(4)
for i in range(4):T[perm[i],i]=1
for c in fixed:
    # Fixed tangent directions: one per swapped ray, plus fixed part of tangent torus.
    swapped=sum(rperm[i]!=i for i in c)//2
    span=s.Matrix.hstack(*[rays[i] for i in c]) if c else s.zeros(4,0)
    plusspan=(span+T*span).rank()
    quotientplus=2-plusspan
    assert swapped+quotientplus>=1
print('toric smooth/projective/fixed-locus checks passed')
# Exact Jacobian-criterion/Serre normality checks.
vs=s.symbols('a b U V W Z A B K L')
a,b,U,V,W,Z,A,B,K,L=vs

def ideal_dimension(polys,vs):
    gb=s.groebner(polys,*vs,order='grevlex')
    supports=[{i for i,e in enumerate(p.LM(order=gb.order).exponents) if e} for p in gb.polys]
    if any(not t for t in supports):return -1
    for size in range(len(vs)+1):
        if any(all(set(c)&t for t in supports) for c in itertools.combinations(range(len(vs)),size)):
            return len(vs)-size
for m in [2,3]:
    fs=[U**2*L-V**2*K-a**m*A**(m-2),W**2*L-Z**2*K-b**3*B]
    J=s.Matrix(fs).jacobian(vs)
    minors=[J[:,[i,j]].det() for i,j in itertools.combinations(range(10),2)]
    dim=ideal_dimension(fs+minors,vs)
    print('singular dimension',m,3,dim)
    assert dim<=6
    pt1=dict(zip(vs,[0,0,1,1,1,1,1,1,0,0]))
    pt2=dict(zip(vs,[0,0,1,1,1,1,0,0,1,1]))
    assert all(f.subs(pt1)==0 and f.subs(pt2)==0 for f in fs)
    assert J.subs(pt1).rank()==1 and J.subs(pt2).rank()==2
    # The nontrivial stabilizer at pt2 is -1 in all four torus factors.
    assert all(sum(Q[:,i])%2==0 for i in [2,3,4,5,8,9])
for n in [2,3]:
    fv=W**2*L-Z**2*K-b**n*B**(n-2)
    v7=[b,U,V,W,Z,B,K,L]
    assert ideal_dimension([fv]+[s.diff(fv,x) for x in v7],v7)<=5
print('exact algebra checks passed')

def in_cone_exact(weights,theta):
    d=len(theta)
    for size in range(1,d+1):
        for sub in itertools.combinations(range(weights.cols),size):
            mat=weights[:,sub]
            if mat.rank()!=size:continue
            try:sol=mat.gauss_jordan_solve(s.Matrix(theta))[0]
            except ValueError:continue
            if all(x>=0 for x in sol):return True
    return not any(theta)
qpos=s.Matrix([[1,0,0,1,1,-1,0,0],[0,0,1,0,1,0,-2,0],[0,1,0,1,0,0,0,-2]])
vp=[b,U,V,W,Z,B,K,L]
from math import gcd
from functools import reduce
for n in [2,3]:
    f=W**2*L-Z**2*K-b**n*B**(n-2)
    terms=[set(i for i,x in enumerate(vp) if t.has(x)) for t in s.Add.make_args(f)]
    count=0
    for bits in itertools.product([0,1],repeat=8):
        supp=[i for i,t in enumerate(bits) if t]; ss=set(supp)
        active=sum(t<=ss for t in terms)
        if active==1:continue
        mat=qpos[:,supp]
        if not in_cone_exact(mat,[1,2,3]):continue
        count+=1
        # Gradient of each term is monomial; its nonvanishing is pattern-determined.
        assert any(all(bits[i] for i,x in enumerate(vp) if s.diff(f,y).has(x)) and s.diff(f,y)!=0 for y in vp)
        dets=[abs(int(mat[:,c].det())) for c in itertools.combinations(range(mat.cols),3)]
        assert reduce(gcd,dets,0)==1
    print('positive semistable supports checked',n,count)
# Boundary primality certificates: saturation plus a rational polynomial chart.
# In each displayed localization the equations solve for two distinct variables.
def check_saturated(polys,den,vs):
    t=s.Dummy('t')
    gb=s.groebner(polys+[1-t*den],t,*vs,order='lex')
    elim=[p.as_expr() for p in gb.polys if not p.as_expr().has(t)]
    orig=s.groebner(polys,*vs,order='lex')
    assert all(orig.reduce(f)[1]==0 for f in elim)
for m in [2,3]:
    fs=[U**2*L-V**2*K-a**m*A**(m-2),W**2*L-Z**2*K-b**3*B]
    for e,den in [(A,U*b),(B,W*(U**2*Z**2-V**2*W**2)),(K,U*b),(L,V*b)]:
        check_saturated(fs+[e],den,vs)
for n in [2,3]:
    fs=[W**2*L-Z**2*K-b**n*B**(n-2)]
    for e,den in [(B,W),(K,W),(L,Z)]:
        check_saturated(fs+[e],den,vp)
for m in [2,3]:
    check_saturated([U**2*L-V**2*K-a**m*A**(m-2),W**2*L-Z**2*K-b**3*B],U*b,vs)
for n in [2,3]:
    check_saturated([W**2*L-Z**2*K-b**n*B**(n-2)],W,vp)
print('domain and boundary primality saturation certificates passed')
# Exact group calculations, without floating-point roots of unity.
for m,n in [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]:
    group={(i,j,e) for i in range(2*m) for j in range(2*n) for e in [0,1] if (i-j)%2==0}
    def mul(x,y):
        i,j,e=x; I,J,E=y
        return ((i+(-1)**e*I)%(2*m),(j+(-1)**e*J)%(2*n),(e+E)%2)
    def inv(x):
        return next(y for y in group if mul(x,y)==(0,0,0))
    classes=[]; todo=set(group)
    while todo:
        x=next(iter(todo)); c={mul(mul(y,x),inv(y)) for y in group}
        todo-=c; classes.append(c)
    def age(x):return 1 if x[2] else int(x[0]!=0)+int(x[1]!=0)
    juniors=sum(age(next(iter(c)))==1 for c in classes)
    comm={(0,0,0)}
    generators={mul(mul(mul(x,y),inv(x)),inv(y)) for x in group for y in group}
    while True:
        new=comm|{mul(x,y) for x in comm for y in generators}
        if new==comm:break
        comm=new
    assert len(group)==4*m*n
    if (m,n)!=(2,2):
        assert comm=={(2*i,2*j,0) for i in range(m) for j in range(n)}
        assert juniors==2+(m>1)+(n>1)
    else:
        assert comm=={(0,0,0),(2,2,0)} and juniors==6
    print('group',m,n,'order',len(group),'junior classes',juniors)

# Cones of the two obstructing points have the asserted single extra inequality.
assert set(facets([2,3,4,5,6,7]))=={(-1,-1,1,1),(-1,0,1,1),(0,-1,1,1),(0,0,0,1),(0,0,1,0)}
assert set(facets([2,3,4,5,8,9]))=={(0,1,0,0),(1,0,0,0),(1,1,-1,-1),(1,1,-1,0),(1,1,0,-1)}
for cols,expected in [([2,3,4,5,6,7],1),([2,3,4,5,8,9],2)]:
    mat=s.Matrix(Q[:,cols])
    assert reduce(gcd,[abs(int(mat[:,c].det())) for c in itertools.combinations(range(6),4)],0)==expected
print('obstructing cones and stabilizers certified')

