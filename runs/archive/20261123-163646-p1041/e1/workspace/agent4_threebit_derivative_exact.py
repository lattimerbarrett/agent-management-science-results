import numpy as np,itertools,time,json,pickle,collections,sys
sys.path.insert(0,'workspace');from a1_cubic_closure_api import closure_kernel,cols
start=time.time();D=json.load(open('workspace/a1_threebit_fiber3cycle_new_orbits.json'));N=16384;xx=np.arange(8192,dtype=np.int64)
EMB=[(xx&((1<<p)-1))|((xx>>p)<<(p+1)) for p in range(14)]
X=[sum(1<<j for j in range(N) if j>>i&1) for i in range(14)];ALL=(1<<N)-1
def mob(f):
 for i in range(14):f^=(f&(ALL^X[i]))<<(1<<i)
 return f
found={};seen=set();stats=collections.Counter();tested=0
for ri,rec in enumerate(D):
 F=int(rec['truth_hex'],16);W=F.bit_count();ANF=mob(F);assert max(j.bit_count() for j in range(N) if ANF>>j&1)<=7
 SS0=np.array([j for j in range(N) if F>>j&1],dtype=np.int64);DIF=np.bincount((SS0[:,None]^SS0[None,:]).ravel(),minlength=N);VS=np.flatnonzero(np.isin(W-DIF,[308,312,316,320,324,328,332]));VS=VS[VS!=0]
 FB=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little')
 print('SOURCE',ri,'weight',W,'directions',len(VS),flush=True)
 for v in VS:
  v=int(v);p=(v&-v).bit_length()-1;R=EMB[p];hb=FB[R]^FB[R^v];h=int.from_bytes(np.packbits(hb,bitorder='little').tobytes(),'little')
  if h in seen:continue
  seen.add(h);SS=np.flatnonzero(hb).tolist();HW=len(SS);E,K,B5=closure_kernel(SS);tested+=1;stats[(HW,len(E),len(K),sum(k.bit_count()%2 for k in K))]+=1
  if not any(k.bit_count()%2 for k in K):continue
  assert len(K)<=24
  tmask=0;prev=0
  for n in range(1<<len(K)):
   gr=n^(n>>1)
   if n:tmask^=K[(gr^prev).bit_length()-1]
   prev=gr;TW=tmask.bit_count();target=HW+2*TW
   if TW>7 or target not in [322,326,330,334] or target in found:continue
   syndrome=0
   for j,x in enumerate(E):
    if tmask>>j&1:syndrome^=cols[x]
   im=0
   while syndrome:
    pp=syndrome.bit_length()-1;aa,bb=B5[pp];syndrome^=aa;im^=bb
   gg=sum(1<<x for j,x in enumerate(SS) if im>>j&1)^sum(1<<x for j,x in enumerate(E) if tmask>>j&1)
   FF=gg|((gg^h)<<8192);assert FF.bit_count()==target
   aa=mob(FF);assert max(j.bit_count() for j in range(N) if aa>>j&1)<=7
   found[target]={'source':ri,'direction':v,'truth_hex':hex(FF),'anf_hex':hex(aa)};json.dump(found,open('workspace/agent4_threebit_derivative_hits.json','w'));print('HIT',target,'source',ri,'v',v,'sec',time.time()-start,flush=True)
 print('DONEsource',ri,'tested',tested,'found',found.keys(),'sec',time.time()-start,flush=True)
print('ALLDONE',tested,found.keys(),'STATS',stats,'SEC',time.time()-start)
pickle.dump(dict(stats),open('workspace/agent4_threebit_derivative_stats.pkl','wb'))
open('workspace/agent4_threebit_derivative_exact.py','w').write(open(__file__).read())
