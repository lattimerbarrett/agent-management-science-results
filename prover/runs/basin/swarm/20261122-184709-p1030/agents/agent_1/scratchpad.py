import numpy as np
from collections import Counter
import sympy as sp

def pars(h,s):
    a=1+4*h*h
    p=2*a*s-2*h
    q=p+a
    r=p+(p*p+1)//a
    return a,p,q,r

def floor_sum(n,k):
    m,z=np.divmod(n,k)
    return k*(m*(m-1)//2)+m*z

def tau(n,p,q,r):
    return 2-n+floor_sum(n,p)-floor_sum(n-1,q)-floor_sum(n-1,r)

def delta(n,p,q,r):
    return 1+n//p-(n+q-1)//q-(n+r-1)//r

def persistent_bars(weights):
    n=len(weights)
    par=np.full(n,-1,dtype=np.int64)
    birth=np.zeros(n,dtype=np.int64)
    out=[]
    def root(i):
        while par[i]!=i:
            par[i]=par[par[i]]; i=par[i]
        return i
    for i in np.argsort(weights,kind='stable'):
        par[i]=i; birth[i]=weights[i]
        for j in (i-1,i+1):
            if 0<=j<n and par[j]>=0:
                u,v=root(i),root(j)
                if u==v: continue
                if birth[u]>birth[v]: u,v=v,u
                length=int(weights[i]-birth[v])
                if length: out.append(length)
                par[v]=u
    return Counter(out)

def symbolic_checks():
    h,s=sp.symbols('h s',integer=True)
    a=1+4*h*h; p=2*a*s-2*h; q=p+a
    v=4*h*s-1; cc=v*v+4*s*s; r=p+cc
    x=2*h*(2*s+1)-1; y=2*s+1; b=x*x+y*y
    for expr in [a*cc-p*p-1, q+r-b, q*r-p*b-1,
                 a*b-q*q-1, p-(2*h*v+2*s), b-4*p-((v-2*h)**2+(2*s-1)**2),
                 (b-2)-4*(h*(2*s+1)-1)*(h*(2*s+1))-4*s*(s+1)]:
        assert sp.expand(expr)==0
    # Gram identity and peak-height identity.
    A,B,W,Zx,Zy=sp.symbols('A B W Zx Zy')
    X=2*h*A-v*B; Y=A-2*s*B
    assert sp.expand(a*A*A-2*p*A*B+cc*B*B-X*X-Y*Y)==0
    Sx,Sy=v-2*h,2*s-1
    assert sp.expand((Sx+2*Zx)**2+(Sy+2*Zy)**2-(Sx*Sx+Sy*Sy)-4*(Zx*Zx+Zy*Zy)-4*(Sx*Zx+Sy*Zy))==0


def check_case(h,s,full=False):
    a,p,q,r=pars(h,s); b=q+r; M=(p-2)*q*r+2; c=M//2
    v=4*h*s-1; x=v+2*h; y=2*s+1
    L=(b-2)//8; d=min(h,s+1)
    assert b%8==2 and p%2==0 and p<q<2*p and r>p
    assert a*(r-p)==p*p+1 and p*b+1==q*r
    assert x*x+y*y==b and 4*p<=b
    tc=int(tau(c,p,q,r)); tmin=tc-L
    # All p-grid vertices: quadratic norm identity, not a sample.
    grid=np.arange(0,M+1,p,dtype=np.int64)
    z=grid-c; A=2*(z//q)+1; B=2*(z//r)+1
    W=2*z//p-A-B; X=2*h*A-v*B; Y=A-2*s*B
    tg=tau(grid,p,q,r)
    assert np.all((W%2==1)&(X%2==1)&(Y%2==1))
    assert np.array_equal(8*(tg-tmin),p*(W*W-1)+X*X+Y*Y-2)
    assert np.min(tg)==tmin
    assert np.all(W==2*delta(grid,p,q,r)-1)
    # Four explicit global minima, on both sides.
    mins=[]
    for XX in (-1,1):
        for YY in (-1,1):
            n=c+p*(1+y*XX-x*YY)//2
            assert 0<n<M and n%p==0 and tau(n,p,q,r)==tmin
            mins.append(n)
    assert min(mins)<c<max(mins)
    # Check every possible (including virtual) peak roof.
    pref=np.minimum.accumulate(tg)
    arg=[]; best=0
    for k in range(len(tg)):
        if tg[k]<tg[best]: best=k
        arg.append(best)
    roofs=[]
    for k,n in enumerate(grid[:-1]):
        if delta(n,p,q,r)!=1: continue
        alpha=q-(n-1)%q; beta=r-(n-1)%r
        if alpha>p or beta>p: continue
        Zx=(int(X[k])-(v-2*h))//2
        Zy=(int(Y[k])-(2*s-1))//2
        m=x*Zx+y*Zy; T=y*Zx-x*Zy
        assert alpha==p//2+2*h*Zx+Zy
        assert beta==p//2-v*Zx-2*s*Zy
        peak=n+min(alpha,beta); height=int(tau(peak,p,q,r))
        assert height==tmin+L+(Zx*Zx+Zy*Zy-abs(m))//2
        roofs.append((peak,height))
        if peak<c:
            assert T<0 and max(abs(2*h*Zx+Zy),abs(v*Zx+2*s*Zy))<=p//2
            j=arg[k]
            # The prefix minimum can be chosen at a W=1 grid point.
            eligible=np.flatnonzero((tg[:k+1]==pref[k]) & (W[:k+1]==1))
            assert len(eligible)
            j=int(eligible[-1]); Dx=2*Zx-int(X[j]); Dy=2*Zy-int(Y[j])
            assert Dx%2==Dy%2==1 and y*Dx-x*Dy>=2
            G=Dx*Dx+Dy*Dy-4*(Zx*Dx+Zy*Dy)+4*abs(m)-2
            assert G%8==0 and G>=8*d
            assert height-pref[k]<=L-d
    # Generate the entire tau path from all points where its slope changes.
    events=np.unique(np.r_[grid,np.arange(1,M,q,dtype=np.int64),np.arange(1,M,r,dtype=np.int64),M])
    weights=tau(events,p,q,r)
    assert np.all(weights>=tmin)
    assert np.array_equal(weights,tau(M-events,p,q,r))
    # Every genuine maximum plateau contains one of the cell roofs.
    neq=np.r_[True,weights[1:]!=weights[:-1]]
    starts=np.flatnonzero(neq)
    ends=np.r_[starts[1:]-1,len(events)-1]
    ev,ww=events[neq],weights[neq]
    roof_positions=np.array([z[0] for z in roofs])
    roof_heights=np.array([z[1] for z in roofs])
    for j in range(1,len(ww)-1):
        if ww[j]>ww[j-1] and ww[j]>ww[j+1]:
            lo,hi=events[starts[j]],events[ends[j]]
            k=np.searchsorted(roof_positions,lo)
            assert k<len(roofs) and roof_positions[k]<=hi and roof_heights[k]==ww[j]
    sg=np.sign(np.diff(ww)); extrema=np.r_[True,sg[:-1]!=sg[1:],True]
    bs=persistent_bars(ww[extrema])
    assert max(bs)==L and bs[L]==1
    assert all(bs.get(i,0)==0 for i in range(L-d+1,L))
    if full:
        ns=np.arange(M,dtype=np.int64); dd=delta(ns,p,q,r)
        assert np.all(np.abs(dd)<=1) and np.array_equal(dd,-dd[::-1])
        tf=np.r_[0,np.cumsum(dd)]
        assert np.array_equal(tf,tau(np.arange(M+1,dtype=np.int64),p,q,r))
        assert np.array_equal(tf[events],weights)
        # Independent semigroup characterization for every integer, including zeros.
        N=M-1; S=np.zeros(M,dtype=np.int8)
        AA,BB,CC=p*q,p*r,q*r
        for i in range(N//AA+1):
            for j in range((N-i*AA)//BB+1):
                S[i*AA+j*BB:N+1:CC]=1
        assert np.array_equal(dd,S-S[::-1])
    print((h,s),'checked',len(grid),'p-grid points,',len(events),'slope events;',
          'top=',[(ell,bs.get(ell,0)) for ell in range(L,L-d,-1)],flush=True)

def check_arithmetic_lemma():
    # Exhaust the entire Z-strip for (h,s)=(2,1), and an odd D box.
    h,s=2,1
    _,p,q,r=pars(h,s); v=4*h*s-1; x=v+2*h; y=2*s+1
    Ds=np.array([(a,b) for a in range(-19,20,2) for b in range(-19,20,2)],dtype=np.int64)
    Ds=Ds[y*Ds[:,0]-x*Ds[:,1]>=2]
    for i in range(-p//2,p//2+1):
        for j in range(-p//2,p//2+1):
            Zx,Zy=2*s*i-j,-v*i+2*h*j
            if y*Zx-x*Zy>=0: continue
            G=np.sum(Ds*Ds,axis=1)-4*(Zx*Ds[:,0]+Zy*Ds[:,1])+4*abs(x*Zx+y*Zy)-2
            assert np.all(G%8==0) and np.all(G>=8*min(h,s+1))
    # All four elementary inequalities used in the proof, in a larger box.
    for h in range(2,10):
        for a in range(-51,52,2):
            for b in range(-51,52,2):
                e=a-2*h*b
                if e>=1:
                    norm=a*a+b*b
                    assert norm+4*e+2>=8*h
                    assert norm-4*b>=6
                    assert norm+4*b+4*(e-1)>=6
                    assert norm+8*b+4*(e-1)>=2
    print('Arithmetic lemma and its elementary bounds independently checked.')

if __name__=='__main__':
    symbolic_checks()
    check_arithmetic_lemma()
    for h,s in [(2,1),(2,2),(2,3),(3,1),(3,2),(4,1),(4,2),(4,3)]:
        check_case(h,s,full=(h,s) in [(2,1),(3,1)])
