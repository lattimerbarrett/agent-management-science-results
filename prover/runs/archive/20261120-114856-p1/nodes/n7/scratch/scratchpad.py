import numpy as np
rng=np.random.default_rng(35)
lam=np.array([.2,.4,.9,1.3,1.9,2.2,2.8])
s=3
y=rng.normal(size=len(lam)); y/=np.linalg.norm(y)
Ds=[]; hs=[]; Ps=[]; ws=[]
for k in range(100):
    K=np.array([lam**j*y for j in range(s+1)]).T
    Q,R=np.linalg.qr(K)
    Ds.append([np.prod(np.diag(R)[:j]**2) for j in range(1,s+2)])
    Ps.append(np.linalg.solve(R[:s,:s], -R[:s,s]))
    hs.append(R[s,s]**2)
    ws.append(y*y)
    y=Q[:,s]*np.sign(R[s,s])
Ds=np.array(Ds)
for j in range(1,s+2):
    print('D',j, Ds[:8,j-1])
for j in range(1,s+2):
    for l in range(1,s+2):
        v=Ds[:-1,j-1]*Ds[1:,l-1]
        d=np.diff(v[::2]); scale=max(abs(v))
        if np.all(d>=-1e-9*scale) or np.all(d<=1e-9*scale):
            print('product',j,l, 'increasing' if d.sum()>0 else 'decreasing')
print('hs',hs[:8])
ws=np.array(ws); hs=np.array(hs)
for a in [-3.,-1.,0.,3.,5.]:
    vals=[]
    for k in range(len(hs)-1):
        pa=a**s+sum(Ps[k][j]*a**j for j in range(s))
        m0=np.sum(ws[k]/(lam-a)); m1=np.sum(ws[k+1]/(lam-a))
        vals.append(hs[k]*m1/(pa*pa*m0))
    print('shift',a,'minimum increment',np.min(np.diff(vals)),'limit',vals[-1])
print('even spectral weights near limit:')
print(ws[-6::2])
print('even two-step change', np.max(abs(ws[-2]-ws[-4])))
np.savez('moments.npz',Ds=Ds,hs=hs,Ps=Ps,ws=ws,lam=lam)
