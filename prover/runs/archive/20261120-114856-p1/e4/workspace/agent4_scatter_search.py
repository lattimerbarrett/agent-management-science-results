import numpy as np,itertools,json,os
from scipy.integrate import solve_ivp
rng=np.random.default_rng(209)
start=(0,0,0);cycles=[]
def dfs(path):
 for j in range(3):
  nn=list(path[-1]);nn[j]^=1;nn=tuple(nn)
  if nn==start and len(path)>=4:cycles.append(path+[start])
  elif nn not in path:dfs(path+[nn])
dfs([start])
def test(q,r,H):
 P=np.polymul(q,r);P[-1]-=H;lam=np.sort_complex(np.roots(P))
 if max(abs(lam.imag))>1e-7:return None
 lam=lam.real;f=np.vander(lam,4,increasing=True);qv=np.polyval(q,lam);rv=np.polyval(r,lam);verts={}
 for bits in itertools.product([0,1],repeat=3):
  ix=[0,1+bits[0],3+bits[1],5+bits[2],7];AA=np.vstack([np.ones(5),(qv[ix,None]*f[ix]).T]);w=np.zeros(8);w[ix]=np.linalg.solve(AA,np.r_[1.,np.zeros(4)]);verts[bits]=w
 def maps(w):
  G=f.T@(w[:,None]*f);Gp=f.T@((w*qv*qv/H)[:,None]*f);dr=-np.linalg.solve(Gp,G);df=rv[:,None]*f+qv[:,None]*f@dr;return G,df-w@df
 SS={};EM={bb:maps(ww)[1]for bb,ww in verts.items()}
 for aa in verts:
  for j in range(3):
   bb=list(aa);bb[j]^=1;bb=tuple(bb)
   if (bb,aa) in SS:SS[aa,bb]=np.linalg.inv(SS[bb,aa]);continue
   wa=verts[aa];wb=verts[bb];dw=wb-wa;ii=np.where((wa==0)&(wb>0))[0][0];act=np.where(wa+wb>0)[0]
   def fun(u,Y):
    w=wa+u*dw;G,Em=maps(w);arow=2*u*Em[ii]/H;B=np.linalg.solve(G,f[act].T@(qv[act]*dw[act]**2/w[act]))/4;return (-np.outer(B,arow)@Y.reshape(4,4)).ravel()
   sol=solve_ivp(fun,[1e-6,1-1e-6],np.eye(4).ravel(),rtol=2e-7,atol=1e-9);SS[aa,bb]=sol.y[:,-1].reshape(4,4)
 for cyc in cycles:
  MM=np.eye(4)
  for aa,bb in zip(cyc[:-1],cyc[1:]):MM=SS[aa,bb]@MM
  vals,U=np.linalg.eig(MM)
  for kk,rho in enumerate(vals):
   if abs(rho.imag)>1e-5 or not(.00001<rho.real<.999):continue
   v=U[:,kk].real;v/=np.linalg.norm(v);signs=[];allv=[v.copy()]
   for aa,bb in zip(cyc[:-1],cyc[1:]):
    ii=np.where((verts[aa]==0)&(verts[bb]>0))[0][0];signs.append(float(2*EM[aa][ii]@v/H));v=SS[aa,bb]@v;allv.append(v.copy())
   if min(signs)>1e-7 or max(signs)<-1e-7:return {'q':q.tolist(),'r':r.tolist(),'H':H,'lam':lam.tolist(),'cycle':cyc,'rho':float(rho.real),'v':U[:,kk].real.tolist(),'signs':signs,'allv':[v.tolist()for v in allv]}
 return None
for trial in range(1000):
 centers=np.sort(rng.uniform(-1,1,4));
 if min(np.diff(centers))<.1:continue
 qr=[];rr=[]
 for j,z in enumerate(centers):
  d=rng.uniform(.02,.2)*min(np.diff(centers))
  if rng.random()<.5:d=-d
  qr.append(z+d);rr.append(z-d)
 q=np.poly(qr);r=np.poly(rr);Q=np.polymul(q,r);critical=np.roots(np.polyder(Q));positive=[np.polyval(Q,z.real)for z in critical if abs(z.imag)<1e-7 and np.polyval(Q,z.real)>1e-9]
 if not positive:continue
 H=min(positive)*rng.uniform(.05,.8)
 try:result=test(q,r,H)
 except (np.linalg.LinAlgError,ValueError):continue
 if result:
  print('FOUND',trial,result,flush=True);json.dump(result,open('workspace/agent4_scatter_coprime_found.json','w'));break
 if trial%50==0:print('tested',trial,flush=True)
else:print('No candidates')
