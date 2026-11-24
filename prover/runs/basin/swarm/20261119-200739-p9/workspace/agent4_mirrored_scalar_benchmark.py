import numpy as np,mpmath as mp
from pathlib import Path
mp.mp.dps=70
out=[]
for N in [4,8,16,32]:
    # cells negative mirrored annuli, central[-1,1], positive annuli
    edges=[-2**k for k in range(N, -1,-1)]+[1]+[2**k for k in range(1,N+1)]
    J=len(edges)-1
    lens=np.diff(np.array(edges,dtype=float))
    levels=np.r_[np.arange(N-1,-1,-1),0,np.arange(N)]
    a=1-1/N
    weights=2.**(a*levels)
    M=np.zeros((J,2,2));M[:,0,0]=np.sqrt(weights);M[:,1,1]=1/np.sqrt(weights)
    G=np.einsum('iab,jbc->ijac',M,np.linalg.inv(M))
    kernel=np.maximum(weights[:,None]/weights[None,:],weights[None,:]/weights[:,None])
    C=0.
    for start in range(J):
        z=np.zeros(J)
        for k in range(1,J+3):
            idx=(start+k-1)%J;z[idx]+=lens[idx]
            pr=z/z.sum();C=max(C,pr@kernel@pr)
    phi=lambda t:mp.mpf(t)*mp.log(abs(t)) if t else mp.mpf(0)
    H=np.zeros((J,J))
    for i in range(J):
        for j in range(i):
            x,y=edges[i:i+2];u,v=edges[j:j+2]
            val=(phi(y-u)-phi(x-u)-phi(y-v)+phi(x-v))/(mp.pi*mp.sqrt(mp.mpf(int(lens[i]))*mp.mpf(int(lens[j]))))
            H[i,j]=float(val);H[j,i]=-float(val)
    T=(H[:,:,None,None]*G).transpose(0,2,1,3).reshape(2*J,2*J)
    norm=np.linalg.svd(T,compute_uv=False)[0]
    print('Nscales',N,'cells',J,'Ap_grid',C,'Hnorm',norm,'norm/char',norm/C,flush=True)
    out.append((N,J,C,norm))
Path('workspace/agent4_mirrored_scalar_benchmark.txt').write_text(str(out))
Path('workspace/agent4_mirrored_scalar_benchmark.py').write_text(Path(__file__).read_text())
