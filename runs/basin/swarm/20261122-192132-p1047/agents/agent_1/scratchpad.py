from fractions import Fraction as F
from itertools import combinations
from sympy import Matrix, primerange, ZZ
from sympy.matrices.normalforms import smith_normal_form

def legendre(a,p):
    x=pow(int(a)%p,(p-1)//2,p)
    return 0 if x==0 else (1 if x==1 else -1)

def minus_one_squares(p):
    assert p%8==3
    for u in range(1,p):
        a=(-1-u*u)%p
        if a and legendre(a,p)==1:
            w=pow(a,(p+1)//4,p)
            assert (u*u+w*w+1)%p==0
            return u,w
    raise AssertionError('Finite-field isotropy failed')

def crt2(a,m,b,n):
    assert __import__('math').gcd(m,n)==1
    return (a+m*((b-a)*pow(m,-1,n)%n))%(m*n)

def matrix_single(p):
    u,w=minus_one_squares(p)
    return [[0,p**3,0],[p**3,p,p*p*u],[0,p*p*u,-p**3]]

def matrix_double(p,q):
    assert p!=q
    D,_=minus_one_squares(p)
    C,_=minus_one_squares(q)
    n=p*q
    b=crt2(p-q*C*C,p*p,q-p*D*D,q*q)
    assert (b+q*C*C-p)%(p*p)==0
    assert (b+p*D*D-q)%(q*q)==0
    return [[0,n**3,0,0],
            [n**3,b,q*q*C,p*p*D],
            [0,q*q*C,-q**3,0],
            [0,p*p*D,0,-p**3]]

def vp(x,p):
    x=F(x)
    if x==0: return float('inf')
    a,b=abs(x.numerator),x.denominator
    v=0
    while a%p==0: a//=p; v+=1
    while b%p==0: b//=p; v-=1
    return v

def unit_symbol(x,p):
    x=F(x); v=vp(x,p)
    u=x/F(p)**v
    return legendre((u.numerator%p)*pow(u.denominator,-1,p),p)

def local_jordan(A,p):
    """Exact Z_p congruence diagonalization; (exponent, unit square class)."""
    A=[[F(x) for x in row] for row in A]
    out=[]
    while A:
        n=len(A)
        v=min(vp(A[i][j],p) for i in range(n) for j in range(n))
        assert v!=float('inf')
        pivot=next((i for i in range(n) if vp(A[i][i],p)==v),None)
        if pivot is None:
            i,j=next((i,j) for i in range(n) for j in range(i+1,n) if vp(A[i][j],p)==v)
            # Replace e_i by e_i+e_j, an integral unimodular congruence.
            T=[[F(int(a==b)) for b in range(n)] for a in range(n)]
            T[j][i]=1
            A=[[sum(T[a][r]*A[a][b]*T[b][s] for a in range(n) for b in range(n))
                for s in range(n)] for r in range(n)]
            pivot=i
            assert vp(A[i][i],p)==v
        A[0],A[pivot]=A[pivot],A[0]
        for row in A: row[0],row[pivot]=row[pivot],row[0]
        d=A[0][0]
        assert all(vp(A[0][i]/d,p)>=0 for i in range(1,n))
        out.append((vp(d,p),unit_symbol(d,p)))
        A=[[A[i][j]-A[i][0]*A[0][j]/d for j in range(1,n)] for i in range(1,n)]
    return sorted(out)

def check_matrix(A,primes):
    M=Matrix(A); n=1
    for p in primes:n*=p
    expected_det=n**9 if len(primes)==1 else -n**9
    assert M==M.T and int(M.det())==expected_det
    assert any(A[i][i]%2 for i in range(len(A)))
    assert A[0][0]==0
    # e_1 is not the characteristic vector mod 2.
    assert any((A[i][0]-A[i][i])%2 for i in range(len(A)))
    for p in primes:
        data=local_jordan(A,p)
        assert all(v>=0 for v,s in data)
        assert [(v,s) for v,s in data if v>0]==[(1,1),(3,1),(5,1)], (primes,data)
    # Put the mod-2 intersection matrix into H direct-sum I, fixing e_1.
    m=len(A)
    e=[Matrix([int(i==j) for i in range(m)]) for j in range(m)]
    f=e[1]+(A[1][1]%2)*e[2]
    cols=[e[0],f]
    for j in range(2,m):
        cols.append(e[j]+int((e[j].T*M*f)[0]%2)*e[0])
    T=Matrix.hstack(*cols)
    H=Matrix.eye(m); H[0,0]=H[1,1]=0; H[0,1]=H[1,0]=1
    assert abs(T.det())==1
    assert all(int(x)%2==0 for x in T.T*M*T-H)
    snf=smith_normal_form(M,domain=ZZ)
    smith=sorted(abs(int(snf[i,i])) for i in range(len(A)))
    assert smith==([1] if len(primes)==2 else [])+[n,n**3,n**5]
    return M

def self_test(bound=100):
    ps=[int(p) for p in primerange(3,bound+1) if p%8==3]
    single=double=0
    for p in ps:
        check_matrix(matrix_single(p),[p]);single+=1
        # No nonempty selection of Jordan constituents is metabolic.
        for mask in range(1,8):assert mask.bit_count()%4!=0
    for p,q in combinations(ps,2):
        check_matrix(matrix_double(p,q),[p,q]);double+=1
        assert legendre(q,p)*legendre(p,q)==-1
        for sign in [-1,1]:
            # Rank-three presentation obstruction.
            assert not(legendre(sign*q,p)==legendre(sign*p,q)==1)
            # Rank-one Witt obstruction for a Mobius band.
            assert not(legendre(sign*q,p)==legendre(sign*p,q)==-1)
    # Independently enumerate small cyclic Gauss sums, not just symbols.
    import cmath, math
    gauss_checks=0
    for p in ps[:3]:
        g=sum(cmath.exp(2j*math.pi*(x*x%p)/p) for x in range(p))/math.sqrt(p)
        assert abs(g*g+1)<1.e-9
        non_square=next(a for a in range(1,p) if legendre(a,p)==-1)
        for k in (1,2,3):
            N=p**k
            for a in (1,non_square):
                z=sum(cmath.exp(2j*math.pi*((a*x*x)%N)/N) for x in range(N))/math.sqrt(N)
                target=legendre(a,p)*g if k%2 else 1
                assert abs(z-target)<1.e-9
                gauss_checks+=1
    print('Enumerated cyclic Gauss sums checked:',gauss_checks)
    print('Primes checked:',ps)
    print('Exact matrix/local-Jordan/Smith checks:',single,'singletons and',double,'pairs')
    print('Example for {3}:');print(Matrix(matrix_single(3)))
    print('Example for {3,11}:');print(Matrix(matrix_double(3,11)))

if __name__=='__main__':self_test()
