import sys,numpy as np,json,collections,time,pickle,multiprocessing as mp
from pathlib import Path
sys.path.insert(0,'workspace')
from a1_cubic_closure_api import closure_kernel,cols
D=json.load(open('workspace/agent2_cubicshear_novel_orbits.json'))+json.load(open('workspace/agent3_quartic_highqrank_verified.json'))
embed=[]
for p in range(14):
 t=np.arange(8192,dtype=np.uint16);embed.append((t&((1<<p)-1))|((t>>p)<<(p+1)))
ctx=mp.get_context('fork');stop=ctx.Event()
def worker(part,DATA):
 hist=collections.Counter();seen=set();checked=0;hit=None;start=time.time();unresolved=[];dirs=collections.Counter()
 for j,s in DATA:
  f=int(s['truth_hex'],16);fb=np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little');S=np.flatnonzero(fb).astype(np.uint16)
  C=np.bincount(np.bitwise_xor(S[:,None],S[None,:]).ravel(),minlength=16384)//2;C[0]=0
  for hw in (308,312,316,324,328,332):
   allowed=[(w-hw)//2 for w in (322,326,330,334) if 0<(w-hw)//2<=7 and w>hw]
   vs=np.where(C==(s['weight']-hw)//2)[0];dirs[hw]+=len(vs)
   for v in vs:
    if stop.is_set():break
    v=int(v);p=(v&-v).bit_length()-1;hbits=fb[embed[p]]^fb[embed[p]^v];hs=np.flatnonzero(hbits).tolist();assert len(hs)==hw
    hh=int.from_bytes(np.packbits(hbits,bitorder='little').tobytes(),'little')
    if hh in seen:continue
    seen.add(hh);E,K,bas=closure_kernel(hs);checked+=1
    odd=any(k.bit_count()%2 for k in K);hist[(hw,len(E),len(K),odd)]+=1
    if odd:
     if len(K)>25:unresolved.append({'h':hex(hh),'E':E,'K':K});continue
     mask=0;T=None
     for z in range(1<<len(K)):
      if z:mask^=K[(z&-z).bit_length()-1]
      if mask.bit_count() in allowed:T=[E[i] for i in range(len(E)) if mask>>i&1];break
     if T is not None:
      moment=0
      for x in T:moment^=cols[x]
      inside=0
      while moment:
       b=moment.bit_length()-1;vv,rel=bas[b];moment^=vv;inside^=rel
      g=sum(1<<x for i,x in enumerate(hs) if inside>>i&1)|sum(1<<x for x in T)
      F=g|((g^hh)<<8192);w=F.bit_count();assert w==hw+2*len(T)
      arr=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
      for bit in range(14):a=arr.reshape(-1,2*(1<<bit));a[:,1<<bit:]^=a[:,:1<<bit]
      degree=max(int(x).bit_count() for x in np.flatnonzero(arr));assert degree<=7
      hit={'weight':w,'truth_hex':hex(F),'degree':degree,'source':j,'v':v,'hweight':hw};print('HIT',hit,flush=True);stop.set();break
   if stop.is_set():break
  if stop.is_set():break
  if j%50<2:print('progress',part,j,'checked',checked,'seconds',time.time()-start,flush=True)
 print('DONE',part,checked,'unresolved',len(unresolved),'hit',bool(hit),'dirs',dict(dirs),'hist',dict(hist),'seconds',time.time()-start,flush=True)
 json.dump(hit,open('workspace/agent2_lower_derivative_hit_%d.json'%part,'w'));pickle.dump(unresolved,open('workspace/agent2_lower_derivative_unresolved_%d.pkl'%part,'wb'));pickle.dump(dict(hist),open('workspace/agent2_lower_derivative_hist_%d.pkl'%part,'wb'))
if __name__=='__main__':
 DATA=list(enumerate(D));p=ctx.Process(target=worker,args=(1,DATA[1::2]));p.start();worker(0,DATA[::2]);p.join()
 Path('workspace/agent2_lower_derivative_search.py').write_text(Path('scratchpad.py').read_text())
