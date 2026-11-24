import numpy as np
from agent2_blowup_ode import BlowupODE
z=np.load('workspace/agent1_GENUINE_s4_periodic.npz');ob=BlowupODE(z['base'],z['f'],z['g'],float(z['L']),z['mus']);S=ob.nodes;V=ob.V;Vm=ob.Vmu;L=ob.N
def field(Y):
 if Y.ndim==1:return field(Y[:,None])[:,0]
 th=-Y[0];W=Y[1:5].T;Z=Y[-2:].T;H=S[None,:]-th[:,None];wv=W@V.T;p=L*H/(ob.d*ob.fv);pa=H*ob.fv/ob.d;M=np.einsum('ni,nj,bn->bij',V,V,p);Mp=np.einsum('ni,nj,bn->bij',V,V,pa);dg=np.linalg.solve(Mp,(-((H*wv/ob.d)*ob.gv)@V)[...,None])[...,0];dn=L**2*np.sum(H*wv/(ob.d*ob.fv**2),axis=1);ratio=(ob.gv*wv+ob.fv*(dg@V.T)-dn[:,None])/L
 wf=-np.linalg.solve(M,((p*ob.fv*ratio**2)@V+4*(Z*ob.fm)@Vm)[...,None])[...,0];ix=np.where(th.real<.5,2,3);rat=ratio[np.arange(len(th)),ix];hd=2*(S[ix]-th)*rat;grow=2+2*((W@Vm.T)/ob.fm+(dg@Vm.T)/ob.gm)-2*dn[:,None]/L;return np.vstack([hd,(W+wf).T,(Z*grow).T])
def jac(y):
 h=1e-20;YY=y[:,None]+1j*h*np.eye(7);return field(YY).imag/h
