import json,sys,pathlib,time,random,itertools,multiprocessing as mp
sys.path.insert(0,'workspace')
from agent3_lift_closure import veronese,closure

def trans_basis(bs):
 B={};basis=[]
 for v0 in bs+[1<<i for i in range(14)]:
  v=v0;c=0
  while v:
   k=v.bit_length()-1
   if k not in B:
    B[k]=(v,c^(1<<len(basis)));basis.append(v0);break
   v^=B[k][0];c^=B[k][1]
  if len(basis)==14:break
 def encode(p):
  c=0
  while p:
   k=p.bit_length()-1;p^=B[k][0];c^=B[k][1]
  return c
 def decode(p):
  x=0
  for j,b in enumerate(basis):
   if p>>j&1:x^=b
  return x
 assert all(decode(encode(p))==p for p in range(16384))
 return encode,decode

def arank(S):
 B={};o=S[0]
 for p in S:
  p^=o
  while p:
   k=p.bit_length()-1
   if k in B:p^=B[k]
   else:B[k]=p;break
 return len(B)

def worker(args):
 import z3
 seedid,comp,target=args;D=json.load(open('workspace/agent1_fullspan_predecessors.json'));d=D[seedid];enc,dec=trans_basis(d['basis'][comp]);S=set(d['support']);T=[enc(p) for p in S];fib={x:[] for x in range(128)}
 for p in T:fib[p&127].append(p>>7)
 A=[z3.BitVec('a'+str(j),7) for j in range(8)];s=z3.Solver();s.set(timeout=90000,random_seed=seedid+comp+target)
 score=[]
 for x,ys in fib.items():
  if not ys:continue
  y=A[7]
  for j in range(7):
   if x>>j&1:y=y^A[j]
  score.append(z3.Or([y==a for a in ys]))
 s.add(z3.PbEq([(p,1) for p in score],target));t0=time.time();res=s.check();ans={'seed':seedid,'comp':comp,'intersection':target,'status':str(res),'time':time.time()-t0,'fiber_hist':{str(k):sum(len(v)==k for v in fib.values()) for k in set(map(len,fib.values()))}}
 if res==z3.sat:
  model=s.model();aa=[model.eval(a).as_long() for a in A];H=[]
  for x in range(128):
   y=aa[7]
   for j in range(7):
    if x>>j&1:y^=aa[j]
   H.append(dec(x|(y<<7)))
  assert len(S.intersection(H))==target
  G=sorted(S^set(H));assert len(G)==448-2*target;ans.update(weight=len(G),rank=arank(G),support=G,flat=H)
  C,r=closure(set(G),veronese(14,5));ans['cl5extra']=len(C)
  if C:ans['closure_witness']=[C[0][0],C[0][1]]
 return ans

if __name__=='__main__':
 cases=[(0,1,58),(1,3,58),(0,0,60),(1,4,62)]
 with mp.Pool(2) as pool:
  out=[]
  for ans in pool.imap_unordered(worker,cases):
   out.append(ans);print({k:v for k,v in ans.items() if k not in ['support','flat']},flush=True);json.dump(out,open('workspace/agent1_targetflat_sat.json','w'))
 pathlib.Path('workspace/agent1_targetflat_sat.py').write_text(pathlib.Path(__file__).read_text())
