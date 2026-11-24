from pathlib import Path
old=Path('workspace/agent2_radial_bvp.py').read_text();exec(old.split('mesh=np.linspace')[0])
def decode(a):
 y=a.copy();y[0]=-expit(a[0]);y[-2:]=np.exp(np.clip(a[-2:],-700,80));return y

def field(a):
 th=expit(a[0]);w=a[1:5];Z=np.exp(np.clip(a[-2:],-700,80));H=ob.nodes-th;wv=ob.V@w
 p=ob.N*H/(ob.d*ob.fv);pp=H*ob.fv/ob.d;M=ob.V.T@(p[:,None]*ob.V);Mp=ob.V.T@(pp[:,None]*ob.V)
 dg=np.linalg.solve(Mp,-ob.V.T@((H*wv/ob.d)*ob.gv));dN=ob.N**2*np.sum(H*wv/(ob.d*ob.fv**2));ratio=(ob.gv*wv+ob.fv*(ob.V@dg)-dN)/ob.N
 wf=-np.linalg.solve(M,ob.V.T@(p*ob.fv*ratio**2)+4*ob.Vmu.T@(Z*ob.fm))
 i=np.argmin(abs(ob.nodes-(0. if th<.5 else 1.)));xdot=2*ratio[i]/(1-th) if th<.5 else -2*ratio[i]/th
 growth=2+2*((ob.Vmu@w)/ob.fm+(ob.Vmu@dg)/ob.gm)-2*dN/ob.N
 return np.r_[xdot,w+wf,growth]
def bc(a,b):
 ca=BI@(decode(a)-eq);tar=np.r_[eps,0.,0.,0.,0.]
 return np.r_[ca[:5]-tar,b[-2:]-np.log(eq[-2:])]
prev=np.load('workspace/agent2_radial_bvp_T2.npz');mesh=np.linspace(0,1,201);ys=np.array([np.interp(mesh,prev['t']/2,row) for row in prev['a']])
for T in range(2,20):
 try:
  sol=solve_bvp(lambda t,a:T*np.column_stack([field(a[:,j]) for j in range(a.shape[1])]),bc,mesh,ys,max_nodes=10000,tol=8e-5)
  yy=np.column_stack([decode(sol.y[:,j]) for j in range(sol.y.shape[1])]);th=-yy[0];print('T',T,'status',sol.status,'res',max(sol.rms_residuals),'bc',max(abs(bc(sol.y[:,0],sol.y[:,-1]))),'theta',min(th),max(th),'xi',min(sol.y[0]),max(sol.y[0]),'wend',np.linalg.norm(yy[1:5,-1]),flush=True)
  np.savez('workspace/agent2_criticalZ_bvp_T'+str(T)+'.npz',t=sol.x*T,a=sol.y,yy=yy,eq=eq,B=B,eps=eps)
  if sol.status!=0:break
  mesh=np.linspace(0,1,1001);ys=sol.sol(mesh)
 except Exception as e:print('FAILED',T,type(e),e);break
Path('workspace/agent2_criticalZ_bvp.py').write_text(Path('scratchpad.py').read_text())
