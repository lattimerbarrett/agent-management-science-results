from pathlib import Path
s=Path('workspace/agent2_lambda25lambda23_boundary.py').read_text().split('parts12=')[0]
exec(s)
from sage.all import GF,matrix
import time,json
start=time.time();F=GF(P)
@lru_cache(None)
def one_mons(d):return [(ks,d-sum(ks)) for k in range(d+1) for ks in partitions(k)]
found=[];checked=0
for h in range(2,25):
 for d in range((h+1)//2,min(12,h-1)+1):
  b=h-1-d
  if b<0:continue
  B=one_mons(b);T=one_mons(d-1);D=list(partitions(d))
  Q=matrix(F,[[l1(h,tuple(sorted(ks+ls)),e+f+1) for ls,f in T] for ks,e in B])
  L=matrix(F,[[l1(h,tuple(sorted(ks+ls)),e) for ls in D] for ks,e in B])
  K=Q.left_kernel().basis_matrix();R=K*L;rr=R.rank();checked+=1
  print('h,d,b',h,d,b,'mat',len(B),len(T),'K',K.nrows(),'newLrank',rr,flush=True)
  if rr:found.append((h,d,b,rr))
print('FRAMED NECESSARYFILTER checked',checked,'found',found,'sec',time.time()-start,flush=True)
json.dump({'checked':checked,'found':found},open('workspace/agent2_framed_filter25.json','w'))
if Path(__file__).name=='scratchpad.py':Path('workspace/agent2_framed_filter25.py').write_text(Path(__file__).read_text())
