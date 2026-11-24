"""Faber--Zagier relation rank in codimension 12, genus 25, exact finite field."""
from math import factorial
from collections import Counter
import json
P=1000000007
N=12

def partitions(n,lo=1):
    if not n:
        yield ()
    for a in range(lo,n+1):
        for b in partitions(n-a,a):
            yield (a,)+b

def mul(a,b):
    c=[0]*(N+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b[:N+1-i]):
            c[i+j]=(c[i+j]+x*y)%P
    return c

def main():
    A=[factorial(6*n)//factorial(3*n)//factorial(2*n)%P for n in range(N+1)]
    B=[a*(6*n+1)*pow(6*n-1,-1,P)%P for n,a in enumerate(A)]
    invA=[1]+[0]*N
    for n in range(1,N+1):
        invA[n]=-sum(A[i]*invA[n-i] for i in range(1,n+1))%P
    D=mul(B,invA)
    powers=[[1]+[0]*N]
    for i in range(10):
        powers.append(mul(powers[-1],D))
    logA=[0]*(N+1)
    for n in range(1,N+1):
        logA[n]=(A[n]-sum(i*logA[i]*A[n-i] for i in range(1,n))*pow(n,-1,P))%P
    F0={}
    for n in range(N+1):
        for mon in partitions(n):
            c=1
            for i,m in Counter(mon).items():
                c=c*pow(-logA[i],m,P)*pow(factorial(m),-1,P)%P
            F0[mon]=c
    sigmas=[s for n in range(11) for s in partitions(n) if all(i%3!=2 for i in s)]
    gamma={}
    for s in sigmas[1:]:
        l=len(s); shift=sum(i//3 for i in s); b=sum(i%3==1 for i in s)
        fac=(-1)**(l+1)*factorial(l-1)
        for m in Counter(s).values():
            fac=fac*pow(factorial(m),-1,P)%P
        gamma[s]=[0]*shift+[fac*x%P for x in powers[b][:N+1-shift]]
    F={():F0}
    for s in sigmas[1:]:
        counts=Counter(s); j=s[0]; out={}
        for tau in sigmas[1:]:
            tc=Counter(tau)
            if not tc[j] or any(v>counts[k] for k,v in tc.items()):
                continue
            rem=tuple(sorted((counts-tc).elements()))
            for mon,c in F[rem].items():
                for n in range(N+1-sum(mon)):
                    a=gamma[tau][n]
                    if not a:
                        continue
                    dest=tuple(sorted(mon+(n,))) if n else mon
                    out[dest]=(out.get(dest,0)-c*a*tc[j]*(48 if n==0 else 1))%P
        F[s]={m:c*pow(counts[j],-1,P)%P for m,c in out.items() if c}
    mons=list(partitions(N)); ix={m:i for i,m in enumerate(mons)}
    rows=[];labels=[]
    for r in range(1,N+1):
        for s in sigmas:
            if 24+sum(s)>=3*r or (25-r-sum(s)-1)%2:
                continue
            for extra in partitions(N-r):
                row=[0]*len(mons)
                for mon,c in F[s].items():
                    if sum(mon)==r:
                        row[ix[tuple(sorted(mon+extra))]]=c
                rows.append(row);labels.append([r,list(s),list(extra)])
    basis={};selected=[]
    for i,row0 in enumerate(rows):
        row=row0[:]
        for j in range(len(row)):
            c=row[j]
            if not c:
                continue
            if j in basis:
                row=[(a-c*b)%P for a,b in zip(row,basis[j])]
            else:
                basis[j]=[a*pow(c,-1,P)%P for a in row]
                selected.append(i)
                break
    print('prime:',P,'monomials:',len(mons),'rows:',len(rows),'rank:',len(basis))
    assert len(mons)==77 and len(rows)==59 and len(basis)==33
    return dict(prime=P,monomials=mons,rows=rows,labels=labels,selected=selected)
if __name__=='__main__':
    data=main()
