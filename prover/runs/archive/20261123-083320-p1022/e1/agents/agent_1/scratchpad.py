"""Exact certificates for a uniform, non-PGL-homogeneous rank-9 bundle on P^5.
The geometry is proved separately; this script checks the finite linear algebra.
"""
import sympy as s
import itertools as it
import json
from pathlib import Path

N=6
pairs=list(it.combinations(range(N),2))
J=s.zeros(N)
for i,j in [(0,1),(2,3),(4,5)]:
    J[i,j]=1; J[j,i]=-1
assert J.det()==1 and J.rank()==6

# Every tensor in U wedge V, dim U=2, has skew rank <=4.
# This is the GENERAL such skew matrix in a basis adapted to U.
a=s.symbols('a')
b=s.symbols('b0:8')
M=s.zeros(6);M[0,1]=a;M[1,0]=-a
for i in range(2):
 for j in range(2,6):
  M[i,j]=b[4*i+j-2];M[j,i]=-M[i,j]
minors=0
for rows in it.combinations(range(6),5):
 for cols in it.combinations(range(6),5):
  assert s.expand(M.extract(rows,cols).det())==0
  minors+=1
assert minors==36

# Simplicity: preserving each ell wedge V first makes T diagonal
# on basis wedges; ell=e_i+e_k then equates any two eigenvalues
# whose index-pairs share an index. Check all constraints have rank14.
rows=[]
for pidx,p in enumerate(pairs):
 for qidx,q in enumerate(pairs):
  if pidx<qidx and len(set(p)&set(q))==1:
   row=[0]*len(pairs);row[pidx]=1;row[qidx]=-1;rows.append(row)
C=s.Matrix(rows)
assert C.rank()==14 and len(C.nullspace())==1
assert C*s.ones(15,1)==s.zeros(C.rows,1)

# Global sections of the exterior Euler resolution:
# 0 -> wedge^2 V* -> V* tensor V* -> Sym^2 V* -> 0.
sympairs=list(it.combinations_with_replacement(range(6),2))
I=s.zeros(36,15);A=s.zeros(21,36)
for col,(i,j) in enumerate(pairs):
 I[6*i+j,col]=1;I[6*j+i,col]=-1
for i in range(6):
 for j in range(6):
  A[sympairs.index(tuple(sorted((i,j)))),6*i+j]=1
assert I.rank()==15 and A.rank()==21 and A*I==s.zeros(21,15)
assert 36==15+21

# A concrete projective automorphism changes the recovered section.
G=s.diag(2,1,1,1,1,1)
Jprime=G.inv()*J*G.inv().T
assert Jprime.rank()==6
assert Jprime[0,1]==s.Rational(1,2) and Jprime[2,3]==1
assert Jprime!=Jprime[2,3]*J

# Optional Chern-class cross-check. E=B/O and B=wedge^2Q.
h=s.symbols('h')
ch=s.series(14-6*s.exp(-h)+s.exp(-2*h),h,0,6).removeO()
c=[s.Integer(1)]
for k in range(1,6):
 c.append(s.simplify(sum((-1)**(j-1)*s.factorial(j)*ch.coeff(h,j)*c[k-j]
                          for j in range(1,k+1))/k))
assert ch.coeff(h,0)==9 and c==[1,4,9,14,14,0]
result={'rank':9,'base_dimension':5,'uniform_splitting':[1,1,1,1,0,0,0,0,0],
        'symplectic_determinant':int(J.det()),'zero_symbolic_5_minors':minors,
        'scalar_endomorphism_constraint_rank':int(C.rank()),
        'koszul_global_ranks':[int(I.rank()),int(A.rank())],
        'chern_classes':[int(v) for v in c],
        'changed_symplectic_coefficients':['1/2','1','1']}
Path('workspace/agent1_counterexample.py').write_text(Path(__file__).read_text())
Path('workspace/agent1_counterexample_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
print('All exact certificates passed. The geometric proof yields d <= 5, not infinity.')
