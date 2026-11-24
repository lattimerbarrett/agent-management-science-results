from pathlib import Path
old=Path('workspace/agent2_s3_edge_bvp.py').read_text();exec(old.split('mesh=np.linspace')[0])
def decode(a):
 y=a.copy();y[0]=-1-expit(a[0]);y[-2:]=np.exp(np.clip(a[-2:],-700,80));return y

def field(a):
 th=1+expit(a[0]);w=a[1:4];Z=np.exp(np.clip(a[-2:],-700,80));H=ob.nodes-th;wv=ob.V@w
 p=ob.N*H/(ob.d*ob.fv);pp=H*ob.fv/ob.d;M=ob.V.T@(p[:,None]*ob.V);Mp=ob.V.T@(pp[:,None]*ob.V)
 dg=np.linalg.solve(Mp,-ob.V.T@((H*wv/ob.d)*ob.gv));dN=ob.N**2*np.sum(H*wv/(ob.d*ob.fv**2));ratio=(ob.gv*wv+ob.fv*(ob.V@dg)-dN)/ob.N
 wf=-np.linalg.solve(M,ob.V.T@(p*ob.fv*ratio**2)+4*ob.Vmu.T@(Z*ob.fm))
 i=np.argmin(abs(ob.nodes-(1. if th<1.5 else 2.)));xdot=2*ratio[i]/(2-th) if th<1.5 else -2*ratio[i]/(th-1)
 growth=2+2*((ob.Vmu@w)/ob.fm+(ob.Vmu@dg)/ob.gm)-2*dN/ob.N
 return np.r_[xdot,w+wf,growth]
def bc(a,b):
 aa=decode(a)
 return np.r_[aa[0]+1.5,ob(0,aa,True)[0],a[-2:]-np.log(.001),b[-2:]-np.log(.001)]
def dn(y):
 th=-y[0];p=ob.N*(ob.nodes-th)/(ob.d*ob.fv);return np.sum(p*(ob.gv-ob.fv)*(ob.V@y[1:4]))
mesh=np.linspace(0,1,101);ys=np.tile(np.r_[0.,[-.55,0.,0.],np.log(.001),np.log(.001)][:,None],(1,len(mesh)))
for T in [.2,.4,.6,1.,1.5,2.,2.5,3.,4.,5.,6.,8.,10.]:
 try:
  sol=solve_bvp(lambda t,a:T*np.column_stack([field(a[:,j]) for j in range(a.shape[1])]),bc,mesh,ys,max_nodes=6000,tol=8e-5)
  yy=np.column_stack([decode(sol.y[:,j]) for j in range(sol.y.shape[1])]);th=-yy[0];ds=np.array([dn(yy[:,j]) for j in range(yy.shape[1])]);print('T',T,'status',sol.status,'res',max(sol.rms_residuals),'bc',max(abs(bc(sol.y[:,0],sol.y[:,-1]))),'theta',min(th),max(th),'deltaNrange',min(ds),max(ds),flush=True)
  np.savez('workspace/agent2_s3_Zreturn_bvp_T'+str(T)+'.npz',t=sol.x*T,a=sol.y,yy=yy,deltaN=ds)
  if sol.status!=0:break
  mesh=np.linspace(0,1,501);ys=sol.sol(mesh)
 except Exception as e:print('FAILED',T,type(e),e);break
Path('workspace/agent2_s3_Zreturn_bvp.py').write_text(Path('scratchpad.py').read_text())
