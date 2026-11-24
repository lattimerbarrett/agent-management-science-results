from pathlib import Path
base=Path('workspace/billiard_words_agent2.py').read_text().split('start=time.time()')[0]
exec(base)
def cut(I,row,positive=True):
 lo,hi=I;A=-row[0];B=row[1]
 if not positive:A=-A;B=-B
 if abs(B)<1e-30:return (lo,hi) if A>0 else(1.,0.)
 x=-A/B
 if B>0:lo=max(lo,x)
 else:hi=min(hi,x)
 return lo,hi
def branches(D):
 v,d,H,core,extra,J,F,Fi,RL,RR=D;WL=adwords(RL,core[2],extra,1,3);WR=adwords(RR,core[1],extra,-1,3);ans=[]
 for wl,ML in WL:
  for wr,MR in WR:
   M=F.copy();I=(-1e6,-1e-10);I=cut(I,M[0],False)
   for stage,(word,R,e) in enumerate([(wr,RR,core[1]),(wl,RL,core[2])]):
    for j in word:
     ell=np.array([-1,1/(extra[j]-e)])@M;I=cut(I,ell);M=R[j]@M;I=cut(I,M[0],False)
    I=cut(I,M[1],e==core[1])
    if stage==0:
     M=Fi@M;I=cut(I,M[0],False)
   if I[0]<I[1]:
    eps=max(1e-16,(I[1]-I[0])*1e-9);I=(I[0]+eps,I[1]-eps)
    if I[0]<I[1]:ans.append((M,I))
 return ans
def mob(M,x):return (-M[1,0]+M[1,1]*x)/(M[0,0]-M[0,1]*x)
def merge(vals):
 vals=sorted(vals);out=[]
 for l,r in vals:
  if not l<r:continue
  if out and l<=out[-1][1]:out[-1]=(out[-1][0],max(out[-1][1],r))
  else:out.append((l,r))
 return out
def survive(B,maxdepth=1000):
 K=merge([I for M,I in B])
 for dep in range(maxdepth):
  KK=[]
  for M,I in B:
   inv=np.linalg.inv(M);a,b=sorted([mob(M,I[0]),mob(M,I[1])])
   for l,r in K:
    l=max(l,a);r=min(r,b)
    if l<r:
     ll,rr=sorted([mob(inv,l),mob(inv,r)]);ll=max(ll,I[0]);rr=min(rr,I[1]);
     if ll<rr:KK.append((ll,rr))
  K=merge(KK)
  if not K:return dep,K
  if len(K)>2000:return dep,K
 return maxdepth,K
rng=np.random.default_rng(191919);best=0;start=time.time()
for tr in range(5000):
 a=rng.uniform(.05,.95);L=1+np.exp(rng.uniform(np.log(.05),np.log(10)));theta=np.exp(rng.uniform(np.log(.001),np.log(.99)));D=data(a,L,theta)
 if D is None:continue
 B=branches(D);dep,K=survive(B,1000)
 if dep>best:
  best=dep;print('NEW',tr,'depth',dep,'aLHtheta',a,L,D[2],theta,'branches',len(B),'K',K[:3],flush=True)
  np.savez('workspace/survivor_best_agent2.npz',a=a,L=L,H=D[2],depth=dep,K=np.array(K),M=np.array([x[0]for x in B]),I=np.array([x[1]for x in B]))
 if dep>=1000 and K and max(r-l for l,r in K)>1e-9:break
print('done',tr,'best',best,'time',time.time()-start)
Path('workspace/survivor_agent2.py').write_text(Path(__file__).read_text())
