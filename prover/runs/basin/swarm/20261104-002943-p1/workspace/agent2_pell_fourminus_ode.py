import numpy as np
D=np.load('workspace/agent2_pell_fourminus_params.npz')
x=D['x'];p=D['p'];q=D['q'];C=float(D['C']);w0=D['w0'];s=4;na=8;nm=4;n=len(x);V=x[:,None]**np.arange(s)

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
    w=z[:n];hco=z[n:n+s];amp=z[n+s:];h=V@hco
    u=w*p*h
    w2=np.r_[np.zeros(na),amp**2]-np.dot(amp,amp)*w
    ws=[w,u,w2,np.zeros(n)]
    out=weightjet(weightjet(ws,p),q)
    b=out[1]-u
    G=V.T@((w*p*p)[:,None]*V)
    hd=np.linalg.solve(G,V.T@(p*(out[2]-w2-b*p*h)))
    ad=np.divide(out[3][na:],2*amp,out=np.zeros(nm),where=amp!=0)
    return np.r_[b,hd,ad]

