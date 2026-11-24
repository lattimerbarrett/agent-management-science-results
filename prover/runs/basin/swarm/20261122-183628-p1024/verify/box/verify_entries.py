import sys
sys.path.insert(0,'agents/agent_1')
import scratchpad as team
from sage.all import QQ, LaurentSeriesRing, binomial
from collections import defaultdict

def check(g,b):
    mats,par=team.build(g,b)
    N,M,P,_=par
    r=(g+2)//3; k=g-r; h=2*g-2
    R=LaurentSeriesRing(QQ,'t',default_prec=8*(M+P)+100)
    t=R.gen(); s=(1-t**(4*g+2)).sqrt()
    a=-QQ(1)/2*t**(-h)*s
    phi=sum(QQ(b[j])*t**(-(2*g-1)+2*j) for j in range(r))
    psi=t**k*phi
    nongaps=[lam for lam in range(M+1) if lam%2==0 or lam>=2*g+1]
    fs=[t**(-lam)*s**(lam%2) for lam in nongaps]
    out=[defaultdict(QQ) for _ in range(3)]
    def add(F,which,m,n,rb=0,cb=0):
        for li,f in enumerate(fs):
            col=(cb*(N+1)+n)*len(fs)+li
            prod=F*f
            assert prod.valuation()>=-M-P
            for e in range(-M-P,0):
                c=prod[e]
                if c:
                    row=(rb*(N+1)+m)*(M+P)+e+M+P
                    out[which][row,col]+=c
    for n in range(N+1):
        for ell in range((N-n)//k+1):
            m=n+ell*k
            A=binomial(-QQ(n)/k,ell)*(-k*psi)**ell
            B=binomial(1-QQ(n)/k,ell)*(-k*psi)**ell
            Am=binomial(-QQ(n)/k,ell-1)*(-k*psi)**(ell-1) if ell else R(0)
            add(t**n*A,0,m,n)
            add(a*t**n*B,2,m,n)
            add(a*t**n*A,1,m,n)
            add(t**n*B,1,m,n,1,1)
            add(-a*t**(n-1)*A-a*t**(n+k)*phi.derivative()*Am,1,m,n,1,0)
    for i in range(3):
        out[i]={ij:c for ij,c in out[i].items() if c}
        assert out[i]==mats[i].dict(), (g,i)
    print('Independent Laurent-series entry match:',g,b, 'nonzeros',[len(x) for x in out])

check(2,[2])
check(4,[2,-3])
check(4,[0,1])
