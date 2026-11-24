from pathlib import Path
exec(Path('workspace/agent4_allcorrected.py').read_text().split('for g in range(1,13):')[0])
import json,pickle,os
from sage.all import bernoulli
allbasis=list(partitions(12))
Edata=json.load(open('workspace/fz25_exceptional.json'))
Ev=vector(F,[0]*77)
for a,v in zip(Edata['basis'],Edata['vector']):Ev[allbasis.index(tuple(a))]=F(int(v))

def boundary_monomial(p,x,y,g,h):
 I,t=x;J,u=y;ans=0
 for a,b,m in splits(p):
  if sum(a)+sum(I)+t!=g-1:continue
  if g==1:v=1
  else:v=point(tuple(sorted(a+I,reverse=True)),t,g)
  ans+=m*v*point(tuple(sorted(b+J,reverse=True)),u,h)
 return ans%P

def factorpair(A,g,d,e,psi):
 out=[]
 for a in A[d]['basis']:
  out.append([pair((a[0],a[1]+psi),b,g) for b in A[e]['basis']])
 return matrix(F,out)

def split_data(g):
 h=25-g;cache='workspace/agent4_boundarysplit_%02d.pkl'%g
 if os.path.exists(cache):return pickle.load(open(cache,'rb'))
 t0=time.time()
 if g==1:A={0:{'basis':[((),0)],'dual':[((),0)],'pair':matrix(F,[[1]])}}
 else:A=factor(g)
 B=factor(h)
 bases=[(x,y) for d in range(g) for x in A[d]['basis'] for y in B[11-d]['basis']]
 sizes=[len(A[d]['basis'])*len(B[11-d]['basis']) for d in range(g)]
 blocks=[]
 for d in range(g):
  rr=[]
  for e in range(g):
   if d+e==g-2:
    v=factorpair(A,g,d,e,1).tensor_product(factorpair(B,h,11-d,11-e,0))
   elif d+e==g-1:
    if g==1:Ap=matrix(F,[[1]])
    else:Ap=factorpair(A,g,d,e,0)
    v=Ap.tensor_product(factorpair(B,h,11-d,11-e,1))
   else:v=zero_matrix(F,sizes[d],sizes[e])
   rr.append(v)
  blocks.append(rr)
 S=block_matrix(F,blocks)
 print('built S',g,S.nrows(),time.time()-t0,flush=True)
 D=matrix(F,[[boundary_monomial(p,x,y,g,h) for p in allbasis] for x,y in bases])
 print('built D',g,D.nrows(),D.ncols(),time.time()-t0,flush=True)
 q=S.solve_right(D*Ev)
 answer=D.transpose()*q
 T=lambda k:F(abs(bernoulli(2*k)))/F(2**(2*k-1)*factorial(2*k))
 answer*=T(g)*T(h)
 pickle.dump((answer,S,D,bases),open(cache,'wb'))
 print('completed split',g,time.time()-t0,flush=True)
 return answer,S,D,bases
ans=vector(F,[0]*77)
for g in range(1,13):
 vv,*_=split_data(g);ans+=vv
json.dump({'p':P,'basis':allbasis,'boundary_pairing_exceptional':[int(v) for v in ans]},open('workspace/agent4_boundary_exceptional.json','w'))
print('boundary pairing functional computed',list(ans),flush=True)
