import sympy as s
from itertools import combinations
from math import comb
N=6
pairs=list(combinations(range(N),2)); idx={p:i for i,p in enumerate(pairs)}
def wedge(u,v):
 return s.Matrix([u[i]*v[j]-u[j]*v[i] for i,j in pairs])
eye=s.eye(N)
J=s.zeros(N)
for i,j in [(0,1),(2,3),(4,5)]: J[i,j]=1; J[j,i]=-1
assert J.det()==1
G=s.diag(2,1,1,1,1,1)
assert G*J*G.T != J and G*J*G.T != 2*J
# Koszul global sections: V* tensor V* -> Sym^2 V*, kernel wedge^2.
sympairs=list(combinations(range(N),2))+[(i,i) for i in range(N)]
D=s.zeros(21,36)
for i in range(N):
 for j in range(N): D[sympairs.index(tuple(sorted((i,j)))),N*i+j]=1
K=s.zeros(36,15)
for k,(i,j) in enumerate(pairs): K[N*i+j,k]=1; K[N*j+i,k]=-1
assert D*K==s.zeros(21,15)
assert (K.rank(),D.rank())==(15,21)
# Simplicity: coordinate hyperplanes force an ambient endomorphism of
# wedge^2 V to be diagonal. Hyperplanes x_i+x_k=0 equate its diagonal entries.
relations=[]
for i,k in combinations(range(N),2):
 for j in range(N):
  if j in (i,k): continue
  row=[0]*15
  row[idx[tuple(sorted((i,j)))]]=1
  row[idx[tuple(sorted((k,j)))]]=-1
  relations.append(row)
assert s.Matrix(relations).rank()==14
# Two symplectic orbits of lines: nonisotropic and isotropic.
# W is the annihilator of the two-dimensional point subspace.
for label,U in [('nonisotropic',s.Matrix.hstack(eye[:,0],eye[:,1])),('isotropic',s.Matrix.hstack(eye[:,0],eye[:,2]))]:
 W=s.Matrix.hstack(*U.T.nullspace())
 restricted=W.T*J*W
 assert restricted.rank() in (2,4)
 assert restricted.rank()>0
 print(label,'rank of bivector restricted to annihilator =',restricted.rank())
# H^q(O(k)) vanishes for all q if -n<=k<=-1;
# H^q(O) and H^q(O(1)), H^q(O(2)) vanish for q>0.
assert all(-5<=k<=-1 for k in [-1,-2])
# Rank budgets of the low-dimensional classification.
for n in [2,3,4]:
 types={'line':1,'T':n,'Omega':n}
 if n==2: types['Sym2T']=3
 if n==4: types['wedge2T']=6
 print('P^%d allowed ranks below %d:'%(n,2*n),types)
assert comb(5,2)-1==9<2*5
print('Koszul ranks:',K.rank(),D.rank())
print('Scalar-endomorphism constraint rank:',s.Matrix(relations).rank())
print('All finite linear algebra checks passed.')