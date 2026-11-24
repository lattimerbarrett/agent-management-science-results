import json,numpy as np,itertools,time
fs=json.load(open('workspace/a3_rejected_n16_candidate.json'));C={0}
for f in fs:
 g=f
 while g:C.add(g);g=(g-1)&f
print('n',max(fs).bit_length(),'facets',len(fs),'fvector',[sum(g.bit_count()==q for g in C) for q in range(1,5)],flush=True)
def rank(A,p):
 A=A.copy()%p;m,n=A.shape;r=0
 for j in range(n):
  inds=np.nonzero(A[r:,j])[0]
  if not len(inds):continue
  i=r+inds[0];A[[i,r]]=A[[r,i]];A[r]=A[r]*pow(int(A[r,j]),-1,p)%p
  ii=np.nonzero(A[:,j])[0];ii=ii[ii!=r]
  A[ii]=(A[ii]-A[ii,j,None]*A[r])%p
  r+=1
  if r==m:break
 return r
def hom(C,p):
 cells=[sorted(g for g in C if g.bit_count()==q) for q in range(5)];rr=[]
 for q in range(1,5):
  ix={g:i for i,g in enumerate(cells[q-1])};A=np.zeros((len(cells[q-1]),len(cells[q])),dtype=np.int64)
  for j,g in enumerate(cells[q]):
   vv=[v for v in range(g.bit_length()) if g>>v&1]
   for k,v in enumerate(vv):A[ix[g^(1<<v)],j]=(-1)**k
  rr.append(rank(A,p))
 return [len(cells[q+1])-rr[q]-(rr[q+1] if q<3 else 0) for q in range(4)]
from pathlib import Path
Path('workspace/a3_candidate_odd_homology.py').write_text(Path(__file__).read_text())
start=time.time()
for p in [3,5,7]:
 print('global',p,hom(C,p),time.time()-start,flush=True)
 for v in range(max(fs).bit_length()):
  L={g^(1<<v) for g in C if g>>v&1};h=hom(L,p)
  if any(h[:2]):print('BADLINK',v,p,h,flush=True)
