from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import sympy as sp,json
M=F(1,8);t=13
# Nine a/b colors (one has a nontrivial two-atom real mixture), one c,
# and three S={a,b} colors. Every color also has its common dummy.
fams=[]
fams.append([frozenset({0,1})]) # color 0: S
fams.append([frozenset({0}),frozenset({1})]) # color 1
fams.append([frozenset({2})]) # color 2: c
fams.extend([[frozenset({0})] for _ in range(4)])
fams.extend([[frozenset({1})] for _ in range(4)])
fams.extend([[frozenset({0,1})] for _ in range(2)])
assert len(fams)==t
vertices=[];colors=[];weights=[];index={}
for i,fam in enumerate(fams):
    for j,A in enumerate(fam):
        index[i,j]=len(vertices);vertices.append(A);colors.append(i)
        weights.append(F(1,6) if i in (0,11,12) else (F(1,2) if i==1 else F(1)))
    index[i,'d']=len(vertices);vertices.append(None);colors.append(i)
    weights.append(F(5,6) if i in (0,11,12) else F(0))
n=len(vertices)
D=[[F(0) for _ in range(n)] for __ in range(n)]
for a in range(n):
    for b in range(a):
        A,B=vertices[a],vertices[b]
        value=F(0) if A is None and B is None else (M if A is None or B is None else F(not A&B))
        D[a][b]=D[b][a]=value
assert all(sum(weights[j] for j in range(n) if colors[j]==i)==1 for i in range(t))
R=sum(w for A,w in zip(vertices,weights) if A is not None)
delta=M*(2*R-t);assert R==F(21,2) and delta==1
Q=sum(D[a][b]*weights[a]*weights[b] for a in range(n) for b in range(a))
assert Q==F(1057,32)
grad=[sum(D[a][b]*weights[b] for b in range(n)) for a in range(n)]
for i in range(t):
    supported=[a for a in range(n) if colors[a]==i and weights[a]>0]
    g=grad[supported[0]]
    assert all(grad[a]==g for a in supported)
    assert all(grad[a]<=g for a in range(n) if colors[a]==i)
# Exact GLOBAL optimum certificate via aggregate real masses A,B,C,S.
# Let a=A+B<=9,c=C<=1,s=S<=3 and z=a+c+s. Actual Q=AB+c(a+s).
# For z<=3: <=z^2/3; for 3<=z<=10: <=(z-1)^2/4+z-1;
# for 10<=z<=13: <=z+77/4. Adding M*z*(13-z) proves global maximum.
z=sp.symbols('z',real=True)
pieces=[z*z/3+sp.Rational(1,8)*z*(13-z),
        (z-1)**2/4+z-1+sp.Rational(1,8)*z*(13-z),
        z+sp.Rational(77,4)+sp.Rational(1,8)*z*(13-z)]
assert sp.diff(pieces[0],z,2)>0 and sp.diff(pieces[1],z,2)>0
assert max(pieces[0].subs(z,a) for a in (0,3))<sp.Rational(1057,32)
assert max(pieces[1].subs(z,a) for a in (3,10))<sp.Rational(1057,32)
assert sp.solve(sp.diff(pieces[2],z),z)==[sp.Rational(21,2)]
assert pieces[2].subs(z,sp.Rational(21,2))==sp.Rational(1057,32)
# Nontrivial pure-real norm-two root and three mixed norm-2M roots.
B=sp.Matrix([[sp.Rational(1)-sp.Rational(D[a][b].numerator,D[a][b].denominator) for b in range(n)] for a in range(n)])
def root(a,b):
    v=sp.zeros(n,1);v[a]=1;v[b]=-1;return v
roots=[root(index[1,0],index[1,1])]+[root(index[i,0],index[i,'d']) for i in (0,11,12)]
G=sp.Matrix([[(u.T*B*v)[0] for v in roots] for u in roots])
assert G==sp.diag(2,0,0,0)+sp.diag(0,1,1,1)*sp.Matrix([[0,0,0,0],[0,sp.Rational(1,4),sp.Rational(1,4),sp.Rational(1,4)],[0,sp.Rational(1,4),sp.Rational(1,4),sp.Rational(1,4)],[0,sp.Rational(1,4),sp.Rational(1,4),sp.Rational(1,4)]])
assert all(e>=0 for e in G.eigenvals())
for i in (0,11,12):
    S=fams[i][0];count=0
    for j in range(t):
        if weights[index[j,'d']]==0:
            statuses={bool(S&A) for A in fams[j]}
            assert len(statuses)==1
            count+=not next(iter(statuses))
    assert count==delta
result=dict(colors=t,real_vertices=sum(map(len,fams)),supported_vertices=sum(w>0 for w in weights),M=str(M),R=str(R),delta=str(delta),Q=str(Q),all_KKT_conditions=True,analytic_global_optimum=str(Q),gram=str(G),eigenvalues={str(e):int(v) for e,v in G.eigenvals().items()},nontrivial_pure_real_multisupport=True)
print(json.dumps(result,indent=2))
Path('workspace/agent2_common_dummy_integer_phase_checks.json').write_text(json.dumps(result,indent=2))
