"""Auxiliary exact checks for the wedge-square construction in dimensions 3--5.
This does not prove the classification of arbitrary uniform bundles.
"""
import sympy as s
from itertools import combinations
from pathlib import Path

def bivector_matrix(m):
    A=s.zeros(m)
    for i in range(0,m-1,2): A[i,i+1]=1; A[i+1,i]=-1
    return A

def wedge_projection_matrix(P):
    n,m=P.shape
    return s.Matrix([[P[a,i]*P[b,j]-P[a,j]*P[b,i]
                      for i,j in combinations(range(m),2)]
                     for a,b in combinations(range(n),2)])

def vec(A):return s.Matrix([A[i,j] for i,j in combinations(range(A.rows),2)])

# If rank omega <=4, choose one coordinate from each symplectic block.
# Its span U meets every term of omega; omega maps to zero in Lambda^2(V/U).
for m in [4,5]:
    A=bivector_matrix(m)
    U=[0,2]
    complement=[i for i in range(m) if i not in U]
    P=s.eye(m)[complement,:]
    assert A.rank()==4
    assert wedge_projection_matrix(P)*vec(A)==s.zeros((m-2)*(m-3)//2,1)
    # This rank-four omega is nowhere zero in Lambda^2(V/l) for coordinate l.
    for j in range(m):
        Pj=s.eye(m)[[i for i in range(m) if i!=j],:]
        assert wedge_projection_matrix(Pj)*vec(A)!=s.zeros((m-1)*(m-2)//2,1)

# In dim6, rank omega=6. A bivector in U wedge V, dim U=2,
# has matrix block form [A B; -B^t 0], so rank <=4.
# Symbolically certify all 5x5 minors vanish for that general block matrix.
a=s.symbols('a')
b=s.symbols('b:8')
M=s.zeros(6);M[0,1]=a;M[1,0]=-a
for i in range(2):
    for j in range(4):M[i,j+2]=b[4*i+j];M[j+2,i]=-b[4*i+j]
for I in combinations(range(6),5):
    for J in combinations(range(6),5):
        assert s.expand(M.extract(I,J).det())==0
assert bivector_matrix(6).det()==1

# Along any line, Q=O(1)+O^(n-1); F=Lambda^2 Q has
# n-1 positive and C(n-1,2) trivial factors.
for n in [3,4,5]:
    F_rank=n*(n-1)//2
    E_rank=F_rank-1
    generic=[1]*(n-1)+[0]*(int(s.binomial(n-1,2))-1)
    assert len(generic)==E_rank and sum(generic)==n-1
    if n in [3,4]:
        jumping=[2]+[1]*(n-3)+[0]*int(s.binomial(n-1,2))
        assert len(jumping)==E_rank and sum(jumping)==n-1
        assert generic!=jumping
        print(f'P^{n}: rank {E_rank}, generic {generic}, jumping {jumping}')
    else:
        assert E_rank<2*n
        print(f'P^{n}: rank {E_rank}, constant splitting {generic}')
print('All exact auxiliary rank/minor/splitting checks passed.')
Path('workspace').mkdir(exist_ok=True)
Path('workspace/agent3_wedge_auxiliary.py').write_text(Path(__file__).read_text())
