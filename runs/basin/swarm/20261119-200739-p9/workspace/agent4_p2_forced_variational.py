import numpy as np
from scipy.optimize import minimize
from pathlib import Path
import json,time
rng=np.random.default_rng(41629)

def setup(N,target):
    d=np.arange(N)[:,None]-np.arange(N)[None,:]
    k=np.abs(d).astype(float)
    xl=lambda x: np.where(x>0,x*np.log(np.maximum(x,1e-200)),0.)
    H=np.sign(d)*(xl(k+1)-2*xl(k)+xl(np.maximum(k-1,0)))/np.pi
    masks=[]
    for start in range(N):
        for length in range(1,N+3):
            z=np.zeros(N)
            for j in range(length):z[(start+j)%N]+=1/length
            masks.append(z)
    P=np.array(masks)
    def evaluate(z,ret=False):
        par=np.zeros((N,3));par[1:]=z.reshape(N-1,3)
        M=np.zeros((N,2,2));M[:,0,0]=np.exp(par[:,0]);M[:,1,1]=np.exp(par[:,1]);M[:,0,1]=M[:,0,0]*par[:,2]
        inv=np.linalg.inv(M)
        G=np.einsum('iab,jbc->ijac',M,inv)
        S=np.sum(G*G,axis=(2,3)); det=np.linalg.det(G)
        K2=(S+np.sqrt(np.maximum(0.,S*S-4*det*det)))/2
        chars=np.einsum('ai,ij,aj->a',P,K2,P)
        C=np.max(chars)
        T=(H[:,:,None,None]*G).transpose(0,2,1,3).reshape(2*N,2*N)
        norm=np.linalg.svd(T,compute_uv=False)[0]
        val=np.log(norm)-np.log(C)
        return (norm,C,val,par) if ret else -np.log(norm)+30*(np.log(C/target))**2
    return evaluate

results=[]
start=time.time()
for N,target in [(16,10),(16,100),(32,10),(32,100)]:
    f=setup(N,target)
    best=None
    for trial in range(2):
        z=rng.normal(size=3*(N-1))*.8
        opt=minimize(f,z,method='L-BFGS-B',bounds=[(-5,5),(-5,5),(-8,8)]*(N-1),options={'maxiter':100,'ftol':1e-9,'maxls':25})
        out=f(opt.x,True)
        if best is None or out[2]>best[2]:best=out
        print('N',N,'trial',trial,'norm,char,logratio',out[:3],'iterations',opt.nit,flush=True)
    results.append({'N':N,'norm':float(best[0]),'characteristic_aligned':float(best[1]),'logratio':float(best[2]),'parameters':best[3].tolist()})
Path('workspace/agent4_p2_forced_variational.json').write_text(json.dumps(results,indent=2))
Path('workspace/agent4_p2_forced_variational.py').write_text(Path(__file__).read_text())
print('Done in',time.time()-start)
