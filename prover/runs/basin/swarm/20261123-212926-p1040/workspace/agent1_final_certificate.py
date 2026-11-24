"""Exact certificate: no stored relation or rank is trusted."""
from itertools import combinations, product
from collections import defaultdict

def red(w):
    z=[]
    for a in w:
        if z and z[-1]==-a:z.pop()
        else:z.append(a)
    return tuple(z)
def inv(w):return tuple(-a for a in w[::-1])
def cat(*ww):return red(a for w in ww for a in w)
def comm(a,b):return cat(a,b,inv(a),inv(b))
def gens(n):
    return [('C',i,j) for i in range(n) for j in range(n) if i!=j]+[('M',i,j,k) for i in range(n) for j,k in combinations(range(n),2) if i not in (j,k)]
def extend(A,g,sign=1):
    typ,i,*args=g; B=list(A)
    if typ=='C':
        w=A[args[0]] if sign==1 else inv(A[args[0]])
        B[i]=cat(w,A[i],inv(w))
    else:
        w=comm(A[args[0]],A[args[1]])
        B[i]=cat(A[i],w if sign==1 else inv(w))
    return tuple(B)
def clean(v):return {i:c for i,c in v.items() if c}
def add(v,w,a=1):
    v=dict(v)
    for i,c in w.items():v[i]=v.get(i,0)+a*c
    return clean(v)
class Lattice:
    # Every accepted row has unit leading coefficient: span is primitive.
    def __init__(self):self.b={};self.queue=[]
    def put(self,v):
        v=clean(v)
        while v:
            p=min(v);a=v[p]
            if p in self.b:v=add(v,self.b[p],-a)
            else:
                if abs(a)!=1:return
                v={i:a*c for i,c in v.items()}
                self.b[p]=v;self.queue.append(v);return

def setup(n):
    G=gens(n);N=len(G);P=list(combinations(range(N),2));pi={x:i for i,x in enumerate(P)}
    return G,P,pi

def collisions(n):
    G,P,pi=setup(n);N=len(G);L=Lattice();unit=tuple((i+1,) for i in range(n))
    zero=(0,)*N;seen={unit:(zero,{})};layer=[(unit,zero,{})]
    for depth in range(3):
        nxt=[]
        for A,e,c in layer:
            for a,g in enumerate(G):
                for sign in (1,-1):
                    B=extend(A,g,sign);f=list(e);f[a]+=sign;f=tuple(f);v=dict(c)
                    for j in range(a+1,N):
                        if e[j]:v[pi[a,j]]=v.get(pi[a,j],0)-sign*e[j]
                    v=clean(v)
                    if B in seen:
                        f0,v0=seen[B];assert f==f0
                        L.put(add(v,v0,-1))
                    else:seen[B]=(f,v);nxt.append((B,f,v))
        layer=nxt
    return L

def actions(n):
    G,P,pi=setup(n);N=len(G);basis={};coords=[]
    for a,g in enumerate(G):
        if g[0]=='C':
            _,i,j=g;v=(i,min(i,j),max(i,j));s=1 if j<i else -1
        else:_,i,j,k=g;v=(i,j,k);s=1
        coords.append((v,s));basis[v]=(a,s)
    allacts=[]
    for p in range(n):
        for q in range(n):
            if p==q:continue
            cols=[]
            for (i,j,k),s in coords:
                v={}
                for r,a in [(i,1)]+([(q,-1)] if i==p else []):
                    for b,x in [(j,1)]+([(p,1)] if j==q else []):
                        for d,y in [(k,1)]+([(p,1)] if k==q else []):
                            if b==d:continue
                            z,t=basis[r,min(b,d),max(b,d)]
                            v[z]=v.get(z,0)+s*a*x*y*t*(1 if b<d else -1)
                cols.append(clean(v))
            act=[]
            for a,b in P:
                v={}
                for i,x in cols[a].items():
                    for j,y in cols[b].items():
                        if i==j:continue
                        k=pi[min(i,j),max(i,j)]
                        v[k]=v.get(k,0)+x*y*(1 if i<j else -1)
                act.append(clean(v))
            allacts.append(act)
    return allacts

def close(n,L):
    aa=actions(n);k=0
    while k<len(L.queue):
        v=L.queue[k];k+=1
        for act in aa:
            w={}
            for i,c in v.items():
                for j,d in act[i].items():w[j]=w.get(j,0)+c*d
            L.put(w)
    return L

