import numpy as np
from scipy.optimize._numdiff import approx_derivative
from pathlib import Path
rng=np.random.default_rng(30)
for n,s in [(4,2),(6,3),(8,4)]:
 lam=np.linspace(-1,1,n);V=lam[:,None]**np.arange(s);p=rng.uniform(.3,1,n);M=V.T@(p[:,None]*V);c=np.linalg.solve(M,-V.T@(p*lam**s));f=lam**s+V@c;N=p@(f*f)
 def fun(q):
  cc=np.linalg.solve(V.T@(q[:,None]*V),-V.T@(q*lam**s));ff=lam**s+V@cc;return q@(ff*ff)
 def grad(q):
  cc=np.linalg.solve(V.T@(q[:,None]*V),-V.T@(q*lam**s));ff=lam**s+V@cc;return ff*ff
 HH=-2*np.diag(f)@V@np.linalg.solve(M,V.T)@np.diag(f)
 assert np.linalg.norm(approx_derivative(lambda q:np.array([fun(q)]),p).reshape(-1)-f*f)<1e-6
 assert np.linalg.norm(approx_derivative(grad,p)-HH)<1e-5
 curv=HH+2*np.diag(f*f/p);assert np.linalg.eigvalsh(curv).min()>-1e-8
 y=np.sqrt(p);K=y[:,None]*V;P=K@np.linalg.solve(K.T@K,K.T)
 def residual(z):
  q=z*z;cc=np.linalg.solve(V.T@(q[:,None]*V),-V.T@(q*lam**s));return z*(lam**s+V@cc)
 J=(np.eye(n)-2*P)@np.diag(f)
 assert np.linalg.norm(approx_derivative(residual,y)-J)<1e-5
 print(n,s,'gradient Hessian relative-curvature reflection VERIFIED')
