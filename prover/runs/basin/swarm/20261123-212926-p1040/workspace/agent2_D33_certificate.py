"""Exact elementary certificate (3,3) belongs to D.
No unproved IA presentation is used. See companion proof text for ping-pong.
"""
from itertools import product

def red(w):
    a=[]
    for x in w:
        if a and a[-1]==-x:a.pop()
        else:a.append(x)
    return tuple(a)
def inv(w):return tuple(-x for x in w[::-1])
def cat(*ws):return red(x for w in ws for x in w)
def comm(u,v):return cat(u,v,inv(u),inv(v))
unit=((1,),(2,),(3,))
# LEFT Magnus generators, C-first.
names=[('C',1,2),('C',1,3),('C',2,1),('C',2,3),('C',3,1),('C',3,2),('M',1,2,3),('M',2,1,3),('M',3,1,2)]
def gen(g,s=1):
    A=list(unit);typ,i,*leaf=g
    if typ=='C':j=leaf[0];A[i-1]=(s*j,i,-s*j)
    else:
        j,k=leaf;c=comm((j,),(k,));A[i-1]=cat(c if s==1 else inv(c),(i,))
    return tuple(A)
def compose(A,B):
    Ai=[inv(w) for w in A]
    return tuple(cat(*(A[x-1] if x>0 else Ai[-x-1] for x in w)) for w in B)
def evaluate(w):
    A=unit
    for x in w:A=compose(A,gen(names[abs(x)-1],1 if x>0 else -1))
    return A

def mul(a,b,N):
    c={}
    for u,x in a.items():
        for v,y in b.items():
            if len(u)+len(v)<=N:c[u+v]=c.get(u+v,0)+x*y
    return {u:c for u,c in c.items() if c}
def magnus(w,N):
    a={():1}
    for x in w:
        i=abs(x)-1;b={():1,(i,):1} if x>0 else {tuple([i]*k):(-1)**k for k in range(N+1)}
        a=mul(a,b,N)
    return a

def mm(A,B,p=None):
    n=len(A);C=tuple(tuple(sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)) for i in range(n))
    return tuple(tuple(x%p for x in r) for r in C) if p else C
def eye(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def inverse2(A):
    a,b=A[0];c,d=A[1];det=a*d-b*c;assert abs(det)==1
    return ((d//det,-b//det),(-c//det,a//det))
def fox(w,t=(1,-1,1)):
    out=[0,0,0];pre=1
    for x in w:
        i=abs(x)-1
        if x>0:out[i]+=pre;pre*=t[i]
        else:pre*=t[i];out[i]-=pre
    return out

def psi(A):
    J=[fox(w) for w in A]
    # Fundamental Fox identity implies span(row e1,row e3) invariant.
    assert J[0][1]==J[2][1]==0
    return inverse2(tuple(tuple(J[i][j] for j in (0,2)) for i in (0,2)))

def matword(w,images,p=None):
    n=len(images[0]);A=eye(n)
    for x in w:
        B=images[abs(x)-1]
        if x<0:
            if p==2:
                # UT4 exponent divides4 or8; inverse finite geometric series.
                N=tuple(tuple((B[i][j]-int(i==j))%2 for j in range(n)) for i in range(n));P=eye(n);C=eye(n)
                for k in range(1,n):
                    P=mm(P,N,2);C=tuple(tuple((C[i][j]+P[i][j])%2 for j in range(n)) for i in range(n))
                B=C
            else:B=inverse2(B)
        A=mm(A,B,p)
    return A

def transvection(i,j):
    A=[list(r) for r in eye(4)];A[i][j]=1;return tuple(map(tuple,A))

if __name__=='__main__':
    W=comm(comm((9,),(7,)),(1,))
    A=evaluate(W)
    assert A!=unit
    for i,w in enumerate(A,1):assert magnus(cat(w,(-i,)),4)=={():1}
    P=[psi(gen(g)) for g in names]
    D=((-1,0),(0,1));U=((1,2),(0,1));V=((1,0),(-2,1));negD=((1,0),(0,-1))
    assert P==[D,eye(2),eye(2),eye(2),eye(2),negD,U,eye(2),V]
    assert psi(A)==matword(W,P)
    a=transvection(0,1);b=transvection(1,2);c=transvection(2,3)
    R=[a,eye(4),eye(4),eye(4),eye(4),a,mm(b,a,2),eye(4),mm(c,a,2)]
    result=matword(W,R,2)
    assert result==transvection(0,3)
    print('W=',W)
    print('Exact Aut image lengths',[len(w) for w in A])
    print('W acts trivially modulo gamma5(F3): VERIFIED by degree4 Magnus expansion')
    print('Fox homomorphism generator matrices:',P)
    print('Class3 UT4(F2) image of W:',result)
    print('CERTIFIED (3,3) in D; target gamma4 is trivial, W image is nontrivial')