def bracket_columns(n):
    G,P,_=setup(n);D=[]
    for g in G:
        if g[0]=='C':_,i,j=g;D.append((i,{(j,i):1,(i,j):-1}))
        else:_,i,j,k=g;D.append((i,{(j,k):1,(k,j):-1}))
    def act(d,w):
        root,v=d;out={}
        for a,x in enumerate(w):
            if x==root:
                for u,c in v.items():out[w[:a]+u+w[a+1:]]=out.get(w[:a]+u+w[a+1:],0)+c
        return clean(out)
    out=[]
    for a,b in P:
        v={}
        for d,e,s in [(D[a],D[b],1),(D[b],D[a],-1)]:
            root,pol=e
            for w,c in pol.items():
                for u,k in act(d,w).items():
                    idx=(root,)+u;v[idx]=v.get(idx,0)+s*c*k
        out.append(clean(v))
    return out

def certify(n,L):
    B=bracket_columns(n);I=Lattice()
    for v in B:I.put(v)
    N=len(gens(n));r=n*n*(n*n-1)//3-n*(n+1)//2
    assert len(I.b)==r
    assert len(L.b)==N*(N-1)//2-r
    for v in L.b.values():
        out={}
        for i,c in v.items():out=add(out,B[i],c)
        assert not out
    print('CERTIFIED',n,'source relations',len(L.b),'primitive image',len(I.b))


def seed_from_four(n,L4):
    G,P,pi=setup(n);gi={g:i for i,g in enumerate(G)}
    L=Lattice();unit=tuple((i+1,) for i in range(n))
    for a,(i,j) in enumerate(P):
        if extend(extend(unit,G[i]),G[j])==extend(extend(unit,G[j]),G[i]):L.put({a:1})
    G4,P4,_=setup(4)
    for sub in combinations(range(n),4):
        ids=[gi[(g[0],)+tuple(sub[i] for i in g[1:])] for g in G4]
        emb=[(pi[min(ids[i],ids[j]),max(ids[i],ids[j])],1 if ids[i]<ids[j] else -1) for i,j in P4]
        for v in L4.b.values():L.put({emb[i][0]:c*emb[i][1] for i,c in v.items()})
    return L

def trace(v):
    out={}
    for (root,a,b,c),coef in v.items():
        if root==a:
            k=tuple(sorted((b,c)));out[k]=out.get(k,0)+coef
    return clean(out)

def degree_two():
    for n in range(2,7):
        for col in bracket_columns(n):assert not trace(col)
        for root,a,b,c in product(range(n),repeat=4):
            if a==b:continue
            v={}
            for w,z in [((a,b,c),1),((b,a,c),-1),((c,a,b),-1),((c,b,a),1)]:
                v[(root,)+w]=v.get((root,)+w,0)+z
            tr=trace(v)
            expected={}
            if root==a:expected[tuple(sorted((b,c)))]=1
            if root==b:
                k=tuple(sorted((a,c)));expected[k]=expected.get(k,0)-1
            assert tr==clean(expected) and (not tr or list(tr.values()) in ([1],[-1]))
    for n in (2,3,4):
        I=Lattice()
        for col in bracket_columns(n):I.put(col)
        assert len(I.b)==n*n*(n*n-1)//3-n*(n+1)//2
    for n in (3,4):
        L=close(n,collisions(n));certify(n,L)
        if n==4:L4=L
    for n in (5,6):certify(n,close(n,seed_from_four(n,L4)))

def uniform_algebra():
    import sympy as S
    x,a,b=S.symbols('x a b');E=S.Matrix([[0,1],[0,0]]);F=E.T;I=S.eye(2)
    def cm(P,Q):return S.simplify(P*Q*P.inv()*Q.inv())
    D=S.diag(1+x,1)
    assert cm(D,I+a*E)==I+a*x*E
    C=cm(I+a*E,I+b*F)
    assert C==S.Matrix([[1+a*b+a*a*b*b,-a*a*b],[a*b*b,1-a*b]])
    for c in range(3,129):
        # Exact current-Lie Johnson cancellation.
        A=x**(c-2)*E;B=-x*F;H=A*B-B*A;d=S.diag(x,0)
        assert H*d-d*H==S.zeros(2)
        cc=C.subs({a:x**(c-2),b:-x}).applyfunc(S.expand)
        rem=lambda z:S.rem(z,x**c,x)
        assert cc.applyfunc(rem)==S.diag(1-x**(c-1),1+x**(c-1))
        odds=[p for p in S.factorint(c) if p%2];p=min(odds) if odds else 2
        ell=p if p%2 else 4;r=c//(p if p%2 else 4)
        P=S.Poly(S.cyclotomic_poly(ell,x).subs(x,1+x**r),x);e=P.degree()
        assert P.LC()==1 and P.TC()==p
        assert all(int(z)%p==0 for z in P.all_coeffs()[1:])
        assert e*p==(p-1)*c
        f=3 if p==2 else 2 if p in (3,5) else 1
        assert p**f>=7 and f%p
    print('CERTIFIED current brackets, torus matrices, Eisenstein/conductor data, c=3..128')

