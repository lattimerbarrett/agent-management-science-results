import numpy as np
from numpy.polynomial import polynomial as P
rng=np.random.default_rng(803);errs=[]
for it in range(100):
 x=np.sort(rng.normal(size=4)*2); p=rng.dirichlet(np.ones(4)*2);V=np.array([x**j for j in range(3)]).T;M=V.T@(p[:,None]*V)
 f=np.r_[np.linalg.solve(M,-V.T@(p*x**3)),1.];fv=P.polyval(x,f);N=p@fv**2;pp=p*fv**2/N;Mp=V.T@(pp[:,None]*V);g=np.r_[np.linalg.solve(Mp,-V.T@(pp*x**3)),1.]
 b=P.polymul(f,g);b[0]+=N;rr=P.polyroots(b);mu=np.sort(rr.real[abs(rr.imag)<1e-7]); n=len(mu)
 if not n:continue
 vm=np.array([mu**j for j in range(3)]).T;fm=P.polyval(mu,f);gm=P.polyval(mu,g)
 L=2*(vm/fm[:,None]-(vm@np.linalg.solve(Mp,M))/gm[:,None])-2*((p*P.polyval(x,g))@V)/N
 F=-4*np.linalg.solve(M,vm.T*fm);C=L@F
 poly=P.polymul(f,g);poly[0]-=N;Q,rem=P.polydiv(poly,P.polyfromroots(x));q=P.polyval(mu,Q)
 D=np.zeros_like(C)
 for i in range(n):
  for j in range(n):
   if i!=j:D[i,j]=16*(fm[j]**2-fm[i]**2)/(fm[i]*q[i]*(mu[i]-mu[j]))
   else:D[i,i]=-16/q[i]*(P.polyval(mu[i],P.polyder(f))-fm[i]*P.polyval(mu[i],P.polyder(g))/gm[i])
 err=np.max(abs(C-D)/(1+abs(C)));errs.append(err)
 import itertools
 cc=C/np.sqrt(abs(np.diag(C)))[:,None]/np.sqrt(abs(np.diag(C)))[None,:]
 dweight=np.abs(fm*q);wc=dweight[:,None]*C
 ev=np.linalg.eigvalsh(-(wc+wc.T)/2)
 if np.max((C+C.T)-np.diag(np.diag(C+C.T)))>1e-6: print('POSITIVEOFFSYMM',it,np.max(C+C.T))
 sym=-(cc+cc.T)/2
 for k in range(1,n+1):
  for ids in itertools.combinations(range(n),k):
   ss=sym[np.ix_(ids,ids)]
   try:z=np.linalg.solve(ss,np.ones(k)); z/=sum(z)
   except:continue
   if min(z)<0:continue
   val=z@ss@z
   if val < -1e-5: print('NOTCOPOSITIVE',k,val,'n',n,'it',it,'C',cc)
 
print('100random max normalized error',max(errs))
