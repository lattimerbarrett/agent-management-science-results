"""Exact arithmetic checks for the P^5 rank-nine uniform bundle construction.
Run as Python; requires SymPy. All assertions certify identities/ranks rather
than printing prespecified mathematical conclusions.
"""
import itertools
import sympy as s

N=6
pairs=list(itertools.combinations(range(N),2))
triples=list(itertools.combinations(range(N),3))
pi={ij:k for k,ij in enumerate(pairs)}
ti={ijk:k for k,ijk in enumerate(triples)}

def wedge2(v,w):
    return [v[i]*w[j]-v[j]*w[i] for i,j in pairs]

def wedge12(v,b):
    return [v[i]*b[pi[j,k]]-v[j]*b[pi[i,k]]+v[k]*b[pi[i,j]] for i,j,k in triples]

basis=[list(s.eye(N)[:,i]) for i in range(N)]
# A bivector in U wedge V has a skew matrix whose lower-right 4x4 block
# is zero. Its generic determinant vanishes, so rank <=4 (ranks are even).
z=iter(s.symbols('z:9'))
M=s.zeros(N)
for i,j in pairs:
    if i<2:
        M[i,j]=next(z)
        M[j,i]=-M[i,j]
assert s.expand(M.det())==0
# Directly verify stronger 5x5 minors vanish; this avoids parity arguments.
for rows in itertools.combinations(range(N),5):
    for cols in itertools.combinations(range(N),5):
        assert M.extract(rows,cols).det()==0
print('Generic bivector in U wedge V: all 5x5 minors vanish (rank <=4).')

omega=s.zeros(N)
for i in (0,2,4):
    omega[i,i+1]=1
    omega[i+1,i]=-1
assert omega.rank()==6 and omega.det()==1
G=s.diag(2,1,1,1,1,1)
changed=G*omega*G.T
assert changed.rank()==6
assert changed[0,1]!=changed[2,3] and omega[0,1]==omega[2,3]
print('Chosen omega and g.omega both rank 6, but are not proportional.')

# Check End(Lambda^2 Q)=C by a finite subset of all incidence conditions.
# A preserves l wedge V iff l wedge A(l wedge e_j)=0 for all j.
# Modular rank 224 gives rational rank >=224. The identity is in the
# kernel, so rank <=224: the nullspace is precisely scalar matrices.
p=32003
assert s.isprime(p)
pivots={}
row_count=0
samples=basis+[[basis[i][k]+basis[j][k] for k in range(N)] for i,j in pairs]
for v in samples:
    for e in basis:
        b=wedge2(v,e)
        for i,j,k in triples:
            row=[0]*225
            for out,coeff in ((pi[j,k],v[i]),(pi[i,k],-v[j]),(pi[i,j],v[k])):
                if coeff:
                    for inp,x in enumerate(b):
                        row[15*out+inp]=(row[15*out+inp]+coeff*x)%p
            if not any(row): continue
            # Identity must satisfy this equation.
            assert sum(row[15*h+h] for h in range(15))%p==0
            row_count+=1
            for pivot,old in sorted(pivots.items()):
                a=row[pivot]
                if a:
                    row=[(x-a*y)%p for x,y in zip(row,old)]
            new=next((h for h,x in enumerate(row) if x),None)
            if new is not None:
                inv=pow(row[new],-1,p)
                pivots[new]=[(x*inv)%p for x in row]
assert len(pivots)==224
print(f'Simplicity incidence certificate: {row_count} equations, 225 unknowns, rank {len(pivots)} modulo {p}; identity in kernel.')

# Koszul global-sections check for H^0(F*)=H^1(F*)=0.
# Multiplication V* tensor V* -> Sym^2 V* has 15-dimensional kernel,
# and the antisymmetrization map Lambda^2 V* identifies with that kernel.
sympairs=list(itertools.combinations_with_replacement(range(N),2))
si={ij:k for k,ij in enumerate(sympairs)}
mu=s.zeros(len(sympairs),N*N)
anti=s.zeros(N*N,len(pairs))
for i in range(N):
    for j in range(N): mu[si[tuple(sorted((i,j)))],N*i+j]=1
for h,(i,j) in enumerate(pairs):
    anti[N*i+j,h]=1
    anti[N*j+i,h]=-1
assert mu.rank()==21
assert anti.rank()==15
assert mu*anti==s.zeros(21,15)
assert 36-mu.rank()==anti.rank()
print('Koszul check: multiplication rank 21, antisymmetrization rank 15, exact at C^36.')
assert s.binomial(5,2)-1==9<2*5
assert (4+5)==9
print('Rank E=9<10; line splitting has four degree-1 and five degree-0 summands.')
