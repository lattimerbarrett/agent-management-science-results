import math,functools,pickle,os
from collections import Counter,defaultdict
P=1000000007
N=12

def parts(n, lo=1):
    if n==0: yield ()
    for a in range(lo,n+1):
        for b in parts(n-a,a): yield (a,)+b

def inv(x):return pow(x%P,-1,P)
def mul(a,b,N=N):
    return [sum(a[i]*b[n-i] for i in range(n+1))%P for n in range(N+1)]
def div(a,b):
    q=[]
    for n in range(len(a)):
        q.append((a[n]-sum(q[i]*b[n-i] for i in range(n)))*inv(b[0])%P)
    return q
A=[math.factorial(6*n)//math.factorial(3*n)//math.factorial(2*n)%P for n in range(N+1)]
B=[a*(6*n+1)*inv(6*n-1)%P for n,a in enumerate(A)]
D=div(B,A)
logA=[0]+[v*inv(i)%P for i,v in enumerate(div([i*A[i]%P for i in range(1,N+1)]+[0],A)[:N],1)]
# derivative indexing: vector [A1,2A2,...], divide A, then integrate
powD=[[1]+[0]*N]
for i in range(10):powD.append(mul(powD[-1],D))
sigmas=[s for w in range(11) for s in parts(w) if all(x%3!=2 for x in s)]
sigmas.sort(key=lambda s:(len(s),s))
@functools.lru_cache(None)
def subs(s):
    cs=list(Counter(s).items())
    out=[()]
    for a,m in cs:out=[t+(a,)*j for t in out for j in range(m+1)]
    return out

def minus(s,t):
    c=Counter(s);c.subtract(t)
    return tuple(a for a in sorted(c) for _ in range(c[a]))

E={}
for s in sigmas:
    if not s:
        f={lam: math.prod(pow(-logA[a]%P,m,P)*inv(math.factorial(m))%P for a,m in Counter(lam).items())%P for r in range(N+1) for lam in parts(r)}
        E[s]=f
        continue
    v=s[0]; mv=s.count(v); f=defaultdict(int)
    for t in subs(s):
        if v not in t:continue
        m=len(t); shift=sum(a//3 for a in t); j=sum(a%3==1 for a in t)
        factor=(-1)**m*math.factorial(m-1)*math.prod(inv(math.factorial(h)) for h in Counter(t).values())*t.count(v)*inv(mv)%P
        rem=minus(s,t)
        for lam,x in E[rem].items():
            maxk=N-sum(lam)
            for k in range(shift,maxk+1):
                coeff=factor*powD[j][k-shift]%P
                if not coeff:continue
                if k==0:newlam=lam;coeff=coeff*48%P
                else:newlam=tuple(sorted(lam+(k,)))
                f[newlam]=(f[newlam]+x*coeff)%P
    E[s]=dict(f)

basis=list(parts(12)); pos={s:i for i,s in enumerate(basis)}
rows=[]; tags=[]
for d in range(1,13):
    for s in sigmas:
        if 24+sum(s)>=3*d or (25-d-sum(s)-1)%2:continue
        for lam in parts(12-d):
            row=[0]*len(basis)
            for t,c in E[s].items():
                if sum(t)==d:row[pos[tuple(sorted(t+lam))]]=c
            rows.append(row);tags.append((d,s,lam))

def rankmod(rows):
    mat=[list(r) for r in rows]; piv=[];r=0
    for j in range(len(mat[0])):
        i=next((i for i in range(r,len(mat)) if mat[i][j]%P),None)
        if i is None:continue
        mat[r],mat[i]=mat[i],mat[r]; z=inv(mat[r][j]);mat[r]=[a*z%P for a in mat[r]]
        for i in range(r+1,len(mat)):
            z=mat[i][j]
            if z:mat[i]=[(a-z*b)%P for a,b in zip(mat[i],mat[r])]
        piv.append(j);r+=1
        if r==len(mat):break
    return r,piv
print('FZ',len(rows),'rank',rankmod(rows)[0],'dim',77-rankmod(rows)[0],flush=True)
for dd in [10,11]:
    bs=list(parts(dd)); ix={s:i for i,s in enumerate(bs)}; rr=[]
    for d in range(1,dd+1):
        for s in sigmas:
            if 24+sum(s)>=3*d or (25-d-sum(s)-1)%2:continue
            for lam in parts(dd-d):
                row=[0]*len(bs)
                for t,c in E[s].items():
                    if sum(t)==d:row[ix[tuple(sorted(t+lam))]]=c
                rr.append(row)
    print('degree',dd,'dim',len(bs)-rankmod(rr)[0])
pickle.dump((rows,tags,E),open('fz.pkl','wb'))
if os.environ.get('EXACT_FZ')=='1':raise SystemExit
# kappa integral recursion polynomials H for total weight<=23
odd=[math.prod(range(1,2*n+2,2))%P for n in range(24)]
@functools.lru_cache(None)
def H(s):
    if not s:return (1,)
    out=[0]*(len(s)+1);v=s[0]; rest=s[1:];c=Counter(rest)
    for t in subs(rest):
        cc=Counter(t); mult=math.prod(math.comb(c[a],cc[a]) for a in cc)
        factor=mult*(-1)**len(t)*inv(odd[v+sum(t)])%P
        hs=H(minus(rest,t))
        for k,x in enumerate(hs):out[k+1]=(out[k+1]+factor*x)%P
    return tuple(out)
@functools.lru_cache(None)
def integral(s):
    return sum(x*(math.factorial(47+k)//math.factorial(48))*odd[23] for k,x in enumerate(H(s)) if k>=1)%P
pair=[[integral(tuple(sorted(a+b))) for b in basis] for a in parts(11)]
print('pairing',len(pair),len(pair[0]),'rank',rankmod(pair)[0],flush=True)
print('FZ annihilated',all(sum(a*b for a,b in zip(row,p))%P==0 for row in rows for p in pair))
pickle.dump(pair,open('pair.pkl','wb'))
# EXACT RUN
import gmpy2
text=open(__file__).read().split('# EXACT RUN')[0]
text=text.replace('def inv(x):return pow(x%P,-1,P)', 'def inv(x):return gmpy2.mpq(1,x)')
text=text.replace('pow(-logA[a]%P,m,P)', '(-logA[a])**m')
text=text.replace('%P','')
os.environ['EXACT_FZ']='1'
print('Rational computation:',flush=True)
exec(text)
