"""Generate the nonrigorous dyadic Hermite certificate seed.
The resulting data are only an approximation; rigor is supplied independently by
agent4_floquet_pointwise and agent2_floquet_budget_check. Does not self-overwrite.
"""
import sys;sys.path.insert(0,'workspace')
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from scipy.linalg import expm

def generate(inputfile='workspace/agent1_actualQ_-0.72.npz',outputfile='workspace/agent2_generated_frames_recheck.npz'):
 z=np.load(inputfile);dd=dict(z);dd['base']=np.array([-3.,-1,0,1,2,3]);dd['L']=np.array(.06);np.savez('workspace/agent2_tmpcycle.npz',**dd)
 ns={};exec(Path('workspace/agent2_genuine_field.py').read_text().replace('workspace/agent1_GENUINE_s4_periodic.npz','workspace/agent2_tmpcycle.npz'),ns);ja=ns['jac']
 Y=z['y'].copy();Y[0]*=-1;Y[:,-1]=Y[:,0];cs=CubicSpline(z['x'],Y,axis=1,bc_type='periodic');T=float(z['p'][0]);B=z['B'].copy();B[0]*=-1;BI=np.linalg.inv(B);sig=np.diag([-1,1,1,1,1,1,1]);jm=np.linspace(0,1,4001);jvals=[]
 for t in jm:
  y=cs(t).copy();y[0]*=-1;jvals.append(T*BI@sig@ja(y)@sig@B)
 js=CubicSpline(jm,np.stack(jvals,axis=2),axis=2)
 sol=solve_ivp(lambda t,a:(js(t)@a.reshape(7,7)).ravel(),[0,1],np.eye(7).ravel(),rtol=2e-12,atol=1e-13,method='DOP853',dense_output=True)
 assert sol.success
 M=sol.y[:,-1].reshape(7,7);ev,V=np.linalg.eig(M);used={np.argmin(abs(ev-1))};cols=[BI@cs(0,1)];D=np.zeros((7,7));col=1
 for k in sorted(range(7),key=lambda k:abs(ev[k])):
  if k in used:continue
  lam=ev[k]
  if abs(lam.imag)<1e-5:
   assert lam.real>0;cols.append(V[:,k].real);D[col,col]=np.log(lam.real);col+=1;used.add(k)
  elif lam.imag>0:
   cols.extend([V[:,k].real,V[:,k].imag]);aa=np.log(abs(lam));bb=np.angle(lam);D[col:col+2,col:col+2]=[[aa,bb],[-bb,aa]];col+=2;used.add(k);used.add(np.argmin(abs(ev-lam.conjugate())))
 assert col==7
 W=np.column_stack(cols);mesh=np.linspace(0,1,2001);P=np.stack([sol.sol(t).reshape(7,7)@W@expm(-D*t) for t in mesh],axis=2);Pd=np.stack([js(t)@P[:,:,i]-P[:,:,i]@D for i,t in enumerate(mesh)],axis=2)
 P[:,0,:]=BI@cs(mesh,1);Pd[:,0,:]=BI@cs(mesh,2);delta=P[:,:,-1]-P[:,:,0];P-=delta[:,:,None]*mesh;Pd-=delta[:,:,None];P[:,:,-1]=P[:,:,0];Pd[:,:,-1]=Pd[:,:,0]
 np.savez(outputfile,x=mesh,gamma_values=cs(mesh).T,gamma_derivs=cs(mesh,1).T,frame_values=np.einsum('ij,jkn->ikn',B,P).transpose(2,0,1),frame_derivs=np.einsum('ij,jkn->ikn',B,Pd).transpose(2,0,1),P=P,Pd=Pd,B=B,D=D,T=T,ev=ev,M=M,q1=-.72)
 return outputfile
if __name__=='__main__':print(generate())
