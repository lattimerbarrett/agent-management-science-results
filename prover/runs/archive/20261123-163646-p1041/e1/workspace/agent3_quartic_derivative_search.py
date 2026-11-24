import sys,json,itertools,time,numpy as np,collections,shutil,random
sys.path.insert(0,'workspace');import a1_cubic_closure_api as api
from sage.all import matrix,GF
from sage.coding.binary_code import weight_dist
start=time.time();states=json.load(open('workspace/agent3_quartic_highqrank_verified.json'));seen=set();stats=collections.Counter();hits={};records=[]

def lowodd(ker,E):
 if not any(v.bit_count()%2 for v in ker):return []
 ds=len(ker);n=len(E);want={1,3,5,7};out=[]
 for v in ker:
  w=v.bit_count()
  if w in want:out.append(v);want.remove(w)
 if not want:return out
 if ds<=23:
  d=weight_dist(matrix(GF(2),[[(v>>i)&1 for i in range(n)] for v in ker]));goals={w for w in want if w<len(d) and d[w]}
  if not goals:return out
  v=0
  for z in range(1,1<<ds):
   v^=ker[(z&-z).bit_length()-1];w=v.bit_count()
   if w in goals:out.append(v);goals.remove(w)
   if not goals:break
  return out
 import z3
 qs=[z3.Bool('q'+str(i)) for i in range(ds)];bits=[]
 for i in range(n):
  vs=[q for q,v in zip(qs,ker) if v>>i&1]
  e=z3.BoolVal(False)
  for q in vs:e=z3.Xor(e,q)
  bits.append(e)
 s=z3.Solver();s.set(timeout=30000)
 for w in want:
  s.push();s.add(z3.PbEq([(b,1) for b in bits],w))
  if s.check()==z3.sat:
   m=s.model();v=0
   for q,k in zip(qs,ker):
    if z3.is_true(m.eval(q)):v^=k
   assert v.bit_count()==w;out.append(v)
  s.pop()
 return out
for si,r in enumerate(states):
 f=int(r['truth_hex'],16);w=r['weight'];arr=np.unpackbits(np.frombuffer(f.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little');S=list(map(int,np.flatnonzero(arr)));SS=set(S);pts=np.array(S,dtype=np.uint16);C=np.bincount((pts[:,None]^pts).ravel(),minlength=16384);vs=np.flatnonzero(C==w-320);stats['directions']+=len(vs)
 for v in map(int,vs):
  if not v:continue
  bit=v.bit_length()-1;lo=(1<<bit)-1;support=[]
  for x in S:
   if (x^v) in SS:continue
   y=x^v if x>>bit&1 else x;y=(y&lo)|((y>>(bit+1))<<bit);support.append(y)
  assert len(support)==320;hh=sum(1<<x for x in support)
  if hh in seen:continue
  seen.add(hh);stats['unique_h320']+=1
  E,ker,b5=api.closure_kernel(support);stats['nonempty_E']+=bool(E);stats['odd_kernel']+=any(k.bit_count()%2 for k in ker)
  if not E or not any(k.bit_count()%2 for k in ker):continue
  print('ODD KERNEL','state',si,'w',w,'v',v,'E',len(E),'dim',len(ker),flush=True)
  for tt in lowodd(ker,E):
   T=[x for i,x in enumerate(E) if tt>>i&1];rhs=0;coef=0
   for x in T:rhs^=api.cols[x]
   while rhs:
    p=rhs.bit_length()-1;assert p in b5
    vv,cc=b5[p];rhs^=vv;coef^=cc
   g=sum(1<<x for i,x in enumerate(support) if coef>>i&1)|sum(1<<x for x in T);F=g|((g^hh)<<8192);ww=F.bit_count();assert ww==320+2*len(T)
   a=np.unpackbits(np.frombuffer(F.to_bytes(2048,'little'),dtype=np.uint8),bitorder='little').copy()
   for j in range(14):
    st=1<<j;bl=a.reshape(-1,2*st);bl[:,st:]^=bl[:,:st]
   anf=list(map(int,np.flatnonzero(a)));assert max(map(int.bit_count,anf))<=7
   hits[ww]={'truth_hex':hex(F),'anf':anf,'weight':ww,'source_state':si,'source_direction':v,'outside':T};print('VERIFIED HIT',ww,flush=True);json.dump(hits,open('workspace/agent3_quartic_derivative_hits.json','w'))
 if si%20==0:
  print('state',si,'stats',dict(stats),'t',round(time.time()-start,2),flush=True);json.dump(dict(stats),open('workspace/agent3_quartic_derivative_stats.json','w'))
 if len(hits)==4 or time.time()-start>280:break
print('DONE state',si,'stats',dict(stats),'hits',list(hits),'time',time.time()-start,flush=True)
shutil.copyfile(__file__,'workspace/agent3_quartic_derivative_search.py')
