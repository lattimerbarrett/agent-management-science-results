import numpy as np
rng=np.random.default_rng(19)
def T(L,y,s):
 vs=[y/np.linalg.norm(y)];alph=[]
 for j in range(len(L)):
  v=L*vs[-1];alph.append(np.dot(v,vs[-1]))
  for _ in range(2):
   for vv in vs:v-=np.dot(vv,v)*vv
  if j<len(L)-1:vs.append(v/np.linalg.norm(v))
 return vs[s],np.array(alph)
for n,s in [(4,2),(5,2),(6,3)]:
 for trial in range(1000):
  L=np.sort(rng.normal(size=n));y=rng.normal(size=n);y/=np.linalg.norm(y);vals=[]
  for k in range(15):
   y,aa=T(L,y,s);vals.append(sum(aa[s+1:]))
  diff=np.diff(vals)
  if min(diff)<-1e-8 and max(diff)>1e-8:
   print('nonmonotone',n,s,trial,L,vals,flush=True);break
 else:print('all monotone',n,s)
