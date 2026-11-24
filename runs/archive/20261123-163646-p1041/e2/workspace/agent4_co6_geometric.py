import itertools,time,numpy as np,z3,json
from pathlib import Path

def xorall(xs):
 if not xs:return z3.BoolVal(False)
 while len(xs)>1:xs=[z3.Xor(xs[i],xs[i+1]) if i+1<len(xs) else xs[i] for i in range(0,len(xs),2)]
 return xs[0]
gl=[]
for typ in range(3):
 p=[]
 for v in range(1,8):
  if typ==0:w=((v&1)<<1)|((v&2)>>1)|(v&4)
  elif typ==1:w=((v<<1)&7)|(v>>2)
  else:w=v^((v&2)>>1)
  p.append(w-1)
 gl.append(p)

def test(mode):
 cps=[]
 for p in gl:
  if mode=='product':
   cps.extend([p+list(range(7,14)),list(range(7))+[x+7 for x in p]])
  else:cps.append(p+[x+7 for x in p])
 if mode=='diag_swap':cps.append(list(range(7,14))+list(range(7)))
 xs=np.arange(16384,dtype=np.uint16);perms=[]
 for p in cps:
  ar=np.zeros(16384,dtype=np.uint16)
  for i,j in enumerate(p):ar|=((xs>>i)&1)<<j
  perms.append(ar.tolist())
 O=[-1]*16384;orbits=[]
 for x in range(16384):
  if O[x]>=0:continue
  k=len(orbits);stack=[x];O[x]=k;out=[]
  while stack:
   y=stack.pop();out.append(y)
   for p in perms:
    z=p[y]
    if O[z]<0:O[z]=k;stack.append(z)
  orbits.append(out)
 allowed=[j for j,o in enumerate(orbits) if len(o)<=156];AI={j:i for i,j in enumerate(allowed)};N=len(allowed);C=1<<N;R={}
 def addrow(row):
  while row&(C-1):
   k=(row&(C-1)).bit_length()-1
   if k in R:row^=R[k]
   else:R[k]=row;return True
  return not row&C
 for orb in orbits:
  d=orb[0]
  if d.bit_count()<=8:continue
  row=0;t=d
  while True:
   j=AI.get(O[t])
   if j is not None:row^=1<<j
   if not t:break
   t=(t-1)&d
  assert addrow(row)
 for x in [0]+[1<<i for i in range(14)]:
  if O[x] not in AI:print(mode,'UNSAT normalizationorbitlarge',flush=True);return
  if not addrow((1<<AI[O[x]])|C):print(mode,'UNSAT linear',flush=True);return
 free=[j for j in range(N) if j not in R]
 def finish(v):
  for k,row in sorted(R.items()):
   if (v&row).bit_count()%2:v^=1<<k
  return v
 particular=finish(C);NB=[finish(1<<j) for j in free];pars=[z3.Bool('p%d'%j) for j in range(len(NB))]
 F=[z3.BoolVal(False)]*len(orbits)
 for i,j in enumerate(allowed):
  e=xorall([pars[k] for k,v in enumerate(NB) if v>>i&1]);F[j]=z3.Not(e) if particular>>i&1 else e
 s=z3.SolverFor('QF_FD');pb=[(F[j],len(o)) for j,o in enumerate(orbits)]
 s.add(z3.PbLe(pb,156),z3.PbGe(pb,64));s.set(timeout=30000)
 st=time.time();ans=s.check();print(mode,'orbits',len(orbits),'free',len(NB),'RESULT',ans,'secs',time.time()-st,flush=True)
 if ans==z3.sat:
  model=s.model();S=[x for x in range(16384) if z3.is_true(model.eval(F[O[x]]))]
  ar=np.zeros(16384,dtype=np.uint8);ar[S]=1
  for i in range(14):ar=ar.reshape(-1,2,1<<i);ar[:,1,:]^=ar[:,0,:];ar=ar.reshape(-1)
  deg=max(x.bit_count() for x in np.nonzero(ar)[0]);assert deg<=8
  out={'weight':len(S),'degree':int(deg),'support':S,'group':mode}
  Path('workspace/agent4_co6_group_found.json').write_text(json.dumps(out));print('FOUND',out,flush=True);raise SystemExit
def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&8:a^=11
 return c
pSinger=[mul(2,v)-1 for v in range(1,8)]
pFrob=[mul(v,v)-1 for v in range(1,8)]
gl=[pSinger,pFrob]
for mode in ['product','diag_swap']:test(mode)
gl=[pSinger]
for mode in ['product']:test(mode)
