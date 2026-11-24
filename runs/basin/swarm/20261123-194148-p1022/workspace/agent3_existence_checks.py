"""Exact checks for the P^5 uniform rank-nine construction.
All arithmetic is over Q, hence valid after extension to C.
The geometric universal statements are proved in the accompanying argument;
these checks verify their finite linear-algebra ingredients.
"""
import itertools
import sympy as s

def check():
    N=6
    pairs=list(itertools.combinations(range(N),2))
    J=s.zeros(N)
    for i,j in [(0,1),(2,3),(4,5)]:
        J[i,j]=1; J[j,i]=-1
    assert J.det()==1 and J.rank()==6
    # A diagonal projectivity moves the projective class of the bivector.
    g=s.diag(2,1,1,1,1,1)
    Jm=g*J*g.T
    assert s.Matrix.hstack(s.Matrix(J).reshape(36,1),s.Matrix(Jm).reshape(36,1)).rank()==2
    # Koszul H^0 complex for Omega^2(2): wedge^2 V* -> V* tensor V* -> Sym^2 V*.
    syms=list(itertools.combinations_with_replacement(range(N),2))
    delta=s.zeros(N*N,len(pairs))
    mult=s.zeros(len(syms),N*N)
    for c,(i,j) in enumerate(pairs):
        delta[i*N+j,c]=1
        delta[j*N+i,c]=-1
    for i in range(N):
        for j in range(N):
            mult[syms.index(tuple(sorted((i,j)))),i*N+j]=1
    assert mult*delta==s.zeros(len(syms),len(pairs))
    assert delta.rank()==15 and mult.rank()==21
    assert delta.cols+mult.rows==N*N
    # End(Lambda^2 Q): preserving e_i wedge V makes every e_i wedge e_j
    # an eigenvector. Preserving (e_i+e_j) wedge e_k equates eigenvalues
    # indexed by edges sharing a vertex. Check all 15 eigenvalues forced equal.
    constraints=[]
    for i,j,k in itertools.permutations(range(N),3):
        row=[0]*len(pairs)
        row[pairs.index(tuple(sorted((i,k))))]=1
        row[pairs.index(tuple(sorted((j,k))))]=-1
        constraints.append(row)
    C=s.Matrix(constraints)
    assert C.rank()==14 and len(C.nullspace())==1
    assert C.nullspace()[0]==s.ones(15,1)
    # The rank obstruction on a line: any bivector in U wedge V for dim U=2
    # has matrix [A B;-B^t 0], with rank at most 2 dim U=4.
    # Universal proof factors this matrix as a sum of two rank <=2 matrices.
    a=s.symbols('a'); b=s.Matrix(2,4,s.symbols('b0:8'))
    A=s.Matrix([[0,a],[-a,0]])
    K=A.row_join(b).col_join((-b.T).row_join(s.zeros(4)))
    Ktop=A.row_join(b).col_join(s.zeros(4,6))
    Kbottom=s.zeros(2,6).col_join((-b.T).row_join(s.zeros(4)))
    assert K==Ktop+Kbottom
    assert Ktop.rank()<=2 and Kbottom.rank()<=2
    assert s.binomial(5,2)-1==9<2*5
    assert (5-1)+(s.binomial(4,2)-1)==9
    return {'ambient_dimension':5,'bundle_rank':9,'symplectic_matrix_rank':6,
            'koszul_ranks':(15,21),'endomorphism_dimension':15-C.rank(),
            'splitting_type':[1]*4+[0]*5}

if __name__=='__main__':
    print(check())
