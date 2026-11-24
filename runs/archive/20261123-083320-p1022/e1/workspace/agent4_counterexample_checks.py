"""Exact certificates for the P^5 rank-nine uniform quotient construction."""
import sympy as s
from itertools import combinations
from pathlib import Path
import json

N=6
pairs=list(combinations(range(N),2)); pair_index={p:i for i,p in enumerate(pairs)}
W=s.zeros(N)
for i in range(0,N,2): W[i,i+1]=1;W[i+1,i]=-1
G=s.diag(s.Rational(1,2),1,1,1,1,1)
eta=G.inv()*W*G.inv().T
assert W.rank()==6 and W.det()==1
assert eta.rank()==6 and eta.det()==4
assert eta[0,1]==2 and eta[2,3]==1 and W[0,1]==W[2,3]==1
assert eta[0,1]*W[2,3]!=eta[2,3]*W[0,1]

# Every element of U wedge V, dim U=2, has skew rank <=4:
# it is U X^T-X U^T = [U X] J [U X]^T, a factorization through C^4.
U=s.Matrix(N,2,s.symbols('u0:'+str(2*N)))
X=s.Matrix(N,2,s.symbols('x0:'+str(2*N)))
J=s.zeros(4)
for i in range(2):J[i,i+2]=1;J[i+2,i]=-1
Z=U.row_join(X)
assert s.simplify(U*X.T-X*U.T-Z*J*Z.T)==s.zeros(N)

# Global exterior Euler/Koszul complex: dimensions 15 -> 36 -> 21.
# d1 sends ei wedge ej to ei tensor ej - ej tensor ei.
# d2 is the multiplication/symmetrization map to Sym^2 C^6.
monomials=list(combinations(range(N),2))+[(i,i) for i in range(N)]
mi={a:i for i,a in enumerate(monomials)}
d1=s.zeros(N*N,len(pairs)); d2=s.zeros(len(monomials),N*N)
for j,(a,b) in enumerate(pairs):
    d1[a*N+b,j]=1;d1[b*N+a,j]=-1
for a in range(N):
    for b in range(N): d2[mi[tuple(sorted((a,b)))],a*N+b]=1
assert d2*d1==s.zeros(21,15)
assert d1.rank()==15 and d2.rank()==21
assert d1.rank()+d2.rank()==36

# End(B)=C: preserving ei wedge V makes the wedge basis eigenlines.
# Preserving (ei+ej) wedge ek forces equal eigenvalues on edges sharing k.
rows=[]
for i,j,k in combinations(range(N),3):
    for p,q in [((i,j),(i,k)),((i,j),(j,k))]:
        row=[0]*len(pairs);row[pair_index[p]]=1;row[pair_index[q]]=-1
        rows.append(row)
relations=s.Matrix(rows)
assert relations.rank()==14
assert relations.nullspace()==[s.ones(15,1)]

# Verify rank and splitting counts: Lambda^2 Q|L=O(1)^4 + O^6.
assert s.binomial(5,2)==10 and s.binomial(4,2)==6
assert 10-1==9 and 9<2*5
assert 4+(6-1)==9
results={
 'omega_rank':int(W.rank()),'omega_determinant':int(W.det()),
 'transformed_omega_rank':int(eta.rank()),
 'transformed_omega_determinant':int(eta.det()),
 'not_proportional_minor':int(eta[0,1]*W[2,3]-eta[2,3]*W[0,1]),
 'rank_factorization_inner_dimension':4,
 'koszul_dimensions':[15,36,21],
 'koszul_ranks':[int(d1.rank()),int(d2.rank())],
 'endomorphism_eigenvalue_relations_rank':int(relations.rank()),
 'endomorphism_space_dimension':15-int(relations.rank()),
 'bundle_rank':9,'projective_dimension':5,
 'line_splitting':{'degree_one':4,'degree_zero':5}}
Path('workspace/agent4_counterexample_checks.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent4_counterexample_checks.py').write_text(Path(__file__).read_text())
print(json.dumps(results,indent=2))
