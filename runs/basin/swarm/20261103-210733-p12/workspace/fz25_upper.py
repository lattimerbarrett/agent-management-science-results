from fractions import Fraction as Q
from functools import lru_cache
from math import factorial, comb
from collections import defaultdict, Counter
import json, os

@lru_cache(None)
def partitions(n, top=None):
    if top is None or top>n: top=n
    if n==0: return ((),)
    return tuple((a,)+p for a in range(top,0,-1) for p in partitions(n-a,a))

D=12; g=25; k0=2*g-2
A=[factorial(6*n)//(factorial(3*n)*factorial(2*n)) for n in range(D+1)]
B=[Q(A[n]*(6*n+1),6*n-1) for n in range(D+1)]
@lru_cache(None)
def kap(p):
    # positive K-indices; sum over permutations, products over cycles
    if not p:return {():1}
    a,*rest=p
    ct=Counter(rest); keys=list(ct)
    out=defaultdict(int)
    def rec(i,chosen,left,mult,total,size):
        if i==len(keys):
            fac=mult*factorial(size)
            for mon,c in kap(tuple(sorted(left,reverse=True))).items():
                out[tuple(sorted(mon+(a+total,),reverse=True))]+=fac*c
            return
        b=keys[i]; m=ct[b]
        for j in range(m+1):rec(i+1,chosen,left+[b]*(m-j),mult*comb(m,j),total+b*j,size+j)
    rec(0,[],[],1,0,0)
    return dict(out)

# exp({1-A}) represented by indices of K, including 0 if present.
base={p:Q((-1)**len(p))*__import__('functools').reduce(lambda a,n:a*A[n],p,1)/__import__('functools').reduce(lambda a,m:a*factorial(m),Counter(p).values(),1) for n in range(D+1) for p in partitions(n)}

def rel(r,sigma):
    pol={p:c for p,c in base.items() if sum(p)<=r}
    for s in sigma:
        shift=s//3; coeff=A if s%3==0 else B
        out=defaultdict(Q)
        for p,c in pol.items():
            for n in range(shift,r-sum(p)+1):
                out[tuple(sorted(p+(n,),reverse=True))]+=c*coeff[n-shift]
        pol=out
    ans=defaultdict(Q)
    for p,c in pol.items():
        if sum(p)!=r:continue
        z=p.count(0); pos=tuple(x for x in p if x)
        for j in range(z):c*=k0+len(pos)+j
        for q,d in kap(pos).items():ans[q]+=c*d
    return dict(ans)

rows=[]; labels=[]
for r in range(1,D+1):
    for sz in range(3*r-g):
        if (3*r-g-1-sz)%2:continue
        for sigma in partitions(sz):
            if any(s%3==2 for s in sigma):continue
            v=rel(r,sigma)
            for extra in partitions(D-r):
                rows.append({tuple(sorted(p+extra,reverse=True)):c for p,c in v.items()})
                labels.append((r,sigma,extra))
basis=partitions(D)
mat=[[row.get(p,0) for p in basis] for row in rows]
print('basis',len(basis),'rows',len(rows),flush=True)
import sympy as sp
M=sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(mat))
assert len(basis)==77 and len(rows)==59
assert M.rank()==33
print('rank',M.rank(),flush=True)
os.makedirs('workspace',exist_ok=True)
with open('workspace/fz25_upper_data.json','w') as f:json.dump({'basis':basis,'labels':labels,'matrix':[[str(c) for c in row] for row in mat]},f)

def rank_mod_certificate(mat,p=1000000007):
    H=[[int(Q(x).numerator%p)*pow(int(Q(x).denominator%p),-1,p)%p for x in row] for row in mat]
    rowids=list(range(len(H))); prows=[]; pcols=[]; r=0
    for j in range(len(H[0])):
        t=next((i for i in range(r,len(H)) if H[i][j]),None)
        if t is None:continue
        H[r],H[t]=H[t],H[r];rowids[r],rowids[t]=rowids[t],rowids[r]
        prows.append(rowids[r]);pcols.append(j)
        inv=pow(H[r][j],-1,p)
        H[r]=[(a*inv)%p for a in H[r]]
        for i in range(r+1,len(H)):
            c=H[i][j]
            if c:H[i]=[(a-c*b)%p for a,b in zip(H[i],H[r])]
        r+=1
        if r==len(H):break
    return prows,pcols
pr,pc=rank_mod_certificate(mat)
minor=sp.Matrix([[mat[i][j] for j in pc] for i in pr])
print('pivot rows',pr,'pivot columns',pc,flush=True)
assert int(minor.det())%1000000007==88277662
print('minor determinant mod prime',int(minor.det())%1000000007,flush=True)
