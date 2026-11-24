import numpy as np
for file,s in [('s2ghosts.npz',2),('search2.npz',3),('nearmax.npz',3),('ghostsearch.npz',3)]:
 D=np.load(file,allow_pickle=True)
 if 'x' in D:x=D['x']
 elif file=='nearmax.npz':x=np.tile(np.array([-3.,-2.,-1.,1.,2.,3.])/3,(len(D['200000']),1))
 else:continue
 if '200000' in D:w=D['200000']
 elif '100000' in D:w=D['100000']
 else:w=D['w']
 if x.ndim==1:x=np.tile(x,(len(w),1))
 V=np.stack([x**j for j in range(s)],axis=2)
 def f(w):
  G=np.einsum('bi,bij,bik->bjk',w,V,V);m=np.einsum('bi,bi,bij->bj',w,x**s,V);a=np.linalg.solve(G,m[...,None])[...,0]
  p=x**s-np.einsum('bij,bj->bi',V,a);h=np.sum(w*p*p,axis=1);return w*p*p/h[:,None],p,h
 wp,p,h=f(w);wpp,q,hh=f(wp)
 mult=p*q/np.sqrt(h*hh)[:,None]
 excluded=w<1e-15
 bad=np.max(np.where(excluded,abs(mult),0),axis=1)
 print(file,'unstable',np.sum(bad>1+1e-8),'max',bad.max())
 for j in np.argsort(bad)[-5:]:print(j,bad[j],'w',w[j],'mult',mult[j])
