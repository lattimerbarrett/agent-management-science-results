from sage.all import ZZ, QQ, matrix, graphs, lcm
from collections import Counter
import math, json, time

def data(n,mask):
    L=matrix(ZZ,n,n)
    k=0
    for i in range(n):
        for j in range(i+1,n):
            if (mask>>k)&1:
                L[i,i]+=1;L[j,j]+=1
                L[i,j]-=1;L[j,i]-=1
            k+=1
    d=[L[i,i] for i in range(n)]
    T=L[1:,1:].det()
    F=L[2:,2:].det() if n>2 else ZZ(1)
    h=1//(int(T)+1)
    r=1//(1+sum(int(x-d[0])**2 for x in d))
    return QQ(d[0]*F*r*(1-h))/(T+h)

def ilog(b,x):
    e=int((x.nbits()-1)/math.log2(int(b)))
    while b**e>x:e-=1
    while b**(e+1)<=x:e+=1
    assert b**e<=x<b**(e+1)
    return e

def literal(n):
    D=n**(n-2)
    Q=lcm(range(1,D+1))
    b=ZZ(2)**(n*(n-1)//2)+1
    coeff=Counter()
    for mask in range(int(b)-1):
        q=Q*data(n,mask)
        assert q.denominator()==1
        coeff[ZZ(q)]+=1
    S=sum(ZZ(c)*b**q for q,c in coeff.items())
    ans=QQ(n)*ilog(b,S)/Q
    return ans,{str(q):c for q,c in coeff.items()}

st=time.time()
for n in [2,3,4]:print('literal',n,literal(n),flush=True)
print('literal time',time.time()-st,flush=True)

n=10
saved=[]
for d in range((n-1)//2+1):
    for G in graphs(n,degree_sequence=[d]*n):
        saved.append((d,list(G.edges(labels=False))))
records={}
checks=0
for d,edges in saved:
    for comp in [False,True]:
        dd=n-1-d if comp else d
        E={tuple(sorted(e)) for e in edges}
        if comp:E={(i,j) for i in range(n) for j in range(i+1,n)}-E
        L=matrix(QQ,n,n)
        for i,j in E:
            L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
        C=L[:n-1,:n-1];T=C.det()
        if T==0:continue
        P=C.inverse()
        R=matrix(QQ,n,n)
        for i in range(n):
            for j in range(i+1,n):
                R[i,j]=R[j,i]=(P[i,i] if i<n-1 else 0)+(P[j,j] if j<n-1 else 0)-(2*P[i,j] if j<n-1 else 0)
                I=[v for v in range(n) if v not in [i,j]]
                F=L.matrix_from_rows_and_columns(I,I).det()
                assert R[i,j]==F/T
                checks+=1
        H=matrix(QQ,n,n)
        for t in range(n):
            I=[v for v in range(n) if v!=t]
            h=L.matrix_from_rows_and_columns(I,I).solve_right(matrix(QQ,n-1,1,[dd]*(n-1)))
            for k,v in enumerate(I):H[v,t]=h[k,0]
        assert H+H.transpose()==n*dd*R
        val=max(n*dd*x for x in R.list())
        count,old=records.get(dd,(0,QQ(0)))
        records[dd]=(count+1,max(old,val))
print('n10:',sorted(records.items()))
print('pair checks',checks,'total time',time.time()-st)
