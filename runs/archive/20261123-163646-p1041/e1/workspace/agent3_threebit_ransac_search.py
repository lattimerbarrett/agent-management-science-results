import json,time,numpy as np,collections,shutil
R=json.load(open('workspace/a1_threebit_fiber3cycle_new_orbits.json'));rng=np.random.default_rng(330336);hits={};start=time.time();records=[]
for ri in [0,2,4]:
 f=int(R[ri]['truth_hex'],16);w=f.bit_count();S=np.array([x for x in range(16384) if f>>x&1],dtype=np.uint16);ind=np.zeros(16384,dtype=np.uint8);ind[S]=1;targets={(w+128-t)//2:t for t in [322,326,330,334]};hist=collections.Counter();mx=0;validtot=0;ts=time.time();print('START',ri,w,'targets',targets,flush=True)
 for batch in range(1000):
  P=S[rng.integers(0,w,size=(10000,8))];V=P[:,1:]^P[:,:1];F=np.empty((10000,128),dtype=np.uint16);F[:,0]=P[:,0]
  for i in range(7):F[:,1<<i:2<<i]=F[:,:1<<i]^V[:,i,None]
  valid=~np.any(F[:,1:]==F[:,:1],axis=1);I=ind[F].sum(axis=1);I[~valid]=0;validtot+=int(valid.sum());mx=max(mx,int(I.max()));uv,ct=np.unique(I,return_counts=True)
  for u,c in zip(uv,ct):hist[int(u)]+=int(c)
  good=np.flatnonzero(np.isin(I,list(targets)))
  for j in good:
   tt=targets[int(I[j])];mask=sum(1<<int(x) for x in F[j]);ff=f^mask;assert ff.bit_count()==tt;arr=np.unpackbits(np.frombuffer(ff.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for k in range(14):
    st=1<<k;bl=arr.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   anf=list(map(int,np.flatnonzero(arr)));assert max(map(int.bit_count,anf))<=7
   hits[tt]={'truth_hex':hex(ff),'weight':tt,'anf':anf,'source_record':ri,'flat':list(map(int,F[j]))};json.dump(hits,open('workspace/agent3_threebit_ransac_hits.json','w'));print('VERIFIED HIT',tt,'record',ri,'batch',batch,'intersection',int(I[j]),flush=True)
  if batch%100==0:print('record',ri,'draws',(batch+1)*10000,'max',mx,'hist>=60',{k:v for k,v in hist.items() if k>=60},'time',round(time.time()-ts,2),flush=True)
  if len(hits)==4:break
 records.append({'source_record':ri,'draws':(batch+1)*10000,'valid':validtot,'max':mx,'histogram':dict(hist),'seconds':time.time()-ts});json.dump(records,open('workspace/agent3_threebit_ransac_results.json','w'))
 if len(hits)==4:break
print('DONE',list(hits),'seconds',time.time()-start,flush=True);shutil.copyfile(__file__,'workspace/agent3_threebit_ransac_search.py')
