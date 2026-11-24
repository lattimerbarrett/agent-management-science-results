from pathlib import Path
c=Path('workspace/agent2_criticalZ_bvp.py').read_text();c=c[:c.index('prev=np.load')]
exec(c)
def dn(y):
 th=-y[0];H=ob.nodes-th;p=ob.N*H/(ob.d*ob.fv);return np.sum(p*(ob.gv-ob.fv)*(ob.V@y[1:5]))
neq=dn(eq);zeq=sum(eq[-2:]);print('NdefEQ',neq,'Zeq',zeq)
def bc(a,b):
 ca=BI@(decode(a)-eq);tar=np.r_[eps,0.,0.,0.,0.];end=decode(b)
 return np.r_[ca[:5]-tar,dn(end)-neq,np.log(sum(end[-2:])/zeq)]
prev=np.load('workspace/agent2_radial_bvp_T2.npz');mesh=np.linspace(0,1,201);ys=np.array([np.interp(mesh,prev['t']/2,row) for row in prev['a']])
for T in range(2,18):
 try:
  sol=solve_bvp(lambda t,a:T*np.column_stack([field(a[:,j]) for j in range(a.shape[1])]),bc,mesh,ys,max_nodes=10000,tol=8e-5)
  yy=np.column_stack([decode(sol.y[:,j]) for j in range(sol.y.shape[1])]);th=-yy[0];print('T',T,'status',sol.status,'res',max(sol.rms_residuals),'bc',max(abs(bc(sol.y[:,0],sol.y[:,-1]))),'theta',min(th),max(th),'xi',min(sol.y[0]),max(sol.y[0]),'wend',np.linalg.norm(yy[1:5,-1]),'Zend',yy[-2:,-1],flush=True)
  np.savez('workspace/agent2_criticalNZ_bvp_T'+str(T)+'.npz',t=sol.x*T,a=sol.y,yy=yy,eq=eq,B=B,eps=eps)
  if sol.status!=0:break
  mesh=np.linspace(0,1,1001);ys=sol.sol(mesh)
 except Exception as e:print('FAILED',T,type(e),e);break
Path('workspace/agent2_criticalNZ_bvp.py').write_text(Path('scratchpad.py').read_text())
