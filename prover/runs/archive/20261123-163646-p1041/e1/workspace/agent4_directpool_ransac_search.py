import json,time,numpy as np,collections,pickle
R=json.load(open('workspace/agent4_directshear_fullhull_sources.json'));rng=np.random.default_rng(444425);hits={};start=time.time();records=[];N=16384;ALL=(1<<N)-1;X=[sum(1<<j for j in range(N) if j>>i&1) for i in range(14)]
def mob(f):
 for i in range(14):f^=(f&(ALL^X[i]))<<(1<<i)
 return f
for ri,rec in enumerate(R):
 f=int(rec['truth_hex'],16);w=f.bit_count();S=np.array([x for x in range(N) if f>>x&1],dtype=np.uint16);ind=np.zeros(N,dtype=np.uint8);ind[S]=1;targets={(w+128-t)//2:t for t in [322,326,330,334]};mx=0;odd=0;validtot=0
 for batch in range(20):
  P=S[rng.integers(0,w,size=(5000,8))];V=P[:,1:]^P[:,:1];F=np.empty((5000,128),dtype=np.uint16);F[:,0]=P[:,0]
  for i in range(7):F[:,1<<i:2<<i]=F[:,:1<<i]^V[:,i,None]
  valid=~np.any(F[:,1:]==F[:,:1],axis=1);I=ind[F].sum(axis=1);I[~valid]=0;validtot+=int(valid.sum());mx=max(mx,int(I.max()));odd=max(odd,int(np.max(I*(I%2))))
  for j in np.flatnonzero(np.isin(I,list(targets))):
   tt=targets[int(I[j])];mask=sum(1<<int(x) for x in F[j]);ff=f^mask;assert ff.bit_count()==tt;a=mob(ff);assert max(j.bit_count() for j in range(N) if a>>j&1)<=7
   hits[tt]={'truth_hex':hex(ff),'anf_hex':hex(a),'weight':tt,'source_record':ri,'flat':list(map(int,F[j]))};json.dump(hits,open('workspace/agent4_directpool_ransac_hits.json','w'));print('VERIFIED HIT',tt,'record',ri,flush=True)
  if len(hits)==4:break
 records.append({'record':ri,'weight':w,'maxI':mx,'maxOddI':odd,'valid':validtot})
 if ri%10==0:print('record',ri,'weight',w,'max',mx,'odd',odd,'targets',list(targets),'time',round(time.time()-start,2),flush=True)
 if len(hits)==4:break
json.dump(records,open('workspace/agent4_directpool_ransac_results.json','w'))
print('DONE',list(hits),'seconds',time.time()-start,'maxOdds',collections.Counter((r['weight'],r['maxOddI']) for r in records),flush=True)
open('workspace/agent4_directpool_ransac_search.py','w').write(open(__file__).read())
