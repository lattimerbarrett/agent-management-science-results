import json,time,numpy as np,shutil,collections
R=json.load(open('workspace/agent3_double8switch_first_states.json'));rng=np.random.default_rng(337318);hits={};start=time.time();records=[]
for ri,r in enumerate(R):
 f=int(r['truth_hex'],16);w=f.bit_count();S=np.array([x for x in range(16384) if f>>x&1],dtype=np.uint16);ind=np.zeros(16384,dtype=np.uint8);ind[S]=1;targets={(w+256-t)//2:t for t in [322,326,330,334]};mx=0;bestw=10000;validtot=0;near=collections.Counter()
 for batch in range(10):
  P=S[rng.integers(0,w,size=(10000,9))];V=P[:,1:]^P[:,:1];F=np.empty((10000,256),dtype=np.uint16);F[:,0]=P[:,0]
  for i in range(8):F[:,1<<i:2<<i]=F[:,:1<<i]^V[:,i,None]
  valid=~np.any(F[:,1:]==F[:,:1],axis=1);I=ind[F].sum(axis=1);I[~valid]=0;validtot+=int(valid.sum());mx=max(mx,int(I.max()));uv,ct=np.unique(I,return_counts=True)
  for u,c in zip(uv,ct):
   ww=w+256-2*int(u)
   if ww<=350:near[ww]+=int(c)
  for j in np.flatnonzero(np.isin(I,list(targets))):
   tt=targets[int(I[j])];mask=sum(1<<int(x) for x in F[j]);ff=f^mask;assert ff.bit_count()==tt;arr=np.unpackbits(np.frombuffer(ff.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for k in range(14):
    st=1<<k;bl=arr.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   anf=list(map(int,np.flatnonzero(arr)));assert max(map(int.bit_count,anf))<=7
   hits[tt]={'truth_hex':hex(ff),'weight':tt,'anf':anf,'first_state_record':ri,'second8flat':list(map(int,F[j]))};json.dump(hits,open('workspace/agent3_double8switch_hits.json','w'));print('VERIFIED HIT',tt,'record',ri,'batch',batch,'intersection',int(I[j]),flush=True)
  if len(hits)==4:break
 records.append({'source_record':ri,'draws':(batch+1)*10000,'valid':validtot,'maxI':mx,'minweight':w+256-2*mx,'nearweights':dict(near)})
 if ri%10==0:print('record',ri,'w',w,'min',w+256-2*mx,'near',dict(near),'hits',list(hits),'t',round(time.time()-start,1),flush=True);json.dump(records,open('workspace/agent3_double8switch_results.json','w'))
 if len(hits)==4:break
json.dump(records,open('workspace/agent3_double8switch_results.json','w'));print('DONE',len(records),'hits',list(hits),'t',time.time()-start,flush=True);shutil.copyfile(__file__,'workspace/agent3_double8switch_second_search.py')
