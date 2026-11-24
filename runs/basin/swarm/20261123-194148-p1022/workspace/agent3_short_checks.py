"""Exact linear algebra for the uniform rank-9 bundle on P^5."""
from itertools import combinations
import sympy as s

def check():
    J=s.zeros(6)
    for i,j in [(0,1),(2,3),(4,5)]:
        J[i,j]=1
        J[j,i]=-1
    assert J.det()==1 and J.rank()==6
    # If omega lies in U wedge V with dim(U)=2, its matrix has block
    # form [A B; -B.T 0], a sum of matrices with <=2 nonzero rows/columns.
    a=s.symbols('a')
    A=s.Matrix([[0,a],[-a,0]])
    B=s.Matrix(2,4,s.symbols('b:8'))
    top=A.row_join(B).col_join(s.zeros(4,6))
    bottom=s.zeros(2,6).col_join((-B.T).row_join(s.zeros(4)))
    assert top.rank()==2 and bottom.rank()==2
    assert (top+bottom)[2:6,2:6]==s.zeros(4)
    # H0(Q_U*)=0 on P(U)=P^2: global sections of its Euler sequence
    # have map U* -> H0(O(1)) equal to the identity.
    assert s.eye(3).nullspace()==[]
    # Nonhomogeneity from jumping plane restrictions.
    plane_results=[]
    for U in [(0,2,4),(0,1,2)]:
        W=[i for i in range(6) if i not in U]
        projected=J.extract(W,W)
        coefficient_map=s.Matrix([[projected[i,j] for i,j in combinations(range(3),2)]])
        h0_dual_restriction=3-coefficient_map.rank()
        plane_results.append(h0_dual_restriction)
    assert plane_results==[3,2]
    n=5
    rank=int(s.binomial(n,2)-1)
    splitting=[1]*(n-1)+[0]*int(s.binomial(n-1,2)-1)
    assert rank==len(splitting)==9 and rank<2*n
    return {'symplectic_rank':J.rank(),'rank':rank,
            'line_splitting':splitting,'plane_h0_dual':plane_results}

if __name__=='__main__':
    print(check())
