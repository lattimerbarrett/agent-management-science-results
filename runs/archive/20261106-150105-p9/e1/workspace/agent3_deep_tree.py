import numpy as np, json, time, os

def branch(W,Q,depth):
    d,U=np.linalg.eigh(W); d=d[::-1]; U=U[:,::-1]; G=U@np.diag(np.sqrt(d))
    b=np.sqrt(1/Q); total=2.5; disc=total**2-4*(1+b*b)
    a=(total+np.sqrt(disc))/2; c=(total-np.sqrt(disc))/2
    P=G@np.array([[a,b],[b,c]])@G.T
    M=G@np.array([[a,-b],[-b,c]])@G.T
    L=G@np.diag([2-a,2-c])@G.T
    if depth==0:
        t=np.sqrt(1-1/Q)
        return [(G@np.array([[1.,t],[t,1.]])@G.T,.5),(G@np.array([[1.,-t],[-t,1.]])@G.T,.5)]
    return [(A,w/4) for A,w in branch(P,Q,depth-1)]+[(L,.25)]+[(A,w/4) for A,w in branch(M,Q,depth-1)]+[(L,.25)]

def compute(Q,depth):
    leaves=branch(np.diag([Q,1.]),Q,depth)
    n=len(leaves); weights=np.array([w for W,w in leaves]); edges=np.r_[0,np.cumsum(weights)]
    mats=np.array([W for W,w in leaves]); d,U=np.linalg.eigh(mats)
    Fs=np.einsum('nik,nk,njk->nij',U,np.sqrt(d),U); Bs=np.einsum('nik,nk,njk->nij',U,1/np.sqrt(d),U)
    def phi(t):
        return t*np.log(np.maximum(abs(t),1e-200))-t
    # K contains exact averaged Hilbert kernels on intervals, excluding diagonal.
    K=phi(edges[1:,None]-edges[None,:-1]); K-=phi(edges[:-1,None]-edges[None,:-1]); K-=phi(edges[1:,None]-edges[None,1:]); K+=phi(edges[:-1,None]-edges[None,1:]); K/=np.pi*np.sqrt(weights[:,None]*weights[None,:]); np.fill_diagonal(K,0.)
    def T(v): return np.einsum('nij,nj->ni',Fs,K@np.einsum('nij,nj->ni',Bs,v))
    def Tstar(v):return -np.einsum('nij,nj->ni',Bs,K@np.einsum('nij,nj->ni',Fs,v))
    rng=np.random.default_rng(8); v=rng.normal(size=(n,2)); v/=np.linalg.norm(v)
    for k in range(70):
        Tv=T(v); z=Tstar(Tv); v=z/np.linalg.norm(z)
    norm=np.linalg.norm(T(v))
    # Every endpoint interval and equal-mass adjacent pair gives lower proxy.
    prefix=np.concatenate([np.zeros((1,2,2)),np.cumsum(mats*weights[:,None,None],axis=0)])
    char=1.
    for i in range(n):
        av=(prefix[i+1:]-prefix[i])/(edges[i+1:]-edges[i])[:,None,None]
        char=max(char,float(np.max(np.linalg.det(av))))
        if i+1<n:char=max(char,float(np.linalg.det((mats[i]+mats[i+1])/2)))
    return {'Q':Q,'depth':depth,'leaves':n,'H_compression_norm_lower':float(norm),'A2_proxy_endpoint_lower':char,'det_leaf_max_error':float(np.max(abs(np.linalg.det(mats)-1)))}

results=[]
for Q,depth in [(2.,6),(3.,8),(4.,8),(4.,10),(8.,8),(8.,10)]:
    t=time.time(); result=compute(Q,depth); result['seconds']=time.time()-t; results.append(result); print(result,flush=True)
with open('workspace/agent3_deep_tree_results.json','w') as f:json.dump(results,f,indent=2)
with open('workspace/agent3_deep_tree.py','w') as f:f.write(open('scratchpad.py').read())
