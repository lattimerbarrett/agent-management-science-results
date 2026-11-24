import numpy as np

def tree(q,alpha=None,order="same"):
    if alpha is None: alpha=10*np.sqrt(q)
    leaves=[]
    def rec(a,b,theta,left,length,q):
        if q<=1+1e-10:
            c,s=np.cos(theta),np.sin(theta);R=np.array([[c,-s],[s,c]])
            leaves.append((left,left+length,R@np.diag([a,b])@R.T));return
        gap=np.sqrt((a-b)**2+4);T=a+b
        aa=(T+gap)/2;bb=(q-1)/aa
        ang=.5*np.arctan2(2,a-b)
        for sig,k in [(-1,0),(1,1)]:
            th=theta+sig*ang;l=left+k*length/2;h=length/2
            qq=q-1
            if qq<=1+1e-10:
                rec(aa,bb,th,l,h,qq);continue
            z=(5-1/qq)/2;stretch=(z+np.sqrt(z*z-4))/2
            active=0 if order=="same" else k if order=="opposite" else 1-k
            for j in [0,1]:
                if j==active: rec(stretch*aa,bb/stretch,th,l+j*h/2,h/2,qq)
                else: rec((2-stretch)*aa,(2-1/stretch)*bb,th,l+j*h/2,h/2,1)
    rec(alpha,q/alpha,0.,0.,1.,q)
    return sorted(leaves,key=lambda z:z[0])

def lower(leaves):
    N=len(leaves);ends=np.array([[l,r] for l,r,W in leaves]);lengths=ends[:,1]-ends[:,0]
    def F(t):
        out=np.zeros_like(t);mask=t!=0;out[mask]=t[mask]*(np.log(abs(t[mask]))-1);return out
    l=ends[:,0];r=ends[:,1]
    K=(F(r[:,None]-l[None,:])-F(l[:,None]-l[None,:])-F(r[:,None]-r[None,:])+F(l[:,None]-r[None,:]))/np.pi/np.sqrt(lengths[:,None]*lengths[None,:])
    np.fill_diagonal(K,0)
    B=[];C=[]
    for l,r,W in leaves:
        d,U=np.linalg.eigh(W);assert min(d)>0
        B.append((U*np.sqrt(d))@U.T);C.append((U/np.sqrt(d))@U.T)
    B=np.array(B);C=np.array(C)
    M=np.einsum('ij,iab,jbc->iajc',K,B,C).reshape(2*N,2*N)
    # normalized f=W^-1 e directional test ratios too
    vals=[]
    for e in np.eye(2):
        z=np.concatenate([np.sqrt(r-l)*c@e for (l,r,W),c in zip(leaves,C)])
        vals.append(np.linalg.norm(M@z)/np.linalg.norm(z))
    return M,vals
