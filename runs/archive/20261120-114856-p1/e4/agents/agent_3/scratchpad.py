import numpy as np
from numpy.polynomial import Polynomial as P
x=P([0,1]);q=(x*x-1)*(x-2)*(x+3);r=(x*x-1)*(x+2)*(x-3);H=1;Q=q*r;poly=Q-H;l=np.sort(poly.roots());betas=np.sort([z.real for z in (Q+H).roots() if abs(z.imag)<1e-8]);ix=[0,1,3,5,7];lv=l[ix];f=np.vander(lv,4,increasing=True);A=np.vstack([np.ones(5),(q(lv)[:,None]*f).T]);w=np.linalg.solve(A,np.r_[1.,np.zeros(4)]);wp=w*q(lv)**2/H;G=f.T@(w[:,None]*f);Gp=f.T@(wp[:,None]*f);Pv=P.fromroots(lv)
for beta in betas:
 fb=np.array([beta**j for j in range(4)]);qb=q(beta);rb=r(beta)
 for gamma in betas:
  if beta==gamma:continue
  fg=np.array([gamma**j for j in range(4)]);qg=q(gamma);rg=r(gamma)
  cc=4*qg*np.linalg.solve(G,fg);ee=-np.linalg.solve(Gp,G@cc);dh=w@(r(lv)*(f@cc));aval=(rb*(fb@cc)+qb*(fb@ee)+dh)/H
  formula=-4*Pv(beta)/(H*qb)*(qb*qb-qg*qg)/(gamma-beta)
  print(beta,gamma,aval,formula,abs(aval-formula));assert abs(aval-formula)<1e-4*max(1,abs(aval))
