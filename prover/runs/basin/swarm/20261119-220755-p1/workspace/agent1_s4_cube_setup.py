import numpy as np,itertools,sys
sys.path.insert(0,'workspace');from agent2_blowup_ode import BlowupODE
S=np.array([-4.,-3.,-2.,-1.,1.,2.,3.,4.]);P=np.poly1d(np.poly(S));L=100.;tpol=np.array([1,-30,273,-820,576+L]);tr=np.sort(np.roots(tpol));print('t',tr)
f=np.array([tr[0]*tr[2],0,-tr[0]-tr[2],0,1.]);g=np.array([tr[1]*tr[3],0,-tr[1]-tr[3],0,1.]);print('f,g',f,g)
pr=np.polynomial.polynomial.polymul(f,g);pr[0]+=L;neg=np.sort(np.roots(pr[::-1]));print('neg',neg)
mu=max(a.real for a in neg if abs(a.imag)<1e-7);ob=BlowupODE(S,f,g,L,[-mu,mu])
