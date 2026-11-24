import numpy as np
def haar_shift(leaves, kind='down'):
    N=len(leaves);l=np.array([a for a,b,W in leaves]);r=np.array([b for a,b,W in leaves]);length=r-l
    def rec(a,b):
        inds=np.where((l>=a-1e-15)&(r<=b+1e-15))[0]
        if len(inds)==1:return None
        mid=(a+b)/2
        h=np.zeros(N)
        for i in inds:h[i]=np.sqrt(length[i]/(b-a))*(1 if r[i]<=mid+1e-15 else -1)
        left=rec(a,mid);right=rec(mid,b)
        if left is not None and right is not None:
            if kind=='down':S[:]+=np.outer((left-right)/np.sqrt(2),h)
            elif kind=='swap':S[:]+=np.outer(left,right)-np.outer(right,left)
        return h
    S=np.zeros((N,N));rec(0,1);return S

def weighted_scalar_matrix(leaves,S):
    N=len(leaves);B=[];C=[]
    for l,r,W in leaves:
        d,U=np.linalg.eigh(W);B.append((U*np.sqrt(d))@U.T);C.append((U/np.sqrt(d))@U.T)
    return np.einsum('ij,iab,jbc->iajc',S,np.array(B),np.array(C)).reshape(2*N,2*N)

def replenish_tree(Q,N,alpha,order='reverse'):
    leaves=[];p=2.;S=3-1/Q;s=(S+np.sqrt(S*S-8))/2;t=2/s
    def emit(a,b,th,l,h):
        c,z=np.cos(th),np.sin(th);R=np.array([[c,-z],[z,c]])
        leaves.append((l,l+h,R@np.diag([a,b])@R.T))
    def rec(a,b,th,l,h,n):
        if n==0:
            rt=np.sqrt(a*a-a/b);a1=a+rt;a2=(a/b)/a1
            emit(a1,1/a1,th,l,h/2);emit(a2,1/a2,th,l+h/2,h/2);return
        amp=np.sqrt(Q/2);gap=np.sqrt((a-b)**2+4*amp**2);aa=(a+b+gap)/2;bb=(Q/2)/aa
        ang=.5*np.arctan2(2*amp,a-b)
        for sig,k in [(-1,0),(1,1)]:
            theta=th+sig*ang;left=l+k*h/2;length=h/2
            active=0 if order=='same' else k if order=='opposite' else 1-k
            for j in [0,1]:
                if j==active:rec(s*aa,t*bb,theta,left+j*length/2,length/2,n-1)
                else:emit((2-s)*aa,(2-t)*bb,theta,left+j*length/2,length/2)
    rec(alpha,Q/alpha,0,0,1,N)
    return sorted(leaves,key=lambda z:z[0])

