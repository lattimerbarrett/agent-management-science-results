import numpy as np
from scipy.optimize import linprog
rng=np.random.default_rng(438)
def op(nodes,p,s=3):
 V=np.array([nodes**j for j in range(s)]).T;M=V.T@(p[:,None]*V)
 fc=np.linalg.solve(M,-V.T@(p*nodes**s));fv=nodes**s+V@fc;N=np.dot(p,fv**2)
 return np.r_[fc,1.],N,p*fv**2/N
found=0;count=0
for it in range(3000):
 nodes=np.sort(rng.normal(size=4)*3);p=rng.dirichlet(np.ones(4)*2)
 f,N,pp=op(nodes,p);g,NN,_=op(nodes,pp)
 prod=np.polynomial.polynomial.polymul(f,g);prod[0]+=N;rr=np.roots(prod[::-1]);mus=np.sort(rr.real[abs(rr.imag)<1e-7]);q=len(mus)
 if q<2:continue
 V=np.array([nodes**j for j in range(3)]).T;Vm=np.array([mus**j for j in range(3)]).T
 fv=np.polynomial.polynomial.polyval(nodes,f);gv=np.polynomial.polynomial.polyval(nodes,g);fm=np.polynomial.polynomial.polyval(mus,f);gm=np.polynomial.polynomial.polyval(mus,g)
 M=V.T@(p[:,None]*V);Mp=V.T@(pp[:,None]*V)
 DG=-np.linalg.solve(Mp,M);D=(p*gv)@V
 L=2*(Vm/fm[:,None]+(Vm@DG)/gm[:,None])-2*D/N
 F=-4*np.linalg.solve(M,Vm.T*fm)
 C=L@F
 scale=np.sqrt(abs(np.diag(C)));C/=scale[:,None]*scale[None,:]
 lp=linprog(np.zeros(q),A_ub=-C,b_ub=np.zeros(q),A_eq=np.ones((1,q)),b_eq=[1],bounds=[(0,None)]*q,method='highs')
 count+=1
 if lp.success:
  print('POSSIBLE',it,'nodes',nodes,'p',p,'mus',mus,'CZ',C@lp.x,'z',lp.x,'C',C);found+=1
  np.savez('workspace/agent4_s3_wall_C_candidate.npz',nodes=nodes,p=p,f=f,g=g,N=N,mus=mus,C=C,z=lp.x)
  if found>=3:break
print('tested',count,'found',found)
