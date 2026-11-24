from fractions import Fraction
from math import factorial
import numpy as np
import sympy as sp

p=7

def parts(n,lo=1):
    if n==0:
        yield ()
    for a in range(lo,n+1):
        for t in parts(n-a,a):
            yield (a,)+t

def sets(k,delta):
    for part in parts(delta):
        if len(part)>k: continue
        I=list(range(k))
        for j,a in enumerate(part): I[k-len(part)+j]+=a
        yield I

def possible(I,A):
    C=np.bincount(np.array(I)%11,minlength=11)
    D=C-np.array([C[8*s%11] for s in range(11)])
    def edge(a,b):
        t=np.zeros(11,dtype=int)
        t[7*a%11]-=1;t[(7*a-3*b)%11]+=1
        return t
    opts=[]
    for a in range(11):
        if np.array_equal(D,edge(a,A)): opts.append((a,A))
    if A==2:
        for a in range(11):
            for b in range(a,11):
                if np.array_equal(D,edge(a,1)+edge(b,1)):opts.append((a,b,1))
    return opts

def structural_check():
    rows=[]
    for r in range(2,11):
        gap=3*(r-1)*(11-r)
        for A in range(1,4):
            for d in range(13):
                if 6*d+19*A>=gap or (3*r*(r-1)+6*d+19*A)%11:continue
                ok=[]
                for I in sets(22+r,d):
                    opts=possible(I,A)
                    if opts:ok.append((I,opts))
                rows.append((r,A,d,len(ok)))
                if ok:
                    assert A==1 and d==7 and r in (5,7) and len(ok)==1
                    S={5:[0,2,3,5,7],7:[0,1,2,3,5,7,10]}[r]
                    assert ok[0][0]==list(range(22))+[22+s for s in S]
                for I in sets(r,d):
                    opts=possible(I,A)
                    if opts:
                        assert (r,A,d) in ((5,1,7),(7,1,7))
    return rows

def ah(N):
    a=[Fraction(1)]
    powers=[];q=1
    while q<=N:powers.append(q);q*=7
    for k in range(1,N+1):
        a.append(sum((a[k-q] for q in powers if q<=k),Fraction(0))/k)
    return a

def mod7(x):
    return int(x.numerator%7)*pow(int(x.denominator%7),-1,7)%7

def val7(x):
    v=0
    while x and x%7==0:x//=7;v+=1
    return v

def D(m,c):
    out=Fraction(7**(m*(m-1)//2))
    for j in range(1,m):out*=factorial(j)
    for j in range(m):out/=factorial(7*j+c)
    return out

def determinant_checks(a):
    for m in range(1,7):
        for c in range(7):
            mat=sp.Matrix(m,m,lambda i,j:a[7*i-j+c] if 7*i-j+c>=0 else 0)
            assert mat.det()==D(m,c)
            assert mod7(D(m,c))!=0
        def vminor(cols):
            return sp.Matrix(m,m,lambda i,j:a[7*i-cols[j]+5] if 7*i-cols[j]+5>=0 else 0).det()
        v0=vminor(list(range(1,m+1)))
        v1=-vminor([0]+list(range(2,m+1)))
        ratio=Fraction(1)
        for l in range(m):ratio*=Fraction(7*l+4,7*l+5)
        assert v0+v1==v0*ratio
        assert mod7(Fraction(v0+v1))!=0
    for m in range(1,1000):
        for c in range(7):
            # valuation of the product formula, without big factorials
            lhs=m*(m-1)//2+sum(sum(j//(7**h) for h in range(1,6)) for j in range(m))
            rhs=sum(sum((7*j+c)//(7**h) for h in range(1,7)) for j in range(m))
            assert lhs==rhs

def solve_mod(A,b):
    A=np.array(A,dtype=np.int64)%7;b=np.array(b,dtype=np.int64).reshape(-1,1)%7
    M=np.concatenate([A,b],axis=1);n=len(A)
    for k in range(n):
        z=next(i for i in range(k,n) if M[i,k])
        M[[k,z]]=M[[z,k]]
        M[k]=M[k]*pow(int(M[k,k]),-1,7)%7
        for i in range(n):
            if i!=k and M[i,k]:M[i]=(M[i]-M[i,k]*M[k])%7
    return M[:,-1]

def lowered(m,r,n,e):
    if n<=2:return False
    c1,c2,cB={5:(1,0,3),7:(6,5,8)}[r]
    def E(indices):
        indices=np.asarray(indices)
        z=np.zeros(indices.shape,dtype=np.int64)
        mask=indices>=0;z[mask]=e[indices[mask]]
        return z
    L=np.arange(m+1)[:,None]; H=np.arange(m+1)[None,:]
    U=E(7*L-H[:,:m]+c1)
    V=E(7*L[:m]-H+c2)
    if m:
        u=np.r_[solve_mod(U[:m].T,-U[m]),1]
        v=np.r_[solve_mod(V[:,:m],-V[:,m]),1]
    else:u=v=np.array([1],dtype=np.int64)
    B=sum((E(7*L-H+cB-7**j) for j in range(2,n)),np.zeros((m+1,m+1),dtype=np.int64))%7
    return bool(int(u@B@v)%7)

def P(k):
    m,r=divmod(k,11)
    if r==0:return 33*m*m-3*m
    return 33*m*m+3*m+(6*m+3)*(r-1)

def hull(points):
    h=[]
    for point in points:
        while len(h)>=2:
            a,b=h[-2:];c=point
            if (b[1]-a[1])*(c[0]-b[0]) >= (c[1]-b[1])*(b[0]-a[0]):h.pop()
            else:break
        h.append(point)
    return h

def block(m,n,e):
    ks=[11*m+1,11*m+5,11*m+7,11*m+11]
    return hull([(k,P(k)-int(r in (5,7) and lowered(m,r,n,e))) for k,r in zip(ks,[1,5,7,11])])

if __name__=='__main__':
    print('structural table:',structural_check())
    a=ah(410);e=np.array([mod7(x) for x in a],dtype=np.int64)
    determinant_checks(a)
    print('exact determinant and valuation checks passed')
    for n in (2,3):
        M=7**(n-1)
        first=None
        for m in range(M):
            h0=block(m,n,e);h1=block(m,n+1,e)
            if h0!=h1:
                first=h0[0][0]
                print('n=',n,'first differing block=',m,'old hull=',h0,'new hull=',h1)
                break
        assert first==11*M-10
    print('R_1=infinity; checked R_2=67 and R_3=529 by finite-field determinant computations')
