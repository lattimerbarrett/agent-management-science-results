import json,numpy as np,random,pickle,collections,time,sys
from pathlib import Path
sys.path.insert(0,'workspace');from agent2_fullsupport_switch_api import full_kernel_direction,lift_direction,direction_reps,quadratic_excess
random.seed(413)
def fp(f):
 a=1-2*np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').astype(np.int32)
 for i in range(14):
  z=a.reshape(-1,2*(1<<i));t=z[:,:1<<i].copy();z[:,:1<<i]=t+z[:,1<<i:];z[:,1<<i:]=t-z[:,1<<i:]
 v,c=np.unique(np.abs(a),return_counts=True);return tuple(zip(map(int,v),map(int,c)))
targets=json.load(open('workspace/a1_threebit_fiber3cycle_new_orbits.json'));ts={j:fp(int(targets[j]['truth_hex'],16)) for j in [0,2]};seeds=json.load(open('workspace/agent4_flat_seeds.json'));found=[];orbits=[];stats=collections.Counter();start=time.time()
for w in [336,340]:
 masks=seeds[str(w)];F=0
 for mask in masks:
  for x in range(16384):
   if x&~mask==0:F^=1<<x
 groups={fp(F)};dirs=direction_reps(masks);print('BASE',w,'directions',len(dirs),flush=True)
 for vi,v in enumerate(dirs):
  SS,K=full_kernel_direction(F,v);stats[(w,len(K),quadratic_excess(SS,K))]+=1;G=[lift_direction(SS,k,v) for k in K]
  ns=(1<<len(K)) if len(K)<=10 else 512
  for jj in range(ns):
   g=0;rel=0
   if len(K)<=10:bits=jj
   else:bits=random.getrandbits(len(K))
   for k,b in enumerate(G):
    if bits>>k&1:g^=b;rel^=K[k]
   cand=F^g;sig=fp(cand)
   if sig not in groups:groups.add(sig);orbits.append({'weight':w,'truth_hex':hex(cand),'v':v,'switchweight':g.bit_count(),'relation':hex(rel)});print('NEWCLASS',w,'classes',len(groups),'K',len(K),'v',v,'switchw',g.bit_count(),flush=True)
   for target,s in ts.items():
    if targets[target]['weight']==w and sig==s:
     rec={'target':target,'weight':w,'truth_hex':hex(cand),'v':v,'switchweight':g.bit_count(),'relation':hex(rel)};found.append(rec);print('SIGNATUREMATCH',target,'v',v,'switchweight',g.bit_count(),flush=True);ts.pop(target);break
  if vi%10==0:print('progress',w,vi,'classes',len(groups),'seconds',time.time()-start,flush=True)
  if time.time()-start>110:break
 if time.time()-start>110:break
print('DONE','stats',dict(stats),'matches',len(found),'neworbits',len(orbits),'seconds',time.time()-start,flush=True)
json.dump(found,open('workspace/agent2_threebit_vs_fullswitch_matches.json','w'));json.dump(orbits,open('workspace/agent2_general_fullswitch_orbits.json','w'))
Path('workspace/agent2_general_fullswitch_survey.py').write_text(Path('scratchpad.py').read_text())
