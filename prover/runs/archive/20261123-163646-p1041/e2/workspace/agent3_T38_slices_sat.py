import z3,itertools,time,json,pathlib,sys,numpy as np
sys.path.insert(0,'workspace')
from agent1_checked_grid import degree

def parity(v,L):
 shift=1
 while shift<L:v=v^z3.LShR(v,shift);shift*=2
 return z3.Extract(0,0,v)
def xorall(vs):
 v=vs[0]
 for x in vs[1:]:v=v^x
 return v

def solve(delta,tm=90000):
 n=38;d=11;L=n-delta-12
 if delta==8:T=list(range(8));q=3
 elif delta==12:T=[x^3 for x in range(32) if (((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1)))];q=5
 else:T=[x^1 for x in list(range(1,8))+[j<<3 for j in range(1,8)]];q=6
 assert len(T)==delta and 0 in T
 cs=[z3.BitVec(f'c{delta}_{j}',d) for j in range(L)];B=[z3.BitVec(f'b{delta}_{i}',d) for i in range(q)]
 s=z3.Then('simplify','solve-eqs','bit-blast',z3.With('sat',anf=True,**{'anf.exlin':True,'anf.delay':0})).solver();s.set(timeout=tm)
 for c in cs:s.add(c!=0,*[c!=1<<j for j in range(d)])
 for c,e in zip(cs,cs[1:]):s.add(z3.ULT(c,e))
 for mask in range(1,1<<q):s.add(xorall([B[i] for i in range(q) if mask>>i&1])!=0)
 tail=[xorall([B[i] for i in range(q) if x>>i&1]) for x in T if x]
 r0=[z3.Concat(*[z3.Extract(i,i,c) for c in reversed(cs)]) for i in range(d)]
 r1=[z3.Concat(*[z3.Extract(i,i,c) for c in reversed(tail)]) for i in range(d)]
 for a,b in zip(r0,r0[1:]):s.add(z3.ULT(a,b))
 for k in range(1,4):
  for inds in itertools.combinations(range(d),k):
   v0=r0[inds[0]];v1=r1[inds[0]]
   for i in inds[1:]:v0=v0&r0[i];v1=v1&r1[i]
   s.add(parity(v0,L)^parity(v1,delta-1)==(1 if k==1 else 0))
 print('built delta',delta,'vars',len(cs)*11+len(B)*11,'assertions',len(s.assertions()),flush=True);t=time.time();r=s.check();print('result',delta,r,time.time()-t,flush=True)
 out={'delta':delta,'result':str(r),'reason':s.reason_unknown() if r==z3.unknown else None}
 if r==z3.sat:
  model=s.model();S=[0]+[1<<j for j in range(d)]+[model[c].as_long() for c in cs]+[(1<<11)]+[(1<<11)^model.eval(a).as_long() for a in tail]
  assert len(set(S))==n
  arr=np.zeros(1<<12,dtype=np.uint8);arr[S]=1;assert degree(arr)<=8
  out['support']=S
 return out
out=[]
for delta in [8,12,14]:
 out.append(solve(delta));pathlib.Path('workspace/agent3_T38_slices_sat.json').write_text(json.dumps(out))
 if 'support' in out[-1]:break
pathlib.Path('workspace/agent3_T38_slices_sat.py').write_text(pathlib.Path(__file__).read_text())
