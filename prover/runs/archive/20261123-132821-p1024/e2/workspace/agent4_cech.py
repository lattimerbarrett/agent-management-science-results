"""Exact finite-Cech rank checks over a finite prime field.
No predicted answer is used to construct the matrices.
"""
from collections import defaultdict
P=1000003

def inv(x): return pow(x%P,P-2,P)
def binom(a,q):
    v=1
    for j in range(q): v=v*(a-j)%P*inv(j+1)%P
    return v

def mul(a,b):
    c=defaultdict(int)
    for i,x in a.items():
        for j,y in b.items(): c[i+j]=(c[i+j]+x*y)%P
    return {i:x for i,x in c.items() if x}

def rank_cols(cols):
    piv={}
    for v in cols:
        while v:
            i=min(v)
            if i not in piv:
                a=inv(v[i]); piv[i]={j:x*a%P for j,x in v.items()}; break
            w=piv[i]; a=v[i]
            for j,x in w.items():
                z=(v.get(j,0)-a*x)%P
                if z:v[j]=z
                else:v.pop(j,None)
    return len(piv)

def h1(g,b,alpha=0,h=0,M=None,N=None):
    # h=0 for base O, h=1 for base T; alpha=0 or 1 for O or vertical log twist.
    r=(g+2)//3;k=g-r
    assert len(b)==r and any(b)
    m=max(j for j,x in enumerate(b) if x)
    pole=2*g-1 # use uniform bound, independent of zeros
    N=4*g-4 if N is None else N
    M=4*g+1 if M is None else M
    D=4*g+2;d=(2-2*g)*h
    low=[-M-(n//k)*max(0,pole-k) for n in range(N+1)]
    rows={(n,e):i for i,(n,e) in enumerate((n,e) for n in range(N+1) for e in range(low[n],0))}
    phi={-(2*g-1-2*j):x%P for j,x in enumerate(b) if x%P}
    pp=[{0:1}]
    for q in range(N//k):pp.append(mul(pp[-1],phi))
    cols=[]
    for n in range(N+1):
        beta=(alpha-n*inv(k))%P
        for eps in (0,1):
            basepole=(2*g+1)*eps
            maxi=(n+d-low[n]-basepole)//2
            for ii in range(maxi+1):
                s=basepole+2*ii; col={}
                for q in range((N-n)//k+1):
                    c=binom(beta,q)*pow(-k,q,P)%P
                    if not c:continue
                    nn=n+q*k
                    for pe,pv in pp[q].items():
                        e=n+d-s+q*k+pe
                        # sqrt(1-t^D) to exponent eps+h
                        for ell in range(max(0,(-1-e)//D+1)):
                            ee=e+D*ell
                            cc=c*pv%P*binom((eps+h)*inv(2)%P,ell)%P*((-1)**ell)%P
                            if not cc:continue
                            assert ee>=low[nn], (g,n,nn,ee,low[nn])
                            row=rows[(nn,ee)]
                            col[row]=(col.get(row,0)+cc)%P
                if col:cols.append(col)
    rank=rank_cols(cols)
    return len(rows)-rank

if __name__=='__main__':
    for g in range(2,10):
        r=(g+2)//3
        for m in range(r):
            b=[j+2 if j<=m else 0 for j in range(r)]
            hs=[h1(g,b,a,h) for a,h in [(0,0),(1,0),(0,1),(1,1)]]
            # Delta also includes rank of horizontal connecting homomorphism.
            print(g,m,hs,'four-term',hs[0]-hs[1]-hs[2]+hs[3],flush=True)
