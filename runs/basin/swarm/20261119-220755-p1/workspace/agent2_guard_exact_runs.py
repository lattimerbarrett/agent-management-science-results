import numpy as np,time
from pathlib import Path
z=np.load('workspace/agent2_rational_positive_eq_0.4.npz');base=z['base'];f=z['f'];N=float(z['N']);mus=z['mus'];yeq=z['y'];guards=np.array([-.8,1.7]);nodes=np.r_[base,mus,guards];J=z['J'];ev,evec=np.linalg.eig(J);v=evec[:,np.argmax(ev.imag)].real;v/=np.linalg.norm(v)
ds=np.array([np.prod([a-b for b in base if a!=b]) for a in base]);powers=np.array([nodes**j for j in range(8)]).T
configs=[];logs=[];eps=.001
for amp in [0.,.001,.01]:
 for C in [1e-4,.01,1.,100.]:
  yy=yeq+amp*v;theta=-yy[0];ww=yy[1:5];ZZ=yy[-2:];fp=f.copy();fp[:-1]+=eps*ww
  b=(base-theta)/(ds*np.polynomial.polynomial.polyval(base,fp));b/=b.sum();out=np.r_[eps**2*ZZ,eps**2*np.ones(2)*C]
  p=np.r_[b*(1-out.sum()),out];assert min(p)>0
  logs.append(np.log(p));configs.append((amp,C))
lp=np.array(logs);B=len(configs);samples=[];t=time.time();check={0,100,1000,10000,100000,300000,1000000}
for k in range(1000001):
 shift=lp.max(axis=1);p=np.exp(lp-shift[:,None]);p/=p.sum(axis=1)[:,None]
 m=p@powers;M=np.empty((B,4,4))
 for i in range(4):
  for j in range(4):M[:,i,j]=m[:,i+j]
 co=np.linalg.solve(M,-m[:,4:8,None])[:,:,0]
 q=nodes[None,:]**4+co[:,0,None]+co[:,1,None]*nodes[None,:]+co[:,2,None]*nodes[None,:]**2+co[:,3,None]*nodes[None,:]**3
 norms=(p*q*q).sum(axis=1)
 if k in check:
  samples.append((k,p.copy(),co.copy(),lp.copy(),norms.copy()));print('k',k,'elapsed',time.time()-t,flush=True)
  for j in range(B):print(configs[j],'N',round(norms[j],9),'p',np.round(p[j],6),'logsneg',np.round(lp[j,6:8],2),flush=True)
 if k==1000000:break
 lp+=2*np.log(abs(q));lp-=lp.max(axis=1)[:,None]
np.savez('workspace/agent2_guard_exact_runs.npz',nodes=nodes,configs=np.array(configs),steps=np.array([v[0] for v in samples]),p=np.array([v[1] for v in samples]),co=np.array([v[2] for v in samples]),lp=np.array([v[3] for v in samples]),N=np.array([v[4] for v in samples]))
Path('workspace/agent2_guard_exact_runs.py').write_text(Path('scratchpad.py').read_text())
