import json,numpy as np,time,collections,shutil
states=json.load(open('workspace/agent3_qrank_guided_novel_orbits.json'));rng=np.random.default_rng(934272);start=time.time();hits={};improved=[]
for si,r in enumerate(states):
 f=int(r['truth_hex'],16);w=r['weight'];S=[x for x in range(16384) if f>>x&1];SS=set(S);maxI=0;hc=collections.Counter();seen=set()
 for batch in range(100):
  samples=rng.choice(S,size=(10000,9),replace=True)
  for sam in samples:
   vs=list(map(int,sam));p=vs[0];ps=[p]
   for b in vs[1:]:
    b^=p;ps +=[x^b for x in ps]
   if len(set(ps))<256:continue
   I=sum(x in SS for x in ps);maxI=max(maxI,I);ww=w+256-2*I
   if I<128:continue
   g=f^sum(1<<x for x in ps);assert g.bit_count()==ww
   if g in seen:continue
   seen.add(g);hc[ww]+=1
   if ww<w:improved.append({'truth_hex':hex(g),'weight':ww,'source':si})
   if ww in (322,326,330,334):
    aa=np.unpackbits(np.frombuffer(g.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
    for bit in range(14):
     st=1<<bit;bl=aa.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
    anf=list(map(int,np.flatnonzero(aa)));assert max(map(int.bit_count,anf))<=7
    hits[ww]={'truth_hex':hex(g),'weight':ww,'anf':anf};print('VERIFIED HIT',ww,flush=True);json.dump(hits,open('workspace/agent3_degree6_switch_hits.json','w'))
  if batch%20==0:print('state',si,'weight',w,'batch',batch,'maxI',maxI,'high',dict(hc),'t',round(time.time()-start,1),flush=True)
 print('stateDONE',si,'maxI',maxI,'high',dict(hc),flush=True)
json.dump(improved,open('workspace/agent3_degree6_switch_improved.json','w'));print('DONE',len(improved),'hits',list(hits),'t',time.time()-start,flush=True);shutil.copyfile(__file__,'workspace/agent3_degree6_switch_search.py')
