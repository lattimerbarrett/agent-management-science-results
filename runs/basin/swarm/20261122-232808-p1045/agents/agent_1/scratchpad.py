import numpy as np, networkx as nx, itertools as it,pickle,time
from scipy.linalg import eigh
mats,Bflag,Bpage=pickle.load(open('bookflags6.pkl','rb'))
a=.09;p=np.sqrt(3*a);b=(1+2*(1-p)**2)/3
gs=[g for g in nx.graph_atlas_g() if len(g)==6];assign=np.array(list(it.product(range(3),repeat=6)))
probs=[]
for g in gs:
 A=nx.to_numpy_array(g,dtype=int);val=np.ones(len(assign))
 for i,j in it.combinations(range(6),2):
  cross=assign[:,i]!=assign[:,j];val*=np.where(cross,p,0) if A[i,j] else np.where(cross,1-p,1)
 aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g,g).isomorphisms_iter());probs.append(val.mean()*720/aut)
probs=np.array(probs);print('zero graphs',np.sum(probs<1e-14),flush=True)
blocks=[];cols=[];starts=[0];scales=[]
# initially all blocks
for ib,M in enumerate(mats):
 e,U=eigh(np.einsum('g,gij->ij',probs,M));N=U[:,e<1e-9]
 MM=np.einsum('ia,gij,jb->gab',N,M,N);k=N.shape[1]
 inds=np.triu_indices(k);fac=np.where(inds[0]==inds[1],1,np.sqrt(2))
 C=MM[:,inds[0],inds[1]]*fac
 scale=np.linalg.norm(C);C/=scale
 cols.append(C);starts.append(starts[-1]+C.shape[1]);blocks.append((k,inds,fac));scales.append(scale)
 print(ib,k,flush=True)
# More book multipliers, using rooted flags of order five.
import os
if os.path.exists('bookflags5.pkl'):
 BF,BP=pickle.load(open('bookflags5.pkl','rb'))
else:
 edges=list(it.combinations(range(5),2)); canon=[]
 for mask in range(1024):
  A=np.zeros((5,5),dtype=int)
  for k,(i,j) in enumerate(edges):A[i,j]=A[j,i]=(mask>>k)&1
  canon.append(min(sum(int(A[perm[i],perm[j]])<<k for k,(i,j) in enumerate(edges)) for extra in it.permutations([2,3,4]) for perm in [(0,1)+extra]))
 fl=[[v for v in sorted(set(canon)) if v&1==c] for c in [0,1]]
 fm=np.array([fl[m&1].index(canon[m]) for m in range(1024)])
 nf=len(fl[0]);print('nf',nf,flush=True)
 BF=np.zeros((2,len(gs),nf));BP=np.zeros_like(BF);perms=np.array(list(it.permutations(range(6))))
 for ig,g in enumerate(gs):
  A=nx.to_numpy_array(g,dtype=int);P=A[perms[:,:,None],perms[:,None,:]]
  mask=sum(P[:,i,j]*(1<<k) for k,(i,j) in enumerate(edges));cc=mask&1;ii=fm[mask]
  for ccc in [0,1]:
   take=cc==ccc;np.add.at(BF[ccc,ig],ii[take],1/720)
   pg=((P[:,0,5]==ccc)&(P[:,1,5]==ccc)).astype(float)
   np.add.at(BP[ccc,ig],ii[take],pg[take]/720)
 pickle.dump((BF,BP),open('bookflags5.pkl','wb'))
C=a*BF[1]-BP[1];scale=np.maximum(np.linalg.norm(C,axis=0),1e-12);cols.append(C/scale);nred=C.shape[1];rstart=starts[-1];starts.append(starts[-1]+nred)
BC=b*BF[0]-BP[0];keep=np.abs(probs@BC)<1e-12;BC=BC[:,keep];scale=np.maximum(np.linalg.norm(BC,axis=0),1e-12);BC/=scale
print('blue flags',BC.shape[1],flush=True);blstart=starts[-1];cols.append(BC)
# graph slack columns
ix=np.where(probs<1e-14)[0];CC=np.eye(len(probs))[:,ix];cols.append(CC)
C=np.concatenate(cols,axis=1)
# Normalize the sum of the blue multipliers.
normal=np.zeros(C.shape[1]);normal[blstart:blstart+BC.shape[1]]=1
C=np.concatenate([C,normal[None,:]],axis=0);c=np.zeros(C.shape[0]);c[-1]=-1
print('eq size',C.shape,flush=True)
# Cone projection. Equality projection via thin SVD.
U,S,Vt=np.linalg.svd(C,full_matrices=False);keep=S>1e-9;U=U[:,keep];S=S[keep];Vt=Vt[keep]
res=c-U@(U.T@c);print('rank',len(S),'rangeerr',np.linalg.norm(res),flush=True)
q=-Vt.T@((U.T@c)/S)
def affine(x):return x-Vt.T@(Vt@x)+q
def cone(x):
 y=x.copy()
 for ib,(k,inds,fac) in enumerate(blocks):
  vals=x[starts[ib]:starts[ib+1]]/fac
  M=np.zeros((k,k));M[inds]=vals;M[(inds[1],inds[0])]=vals
  e,U=eigh(M);M=(U*np.maximum(e,0))@U.T
  y[starts[ib]:starts[ib+1]]=M[inds]*fac
 y[rstart:]=np.maximum(y[rstart:],0)
 return y
x=np.zeros(C.shape[1]);t0=time.time()
for iteration in range(100001):
 y=cone(x);z=affine(2*y-x);x+=z-y
 if iteration%1000==0:
  err=np.linalg.norm(C@y+c);print(iteration,err,np.linalg.norm(y),time.time()-t0,flush=True)
  if err<1e-9:break
pickle.dump((a,b,blocks,starts,C,c,y,scales),open('bookdual.pkl','wb'))
