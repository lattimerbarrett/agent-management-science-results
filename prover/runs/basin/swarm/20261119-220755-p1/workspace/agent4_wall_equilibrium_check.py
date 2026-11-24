"""Finite floating-point boundary-EQ checks; no interval certificate."""
import numpy as np,sys
sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
D=np.load('workspace/agent2_rational_positive_eq_0.4.npz')
ob=BlowupODE(D['base'],D['f'],D['g'],D['N'],D['mus']);s=ob.s
for theta in [0.,1.]:
 H=ob.nodes-theta;p=ob.N*H/(ob.d*ob.fv);pp=H*ob.fv/ob.d
 M=ob.V.T@(p[:,None]*ob.V);Mp=ob.V.T@(pp[:,None]*ob.V)
 F=-4*np.linalg.solve(M,ob.Vmu.T*ob.fm)
 LL=[];bb=[];ia=np.argmin(abs(ob.nodes-theta))
 for j in range(s):
  w=np.eye(s)[j];wv=ob.V@w
  dg=np.linalg.solve(Mp,-ob.V.T@((H*wv/ob.d)*ob.gv))
  dN=ob.N**2*np.sum(H*wv/(ob.d*ob.fv**2))
  LL.append(2*((ob.Vmu@w)/ob.fm+(ob.Vmu@dg)/ob.gm)-2*dN/ob.N)
  ratio=(ob.gv*wv+ob.fv*(ob.V@dg)-dN)/ob.N
  bb.append(2*ratio[ia])
 L=np.array(LL).T;B=np.array(bb);C=L@F
 print('theta',theta,'C',C,'B F',B@F)
 assert all(np.diag(C)<0)
 ZZ=np.linalg.solve(C,np.ones(2)*2);w=-F@ZZ
 assert min(ZZ)>0
 # The Hdot interpolation in shared ODE has cancellation at the exact wall;
 # use exact face invariance Hdot=0, and check the remaining equations.
 field=ob(0,np.r_[-theta,w,ZZ],True)
 assert np.linalg.norm(field[1:])<1e-6
 J=np.block([[np.eye(s),F],[ZZ[:,None]*L,np.zeros((2,2))]])
 print('mixedEQ Z',ZZ,'theta normal eigenvalue',B@w)
 print('tangent normal spectrum',np.linalg.eigvals(J))
