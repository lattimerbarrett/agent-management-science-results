import numpy as np
# Eight active inverse-polynomial nodes and one minus-one-neutral node.
x=np.r_[np.array([-8.,-7.,-4.,-1.,1.,4.,7.,8.])/8,np.sqrt((65-np.sqrt(2529))/2)/8]
s=4;n=len(x);V=x[:,None]**np.arange(s)
P0=x**4-65*x*x/64+424/4096
H=360/4096;delta=H/np.sqrt(2);C=delta**2
p=P0-delta;q=P0+delta
w0=np.r_[np.where(P0[:8]>0,(1+1/np.sqrt(2))/8,(1-1/np.sqrt(2))/8),0.]
assert np.max(abs(p[:8]*q[:8]-C))<1e-15
assert abs(p[-1]*q[-1]+C)<1e-15
assert np.max(abs(V.T@(w0*p)))<1e-15

def weightjet(ws,ref):
    order=len(ws)-1
    Ms=[V.T@(w[:,None]*V) for w in ws]
    ps=[ref]+[None]*order
    cs=[np.zeros(s)]
    for j in range(1,order+1):
        rhs=V.T@(ws[j]*ref)
        for l in range(1,j):rhs+=Ms[l]@cs[j-l]
        cs.append(-np.linalg.solve(Ms[0],rhs))
        ps[j]=V@cs[j]
    raw=[np.zeros(n) for j in range(order+1)]
    for j in range(order+1):
        for a in range(j+1):
            for b in range(j-a+1):
                c=j-a-b
                raw[j]+=ws[a]*ps[b]*ps[c]
    den=[r.sum() for r in raw];out=[]
    for j in range(order+1):
        v=raw[j].copy()
        for l in range(1,j+1):v-=den[l]*out[j-l]
        out.append(v/den[0])
    return out

def ode(t,z):
    w=z[:n];hco=z[n:n+s];amp=z[-1];h=V@hco
    u=w*p*h
    w2=amp**2*(np.eye(n)[-1]-w)
    ws=[w,u,w2,np.zeros(n)]
    out=weightjet(weightjet(ws,p),q)
    b=out[1]-u
    G=V.T@((w*p*p)[:,None]*V)
    hd=np.linalg.solve(G,V.T@(p*(out[2]-w2-b*p*h)))
    ad=out[3][-1]/(2*amp) if amp else 0.
    return np.r_[b,hd,ad]

if __name__=='__main__':
    rng=np.random.default_rng(7);h=rng.normal(size=s);amp=.2;u=w0*p*(V@h);w2=amp**2*(np.eye(n)[-1]-w0)
    out=weightjet(weightjet([w0,u,w2,np.zeros(n)],p),q)
    assert np.linalg.norm(out[0]-w0)<1e-12
    assert abs(out[1][-1])<1e-12 and abs(out[2][-1]-amp**2)<1e-12
    print('minus-one blowup first/second jets checked',np.linalg.norm(ode(0,np.r_[w0,h,amp])))