def fox_checks():
    import sympy as S
    T=S.Symbol('T');s=T-1
    def fox(A):
        n=len(A);J=S.zeros(n)
        for i,w in enumerate(A):
            e=0
            for a in w:
                j=abs(a)-1
                if a>0:J[i,j]+=T**e
                else:J[i,j]-=T**(e-(j==1))
                e+=(1 if a>0 else -1)*(j==1)
        return J.T
    for n in range(2,7):
        unit=tuple((i+1,) for i in range(n));ids=[i for i in range(n) if i!=1];idx={i:k for k,i in enumerate(ids)}
        for g in gens(n):
            R=fox(extend(unit,g)).extract(ids,ids);want=S.eye(n-1)
            if g[0]=='C':
                _,i,j=g
                if j==1:want[idx[i],idx[i]]=T
            else:
                _,i,j,k=g
                if i!=1 and 1 in (j,k):
                    leaf=k if j==1 else j
                    want[idx[leaf],idx[i]]=(1 if j==1 else -1)*s
            assert (R-want).applyfunc(S.simplify)==S.zeros(n-1)
    print('CERTIFIED exact Fox derivatives of every Magnus generator, ranks 2..6')

class LocalRing:
    # Z[pi]/(pi^2+p*pi+p, pi^N), represented by pi-adic digits.
    def __init__(self,p,N):
        self.p=p;self.N=N;self.zero=(0,0);self.one=(1,0)
        self.elts=[self.digits(d) for d in product(range(p),repeat=N)]
    def digits(self,d):
        a=b=0
        for x in d[::-1]:a,b=-self.p*b,a-self.p*b;a+=x
        return a,b
    def reduce(self,a,b):
        d=[]
        for _ in range(self.N):
            r=a%self.p;d.append(r);a-=r;a,b=b-a,-a//self.p
        return self.digits(d)
    def add(self,x,y):return self.reduce(x[0]+y[0],x[1]+y[1])
    def scale(self,x,a):return self.reduce(a*x[0],a*x[1])
    def mul(self,x,y):
        a,b=x;c,d=y;p=self.p
        return self.reduce(a*c-p*b*d,a*d+b*c-p*b*d)
    def power(self,x,n):
        a=self.one
        for _ in range(n):a=self.mul(a,x)
        return a

def norm_checks():
    for p,N in [(3,3),(2,4)]:
        R=LocalRing(p,N);pi=R.reduce(0,1);zeta=R.add(R.one,pi);norms=set()
        if p==3:
            for a,b,c in product(R.elts,repeat=3):
                v=R.add(R.add(R.power(a,3),R.mul(zeta,R.power(b,3))),R.mul(R.power(zeta,2),R.power(c,3)))
                v=R.add(v,R.scale(R.mul(zeta,R.mul(a,R.mul(b,c))),-3));norms.add(v)
        else:
            for a,b in product(R.elts,repeat=2):norms.add(R.add(R.power(a,2),R.scale(R.mul(zeta,R.power(b,2)),-1)))
        for sign in (1,-1):assert R.add(R.one,R.scale(R.power(pi,N-1),sign)) not in norms
        print('CERTIFIED nonnorms: p,c=',p,N,'ring size',len(R.elts),'norm-image size',len(norms))

def pari_checks():
    # Optional independent quadratic Hilbert-symbol check, using Sage/PARI.
    try:from sage.all import pari
    except ImportError:return
    for c in (4,8,16,32,64):
        r=c//4;P=pari('x')**(2*r)+2*pari('x')**r+2
        nf=pari.nfinit(P);pi=pari.Mod(pari('x'),P);pr=pari.idealprimedec(nf,2)
        assert len(pr)==1 and pari.nfhilbert(nf,1-pi**(c-1),1+pi,pr[0])==-1
    print('CERTIFIED PARI quadratic Hilbert symbols, c=4,8,16,32,64')

if __name__=='__main__':
    import time
    t=time.time();degree_two();fox_checks();uniform_algebra();norm_checks();pari_checks()
    print('ALL CERTIFICATES VERIFIED; seconds',time.time()-t)
