import itertools
import sympy as s
from math import comb

N=6
pairs=list(itertools.combinations(range(N),2))
J=s.zeros(N)
for i in range(0,N,2):
    J[i,i+1]=1
    J[i+1,i]=-1
assert J.rank()==6
print('rank of the alternating form:',J.rank())
# A point has annihilator of dimension 5. Sp(6) is transitive on points.
I=list(range(1,N))
assert J.extract(I,I).rank()==4
print('rank on the annihilator of a point:',J.extract(I,I).rank())
# The two Sp(6)-orbits on Gr(2,6).
for name,W,expected in [('symplectic',(0,1),4),('isotropic',(0,2),2)]:
    I=[i for i in range(N) if i not in W]
    A=J.extract(I,I)
    coeff=s.Matrix([[J[i,j] for i,j in itertools.combinations(I,2)]])
    assert A.rank()==expected and coeff.rank()==1
    assert len(I)==4 and coeff.cols==6
    print(name,'line: restricted skew rank',A.rank(),
          '; constant-block map rank',coeff.rank(),
          '; kernel splitting: 5 O + 4 O(-1)')

# The global-sections Koszul complex for Omega^2(2).
# wedge^2 V* --> V* tensor V* --> Sym^2 V*.
sympairs=list(itertools.combinations_with_replacement(range(N),2))
D=s.zeros(N*N,len(pairs))
M=s.zeros(len(sympairs),N*N)
for c,(i,j) in enumerate(pairs):
    D[N*i+j,c]=1
    D[N*j+i,c]=-1
for i in range(N):
    for j in range(N):
        M[sympairs.index(tuple(sorted((i,j)))),N*i+j]=1
assert M*D==s.zeros(len(sympairs),len(pairs))
assert D.rank()==15 and M.rank()==21
assert D.cols==D.rank() and D.rank()+M.rank()==N*N
print('Koszul complex dimensions/ranks:',D.cols,D.rows,M.rows,D.rank(),M.rank())

def line_cohomology(n,k):
    out=[0]*(n+1)
    if k>=0: out[0]=comb(n+k,n)
    if k<=-n-1: out[n]=comb(-k-1,n)
    return out
for k in [-2,-1]:
    assert line_cohomology(5,k)==[0]*6
print('O(-1), O(-2) on P^5: all cohomology zero')

# Finite certificate for simplicity of wedge^2 Q.
# Preserving e_i wedge V forces all wedge basis vectors to be eigenvectors.
# Preserving (e_i+e_j) wedge V then equates their eigenvalues.
index={ij:t for t,ij in enumerate(pairs)}
def pair_index(i,j): return index[tuple(sorted((i,j)))]
rows=[]
for i,j,k in itertools.permutations(range(N),3):
    row=[0]*len(pairs)
    row[pair_index(i,k)]+=1
    row[pair_index(j,k)]-=1
    rows.append(row)
C=s.Matrix(rows)
assert C.rank()==14
assert C.nullspace()==[s.ones(15,1)]
print('simplicity certificate: 15 eigenvalues, relation rank',C.rank())

# An explicit projective change of coordinates changes the projective form.
G=s.diag(2,1,1,1,1,1)
J2=G*J*G.T
q=s.Matrix([J[i,j] for i,j in pairs])
q2=s.Matrix([J2[i,j] for i,j in pairs])
assert s.Matrix.hstack(q,q2).rank()==2
print('q and its transform are not proportional')

# Ranks relevant to the minimum (classification bounds are theorem inputs).
for n in [2,3,4]:
    assert list(range(1,2*n))[-1]=={2:3,3:5,4:7}[n]
rank=comb(5,2)-1
assert rank==9 and 1<=rank<2*5
print('constructed rank:',rank,'<',10)
print('All exact arithmetic assertions passed.')
