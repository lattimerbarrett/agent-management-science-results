import sys,numpy as np,json,collections,time,pickle
from pathlib import Path
sys.path.insert(0,'workspace')
from a1_cubic_closure_api import closure_kernel,cols
D=json.load(open('workspace/agent2_cubicshear_novel_orbits.json'));embed=[]
for p in range(14):
 t=np.arange(8192,dtype=np.uint16);embed.append((t&((1<<p)-1))|((t>>p)<<(p+1)))
hist=collections.Counter();seen=set();checked=0;hit=None;start=time.time();unresolved=[]
for j,s in enumerate(D):
 f=int(s['truth_hex'],16);fb=np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little');S=np.flatnonzero(fb).astype(np.uint16)
 C=np.bincount(np.bitwise_xor(S[:,None],S[None,:]).ravel(),minlength=16384)//2;C[0]=0;vs=np.where(C==(s['weight']-320)//2)[0]
 for v in vs:
  v=int(v);p=(v&-v).bit_length()-1;hbits=fb[embed[p]]^fb[embed[p]^v];hs=np.flatnonzero(hbits).tolist();assert len(hs)==320
  hh=int.from_bytes(np.packbits(hbits,bitorder='little').tobytes(),'little')
  if hh in seen:continue
  seen.add(hh);E,K,bas=closure_kernel(hs);checked+=1
  odd=any(k.bit_count()%2 for k in K);hist[(len(E),len(K),odd)]+=1
  if odd:
   if len(K)>25:unresolved.append({'h':hex(hh),'E':E,'K':K});continue
   mask=0;T=None
   for z in range(1<<len(K)):
    if z:mask^=K[(z&-z).bit_length()-1]
    if mask.bit_count() in (1,3,5,7):T=[E[i] for i in range(len(E)) if mask>>i&1];break
   if T is not None:
    moment=0
    for x in T:moment^=cols[x]
    inside=0
    while moment:
     b=moment.bit_length()-1;vv,rel=bas[b];moment^=vv;inside^=rel
    g=sum(1<<x for i,x in enumerate(hs) if inside>>i&1)|sum(1<<x for x in T)
    F=g|((g^hh)<<8192);w=F.bit_count();assert w==320+2*len(T)
    arr=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
    for bit in range(14):a=arr.reshape(-1,2*(1<<bit));a[:,1<<bit:]^=a[:,:1<<bit]
    degree=max(int(x).bit_count() for x in np.flatnonzero(arr));assert degree<=7
    hit={'weight':w,'truth_hex':hex(F),'degree':degree,'source':j,'v':v};print('HIT',hit,flush=True);break
 if hit:break
 print('progress',j,'dirs',len(vs),'checked',checked,'hist',dict(hist),'seconds',time.time()-start,flush=True)
print('DONE',checked,'unresolved',len(unresolved),'hit',bool(hit),'hist',dict(hist),'seconds',time.time()-start,flush=True)
json.dump(hit,open('workspace/agent2_cubic_derivative_hit.json','w'));pickle.dump(unresolved,open('workspace/agent2_cubic_derivative_unresolved.pkl','wb'))
Path('workspace/agent2_cubic_derivative_search.py').write_text(Path('scratchpad.py').read_text())
