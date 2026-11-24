import numpy as np
from scipy.special import logsumexp
rng=np.random.default_rng(713)

def run(lam, logw, N=20000):
    n=len(lam)
    d=np.array([1/(lam[i]*np.prod(lam[i]-np.delete(lam,i))) for i in range(n)])
    ld=np.log(np.abs(d)); hist=[]
    for k in range(N):
        h=2*ld-logw
        a=h+np.log(lam); a-=logsumexp(a)
        theta=np.dot(np.exp(a),lam)
        logw=2*ld+2*np.log(np.maximum(np.abs(lam-theta),1e-300))-logw
        logw-=logsumexp(logw)
        if k%100==0: hist.append(np.exp(logw))
    return np.array(hist), logw
def run_general(lam,w,N=10000):
    hist=[]
    lam=(lam-lam.mean())/(lam.max()-lam.min())
    for k in range(N):
        prev=np.zeros(len(lam)); p=np.ones(len(lam)); beta=0.
        for j in range(3):
            norm=np.dot(w,p*p)
            alpha=np.dot(w,lam*p*p)/norm
            new=(lam-alpha)*p-beta*prev
            beta=np.dot(w,new*new)/norm
            prev,p=p,new
        w=w*p*p
        w/=sum(w)
        if k%100==0: hist.append(w.copy())
    return np.array(hist)
best=[]
for t in range(100):
    lam=np.sort(np.exp(rng.uniform(0,3,6))) if t>=20 else np.arange(1.,7.)
    w=rng.dirichlet(np.ones(6))
    h=run_general(lam,w,5000)
    score=np.linalg.norm(h[-1]-h[-11])
    best.append((score,lam,w,h[-1],h[-11]))
best.sort(key=lambda a:-a[0])
for row in best[:5]: print(row)
np.savez('best6.npz',lam=best[0][1],w=best[0][2])
