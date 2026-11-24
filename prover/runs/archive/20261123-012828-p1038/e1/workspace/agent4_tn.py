"""Exact checks of the axial total-nonnegativity and Laplace lemmas."""
from fractions import Fraction as F
from itertools import combinations

def det(A):
    A=[list(r) for r in A];n=len(A);out=F(1)
    for k in range(n):
        if not A[k][k]:
            p=next((j for j in range(k+1,n) if A[j][k]),None)
            if p is None:return F(0)
            A[k],A[p]=A[p],A[k];out=-out
        a=A[k][k];out*=a
        for j in range(k+1,n):
            c=A[j][k]/a
            for l in range(k+1,n):A[j][l]-=c*A[k][l]
    return out

def matrix(u,v,signed=False):
    k=len(u);A=[[F(0)]*(k+2) for i in range(k)]
    for i,(x,y) in enumerate(zip(u,v)):
        A[i][i]=F(1);A[i][i+1]=(-1 if signed else 1)*(x+y);A[i][i+2]=x*y
    return A

def factor(u,v):
    k=len(u);w=[F(0)];z=[]
    for x,y in zip(u,v):
        assert w[-1]<=x
        z.append(x+y-w[-1]);w.append(x*y/z[-1])
    B=[[F(int(i==j))+(z[i] if j==i+1 else 0) for j in range(k+1)] for i in range(k)]
    C=[[F(int(i==j))+(w[i] if j==i+1 else 0) for j in range(k+2)] for i in range(k+1)]
    assert [[sum(B[i][t]*C[t][j] for t in range(k+1)) for j in range(k+2)] for i in range(k)]==matrix(u,v)
    return B,C

def check():
    checked=0
    for k in range(1,8):
        u=[F((i+1)**2,17) for i in range(k)]
        v=[F(3*(i+1)+1,19) for i in range(k)]
        factor(u,v);P=matrix(u,v);Q=matrix(u,v,True)
        for size in range(1,k+1):
            for rr in combinations(range(k),size):
                for cc in combinations(range(k+2),size):
                    assert det([[P[i][j] for j in cc] for i in rr])>=0
                    checked+=1
        A=[F((i+3)**2,7) for i in range(k+2)]
        B=[F((i+1)**3,13) for i in range(k+2)]
        expanded=F(0)
        for i,j in combinations(range(k+2),2):
            cols=[l for l in range(k+2) if l not in (i,j)]
            weight=det([[P[t][l] for l in cols] for t in range(k)])
            expanded+=weight*(A[i]*B[j]-A[j]*B[i])
        assert det(Q+[A,B])==expanded
    return checked

if __name__=='__main__':print('Exact rational minors/Laplace checks:',check())


def maximal_minor(u,v,i,j):
    """Positive explicit formula for the minor omitting columns i,j."""
    k=len(u);prev,cur=F(0),F(1)
    for t in range(j-2,i-1,-1):
        prev,cur=cur,(u[t]+v[t])*cur-u[t]*v[t]*prev
    for t in range(j-1,k):cur*=u[t]*v[t]
    return cur

def check_maximal():
    count=0
    for k in range(1,15):
        u=[F((i+1)**2,17) for i in range(k)]
        v=[F(3*(i+1)+1,19) for i in range(k)]
        P=matrix(u,v)
        for i,j in combinations(range(k+2),2):
            val=maximal_minor(u,v,i,j);lo=F(1)
            for t in range(i,j-1):lo*=max(u[t],v[t])
            for t in range(j-1,k):lo*=u[t]*v[t]
            cc=[c for c in range(k+2) if c not in (i,j)]
            assert val==det([[P[t][c] for c in cc] for t in range(k)])
            assert val>=lo>0
            count+=1
    return count
