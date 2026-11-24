import sympy as s
from fractions import Fraction as F
from math import factorial, comb
import pickle
N=12; W=10; g=25
parts=[1,3,4,6,7,9,10]
def partitions(n, allowed=None):
    if n==0: yield ()
    else:
        if allowed is None: allowed=range(1,n+1)
        for a in allowed:
            if a<=n:
                for tail in partitions(n-a,[b for b in allowed if b>=a]): yield (a,)+tail
sigmas=[p for w in range(W+1) for p in partitions(w,parts)]
A=[F(factorial(6*i),factorial(3*i)*factorial(2*i)) for i in range(N+1)]
B=[a*F(6*i+1,6*i-1) for i,a in enumerate(A)]
def mul(a,b): return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(N+1)]
ratio=[]
for i in range(N+1): ratio.append(B[i]-sum(A[j]*ratio[i-j] for j in range(1,i+1)))
powers=[[F(1)]+[F(0)]*N]
for j in range(W): powers.append(mul(powers[-1],ratio))
logA=[F(0)]*(N+1)
for i in range(1,N+1): logA[i]=A[i]-sum(F(j,i)*logA[j]*A[i-j] for j in range(1,i))
# gamma_i is list (sigma, coefficient); kappa_i factor suppressed
Gamma=[[] for i in range(N+1)]
for sig in sigmas:
    if not sig:
        cs=logA
    else:
        l=len(sig); shift=sum(a//3 for a in sig); n1=sum(a%3==1 for a in sig)
        c=F((-1)**(l-1)*factorial(l-1))
        for a in set(sig): c/=factorial(sig.count(a))
        cs=[F(0)]*shift+[c*v for v in powers[n1][:N+1-shift]]
    for i in range(1,N+1):
        if cs[i]: Gamma[i].append((sig,cs[i]))
E=[{((1,)*l,()):F(comb(2*g-3+l,l)) for l in range(W+1)}]
for r in range(1,N+1):
    curr={}
    for i in range(1,r+1):
        for sig,c in Gamma[i]:
            w=sum(sig)
            for (ps,ks),v in E[r-i].items():
                if w+sum(ps)>W: continue
                key=(tuple(sorted(sig+ps)),tuple(sorted(ks+(i,))))
                curr[key]=curr.get(key,F(0))-F(i,r)*c*v
    curr={k:v for k,v in curr.items() if v}
    E.append(curr)
    print(r,len(curr),flush=True)
# gather relations, and products at degree12
rels=[]
for r in range(1,N+1):
    for sig in sigmas:
        w=sum(sig)
        if 2*g: pass
        if g-1+w>=3*r or (g-r-w-1)%2: continue
        rel={ks:c for (ps,ks),c in E[r].items() if ps==sig}
        if not rel: continue
        for p in partitions(N-r):
            rels.append({tuple(sorted(ks+p)):c for ks,c in rel.items()})
basis=list(partitions(N)); prime=1000000007
mat=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix([[(v.numerator*pow(v.denominator,-1,prime))%prime for p in basis for v in [rel.get(p,F(0))]] for rel in rels])).convert_to(s.GF(prime))
print('relations',len(rels),'rank',mat.rank(),'FZdimension',len(basis)-mat.rank(),flush=True)
with open('fz.pkl','wb') as f: pickle.dump((E,rels,basis),f)
from functools import lru_cache
from collections import Counter
from itertools import product
DF=[1]*49
for k in range(1,49): DF[k]=DF[k-1]*(2*k-1)%prime
invdf=[pow(v,-1,prime) for v in DF]
@lru_cache(None)
def poly(ds):
    if not ds: return (1,)
    first=ds[0]; ctr=Counter(ds[1:]); vals=sorted(ctr)
    out=[0]*(len(ds)+1)
    for nums in product(*(range(ctr[a]+1) for a in vals)):
        bsum=first+sum(a*n for a,n in zip(vals,nums)); bsize=1+sum(nums)
        coeff=(-1)**(bsize-1)*invdf[bsum+1]
        for a,n in zip(vals,nums): coeff=coeff*comb(ctr[a],n)%prime
        rest=tuple(a for a,n in zip(vals,nums) for _ in range(ctr[a]-n))
        v=poly(rest)
        for k,c in enumerate(v): out[k+1]=(out[k+1]+c*coeff)%prime
    return tuple(out)
@lru_cache(None)
def intersection(ds):
    v=poly(ds)
    return sum(c*(factorial(2*g-3+k)%prime) for k,c in enumerate(v))%prime
lowbasis=list(partitions(g-2-N))
ints=[[intersection(tuple(sorted(p+q))) for q in basis] for p in lowbasis]
pmat=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix(ints)).convert_to(s.GF(prime))
print('pairing rank',pmat.rank(),'dims',len(lowbasis),len(basis),flush=True)
fzred, fzpivots=mat.rref()
free=[i for i in range(len(basis)) if i not in fzpivots]
qpair=pmat.extract(list(range(len(lowbasis))),free)
null=qpair.nullspace().to_Matrix()
print('FZ quotient basis size',len(free),'pairing kernel dimension',null.rows,flush=True)
rvec=[0]*len(basis)
for j,c in zip(free,list(null.row(0))): rvec[j]=int(c)%prime
rmat=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix([rvec])).convert_to(s.GF(prime))
print('FZ plus extra kernel generator rank',mat.vstack(rmat).rank(),flush=True)
print('kernel generator support:',[(basis[j],rvec[j]) for j in free if rvec[j]],flush=True)
print('pairing annihilates FZ:',(pmat*mat.transpose()).is_zero_matrix,flush=True)
with open('relation_data.pkl','wb') as f: pickle.dump((basis,lowbasis,free,ints,rvec),f)
# Recompute every intersection over Q, independently of finite-field arithmetic.
DFQ=[1]*49
for k in range(1,49): DFQ[k]=DFQ[k-1]*(2*k-1)
@lru_cache(None)
def polyQ(ds):
    if not ds: return (F(1),)
    first=ds[0]; ctr=Counter(ds[1:]); vals=sorted(ctr)
    out=[F(0)]*(len(ds)+1)
    for nums in product(*(range(ctr[a]+1) for a in vals)):
        bsum=first+sum(a*n for a,n in zip(vals,nums)); bsize=1+sum(nums)
        coeff=F((-1)**(bsize-1),DFQ[bsum+1])
        for a,n in zip(vals,nums): coeff*=comb(ctr[a],n)
        rest=tuple(a for a,n in zip(vals,nums) for _ in range(ctr[a]-n))
        for k,c in enumerate(polyQ(rest)): out[k+1]+=c*coeff
    return tuple(out)
@lru_cache(None)
def intersectionQ(ds):
    return sum(c*factorial(2*g-3+k) for k,c in enumerate(polyQ(ds)))
Qints=[[intersectionQ(tuple(sorted(p+q))) for q in basis] for p in lowbasis]
Qmat=s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix(Qints)).convert_to(s.QQ)
print('EXACT RATIONAL PAIRING RANK:',Qmat.rank(),flush=True)
with open('exact_pairing.pkl','wb') as f: pickle.dump((Qints,basis,lowbasis),f)
