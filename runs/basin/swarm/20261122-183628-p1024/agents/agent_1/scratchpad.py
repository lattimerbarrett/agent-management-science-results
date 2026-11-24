from sage.all import QQ, matrix, binomial
from collections import defaultdict
from time import time


def lp_mul(a,b):
    c=defaultdict(QQ)
    for i,x in a.items():
        for j,y in b.items():
            c[i+j]+=x*y
    return {i:x for i,x in c.items() if x}


def build(g,b,N=None,K=QQ):
    r=(g+2)//3; k=g-r
    assert len(b)==r
    b=[K(x) for x in b]
    if N is None: N=4*g-4
    h=2*g-2; q=2*g-1; d=q-k; J=N//k
    M=N+J*d+1; P=J*d+h+1; B=M+P; D=4*g+2
    nongaps=[j for j in range(M+1) if j%2==0 or j>=2*g+1]
    nc=(N+1)*len(nongaps); nr=(N+1)*B
    entries=[defaultdict(QQ),defaultdict(QQ),defaultdict(QQ)] # O, S, L
    psi={k-q+2*j:x for j,x in enumerate(b) if x}
    deriv={k-q+2*j-1:(-q+2*j)*x for j,x in enumerate(b) if x}
    pw=[{0:QQ(1)}]
    for l in range(J): pw.append(lp_mul(pw[-1],psi))
    sqrt=[(-1)**j*binomial(QQ(1)/2,j) for j in range((B+M+P+D)//D+2)]
    def add(which, rb, cb, m,n,poly,shift,fac,sp):
        # polynomial * t^shift * fac * s^sp, times each affine monomial
        for il,lam in enumerate(nongaps):
            eps=lam%2
            beta=sp+eps
            col=(cb*(N+1)+n)*len(nongaps)+il
            for e,v in poly.items():
                e0=e+shift-lam
                if beta==0: terms=[(0,QQ(1))]
                elif beta==2: terms=[(0,QQ(1)),(1,QQ(-1))]
                else: terms=enumerate(sqrt[:max(0,(-1-e0)//D+1)])
                for j,c in terms:
                    e1=e0+D*j
                    if -B<=e1<0 and c:
                        row=(rb*(N+1)+m)*B+(e1+B)
                        entries[which][row,col]+=fac*v*c
    for n in range(N+1):
        for l in range((N-n)//k+1):
            m=n+l*k
            co=binomial(-QQ(n)/k,l)*(-k)**l
            cl=binomial(1-QQ(n)/k,l)*(-k)**l
            add(0,0,0,m,n,pw[l],n,co,0)
            add(2,0,0,m,n,pw[l],n-h,-cl/2,1)
            add(1,0,0,m,n,pw[l],n-h,-co/2,1)
            add(1,1,1,m,n,pw[l],n,cl,0)
            add(1,1,0,m,n,pw[l],n-h-1,co/2,1)
            if l:
                cp=binomial(-QQ(n)/k,l-1)*(-k)**(l-1)
                add(1,1,0,m,n,lp_mul(deriv,pw[l-1]),n-h,cp/2,1)
    mats=[]
    for i,ent in enumerate(entries):
        mult=2 if i==1 else 1
        mats.append(matrix(K,mult*nr,mult*nc,{ij:x for ij,x in ent.items() if x},sparse=True))
    return mats,(N,M,P,len(nongaps))


def invariants(g,b,N=None,K=QQ):
    t=time(); mats,pars=build(g,b,N,K)
    ranks=[A.rank() for A in mats]
    N,M,P,a=pars
    chis=[]
    # chi(O(np))=n+1-g; chi(Theta(np))=n+3-3g
    chiO=sum(n+1-g for n in range(N+1))
    chiL=sum(n+3-3*g for n in range(N+1))
    chis=[chiO,chiO+chiL,chiL]
    h0=[A.ncols()-rho for A,rho in zip(mats,ranks)]
    h1=[a-c for a,c in zip(h0,chis)]
    delta=ranks[1]-ranks[0]-ranks[2]
    assert delta==h1[0]-h1[1]+h1[2]
    print('g,b,N=',g,b,N,'shape=',[(A.nrows(),A.ncols()) for A in mats],
          'ranks=',ranks,'h1=',h1,'Delta=',delta,'seconds=',round(time()-t,3),flush=True)
    return h1,delta

def check_inverses(k,N):
    import sympy as sp
    t,F,Fp,a=sp.symbols('t F Fp a', nonzero=True)
    d=N+1
    TO=sp.zeros(d); UO=sp.zeros(d)
    TL=sp.zeros(d); UL=sp.zeros(d)
    TS=sp.zeros(2*d); US=sp.zeros(2*d)
    for n in range(d):
        for ell in range((N-n)//k+1):
            m=n+ell*k
            c=sp.binomial(-sp.Rational(n,k),ell)*(-k*t**k*F)**ell
            e=sp.binomial(1-sp.Rational(n,k),ell)*(-k*t**k*F)**ell
            ci=sp.binomial(-sp.Rational(n,k),ell)*(k*F)**ell
            ei=sp.binomial(1-sp.Rational(n,k),ell)*(k*F)**ell
            TO[m,n]=t**n*c; UO[m,n]=t**(-n)*ci
            TL[m,n]=a*t**n*e; UL[m,n]=t**(-n)*ei/a
            TS[m,n]=a*TO[m,n]; TS[d+m,d+n]=t**n*e
            TS[d+m,n]=-a*t**(n-1)*c
            US[m,n]=UO[m,n]/a; US[d+m,d+n]=t**(-n)*ei
            US[d+m,n]=t**(-n-1)*ci
            if ell:
                cp=sp.binomial(-sp.Rational(n,k),ell-1)*(-k*t**k*F)**(ell-1)
                cip=sp.binomial(-sp.Rational(n,k),ell-1)*(k*F)**(ell-1)
                TS[d+m,n]-=a*t**(n+k)*Fp*cp
                US[d+m,n]+=t**(-n)*(Fp+k*F/t)*cip
    for T,U in [(TO,UO),(TS,US),(TL,UL)]:
        assert all(sp.expand(v)==0 for v in T*U-sp.eye(T.rows))
    print('symbolic inverses checked:', k,N,flush=True)

if __name__=='__main__':
    from sage.all import QQbar
    assert invariants(4,[QQbar(2).sqrt(),QQbar.gen()],K=QQbar)[1]==-1
    for k,N in [(1,4),(2,8),(2,12),(3,16)]:
        check_inverses(k,N)
    for g in range(2,7):
        hh,dd=invariants(g,[0]*((g+2)//3))
        assert hh==[g*g,6*g*g-7*g+2,5*g*g-7*g+3] and dd==1
    for g,b in [(2,[1]),(3,[1]),(4,[1,0]),(4,[0,1]),(4,[1,1]),(7,[1,2,1])]:
        base=invariants(g,b)
        for inc in [1,2]:
            assert invariants(g,b,4*g-4+inc)==base
