"""Exact checks of the minimal-support involution for restarted CG directions.
Run with python; requires SymPy. All assertions are exact rational identities.
"""
import sympy as S

def monic_map(lam,w,s):
    H=S.Matrix(s,s,lambda i,j:sum(w[t]*lam[t]**(i+j) for t in range(len(lam))))
    h=S.Matrix([sum(w[t]*lam[t]**(s+j) for t in range(len(lam))) for j in range(s)])
    c=H.inv()*h
    q=[S.factor(lam[t]**s-sum(c[j]*lam[t]**j for j in range(s))) for t in range(len(lam))]
    beta2=S.factor(sum(wi*qi**2 for wi,qi in zip(w,q)))
    wp=[S.factor(wi*qi**2/beta2) for wi,qi in zip(w,q)]
    return wp,q,beta2

for s in range(1,7):
    lam=list(map(S.Integer,range(1,s+2)))
    raw=[S.Integer((i+1)**2+2) for i in range(s+1)]
    w=[a/sum(raw) for a in raw]
    wp,q,beta2=monic_map(lam,w,s)
    wpp,p,beta2p=monic_map(lam,wp,s)
    assert wpp==w
    assert beta2==beta2p
    assert all(S.factor(qi*pi-beta2)==0 for qi,pi in zip(q,p))
    # Reciprocal weights formula from the barycentric null vector.
    deriv=[S.prod(li-lj for j,lj in enumerate(lam) if j!=i) for i,li in enumerate(lam)]
    reciprocals=[1/(wi*di**2) for wi,di in zip(w,deriv)]
    check=[S.factor(a/sum(reciprocals)) for a in reciprocals]
    assert wp==check
print('All exact minimal-support identities verified for s=1,...,6.')
