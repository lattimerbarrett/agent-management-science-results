import numpy as np, itertools, time, pickle, pathlib, sys
sys.path.insert(0,'workspace')
from agent1_checked_grid import witnesses,truth_table

def veronese(m,d):
 fn=pathlib.Path(f'workspace/agent3_veronese_{m}_{d}.pkl')
 if fn.exists():return pickle.loads(fn.read_bytes())
 masks=[sum(1<<i for i in S) for k in range(d+1) for S in itertools.combinations(range(m),k)]
 xs=np.arange(1<<m,dtype=np.uint32)
 mat=np.zeros((1<<m,(len(masks)+63)//64),dtype='<u8')
 for j,mask in enumerate(masks):mat[:,j//64]|=((xs&mask)==mask).astype(np.uint64)<<np.uint64(j%64)
 vs=[int.from_bytes(row.tobytes(),'little') for row in mat]
 fn.write_bytes(pickle.dumps(vs));return vs

def closure(S,vs):
 basis={};comb={}
 for i,s in enumerate(S):
  v=vs[s];c=1<<i
  while v:
   k=v.bit_length()-1
   if k not in basis:basis[k]=v;comb[k]=c;break
   v^=basis[k];c^=comb[k]
 out=[]
 for p,v in enumerate(vs):
  if p in S:continue
  c=0
  while v:
   k=v.bit_length()-1
   if k not in basis:break
   v^=basis[k];c^=comb[k]
  if not v:out.append((p,c))
 return out,len(basis)
if __name__=='__main__':
 t=time.time();vs=veronese(14,5);print('veronese',time.time()-t)
 from agent1_checked_grid import dyadic_blocks,degree
 targets=[256,272,288,296,304,308,320,324,328,332]
 found=[];ranks={w:set() for w in targets};counts={w:0 for w in targets}
 for a in range(129):
  for b in range(129):
   base=128*(a+b)-2*a*b
   caps=[]
   for ranges in [[(0,a,0,b),(a,128,b,128)],[(0,a,b,128),(a,128,0,b)]]:
    caps.append(sum(sx*sy for x0,x1,y0,y1 in ranges for x,sx in dyadic_blocks(x0,x1) for y,sy in dyadic_blocks(y0,y1) if sx*sy>=128)//128)
   for w in targets:
    if (w-base)%128:continue
    tt=(w-base)//128
    if not -caps[1]<=tt<=caps[0]:continue
    arr=truth_table(a,b,tt);assert int(arr.sum())==w
    S=set(np.where(arr)[0].tolist());cl,rk=closure(S,vs)
    counts[w]+=1;ranks[w].add(rk)
    if cl:
     p,c=cl[0];ss=list(S);h=np.zeros(16384,dtype=np.uint8);h[p]=1
     for i,s in enumerate(ss):
      if c>>i&1:h[s]=1
     assert degree(h)<=8
     f=np.concatenate([h,h^arr]);assert int(f.sum())==w+2;assert degree(f)<=8
     found.append({'w':w+2,'a':a,'b':b,'t':tt,'p':p,'h_support':np.where(h)[0].tolist()})
     print('FOUND',found[-1]);raise SystemExit
 print('counts',counts,'ranks',ranks,'time',time.time()-t)
 import json
 pathlib.Path('workspace/agent3_lift_closure_results.json').write_text(json.dumps({'counts':counts,'ranks':{w:sorted(rs) for w,rs in ranks.items()},'found':found}))
 pathlib.Path('workspace/agent3_lift_closure.py').write_text(pathlib.Path(__file__).read_text())
