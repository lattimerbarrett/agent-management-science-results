import numpy as np,mpmath as mp
from scipy.optimize import minimize
from pathlib import Path
import json,time
rng=np.random.default_rng(41639)
mp.mp.dps=60

def setup(N,target):
    lens=np.array([2.**k for k in range(N)])
    edges=[2**k-1 for k in range(N+1)]
    phi=lambda t:mp.mpf(t)*mp.log(abs(t)) if t else mp.mpf(0)
    H=np.zeros((N,N))
    for i in range(N):
        for j in range(i):
            a,b=edges[i:i+2];c,d=edges[j:j+2]
            val=(phi(b-c)-phi(a-c)-phi(b-d)+phi(a-d))/(mp.pi*mp.sqrt(mp.mpf(int(lens[i]))*mp.mpf(int(lens[j]))))
            H[i,j]=float(val);H[j,i]=-float(val)
    ls=np.r_[lens[::-1],lens,lens*2**N]
    types=np.r_[np.zeros(N,dtype=int),np.arange(N),np.full(N,N-1,dtype=int)]
    P=[]
    for start in range(3*N):
        counts=np.zeros(N)
        for end in range(start,3*N):
            counts[types[end]]+=ls[end]
            P.append(counts.copy()/counts.sum())
    for i in range(N-1):
        z=np.zeros(N);z[i:i+2]=.5;P.append(z)
    P=np.array(P)
    def evaluate(z,ret=False):
        par=np.zeros((N,3));par[1:]=z.reshape(N-1,3)
        M=np.zeros((N,2,2));M[:,0,0]=np.exp(par[:,0]);M[:,1,1]=np.exp(par[:,1]);M[:,0,1]=M[:,0,0]*par[:,2]
        G=np.einsum('iab,jbc->ijac',M,np.linalg.inv(M))
        S=np.sum(G*G,axis=(2,3));det=np.linalg.det(G)
        K2=(S+np.sqrt(np.maximum(0.,S*S-4*det*det)))/2
        C=np.max(np.einsum('ai,ij,aj->a',P,K2,P))
        T=(H[:,:,None,None]*G).transpose(0,2,1,3).reshape(2*N,2*N)
        norm=np.linalg.svd(T,compute_uv=False)[0]
        val=np.log(norm)-np.log(C)
        return (norm,C,val,par) if ret else -np.log(norm)+30*np.log(C/target)**2
    return evaluate

results=[];start=time.time()
for N,target in [(12,10),(12,100),(20,10),(20,100)]:
    f=setup(N,target);best=None
    for trial in range(2):
        z=rng.normal(size=3*(N-1))*.6
        opt=minimize(f,z,method='L-BFGS-B',bounds=[(-6,6),(-6,6),(-10,10)]*(N-1),options={'maxiter':100,'ftol':1e-9,'maxls':25})
        out=f(opt.x,True)
        if best is None or out[2]>best[2]:best=out
        print('N',N,'trial',trial,'norm,char,logratio',out[:3],'iterations',opt.nit,flush=True)
    results.append({'N':N,'norm':float(best[0]),'characteristic_aligned':float(best[1]),'logratio':float(best[2]),'parameters':best[3].tolist()})
Path('workspace/agent4_p2_geometric_variational.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent4_p2_geometric_variational.py').write_text(Path(__file__).read_text())
print('Done in',time.time()-start)
