import z3,itertools,time,json
from pathlib import Path

def bits(c):return sum(1<<v for v in c)
def solve(n,timeout):
 D=4;fs=[bits(c) for c in itertools.combinations(range(n),D)];m=len(fs);w=m.bit_length()
 s=z3.SolverFor('QF_BV');s.set(timeout=timeout*1000)
 r=[z3.BitVec('r%d'%i,w) for i in range(m)]
 def less(a,b):return z3.ULT(a,b)
 def leq(a,b):return z3.ULE(a,b)
 for x in r:s.add(leq(x,m))
 s.add(r[0]==1,r[1]==2,z3.Or([x==0 for x in r]))
 for i,x in enumerate(r):
  for y in r[:i]:s.add(z3.Or(x==0,y==0,x!=y))
 t={0:z3.BitVecVal(1,w)}
 for size in range(1,4):
  for c in itertools.combinations(range(n),size):
   a=bits(c);v=z3.BitVec('t%d'%a,w);t[a]=v
   rs=[r[i] for i,f in enumerate(fs) if f&a==a]
   s.add(leq(v,m))
   s.add((v==0)==z3.And([x==0 for x in rs]))
   s.add(z3.Implies(v!=0,z3.Or([v==x for x in rs])))
   for x in rs:s.add(z3.Or(x==0,leq(v,x)))
 for v in range(n):s.add(t[1<<v]!=0)
 for i,f in enumerate(fs):
  vs=[v for v in range(n) if f>>v&1]
  for size in range(3):
   for c in itertools.combinations(vs,size):
    a=bits(c)
    prior=z3.And(t[a]!=0,less(t[a],r[i]))
    ridges=[z3.And(t[f^(1<<v)]!=0,less(t[f^(1<<v)],r[i])) for v in vs if not a>>v&1]
    s.add(z3.Implies(z3.And(r[i]!=0,r[i]!=1,prior),z3.Or(ridges)))
  blocked=[]
  for size in range(3):
   for c in itertools.combinations(vs,size):
    a=bits(c)
    blocked.append(z3.And(t[a]!=0,*[t[f^(1<<v)]==0 for v in vs if not a>>v&1]))
  s.add(z3.Implies(r[i]==0,z3.Or(blocked)))
 print('built',n,m,len(s.assertions()),flush=True);start=time.time();res=s.check();print(n,res,time.time()-start,flush=True)
 out={'n':n,'result':str(res),'seconds':time.time()-start}
 if res==z3.sat:
  model=s.model();out['order']=[f for rank,f in sorted((model.eval(r[i]).as_long(),f) for i,f in enumerate(fs)) if rank]
 Path('workspace/agent1_bv_sat_%d.json'%n).write_text(json.dumps(out))
 if res==z3.sat:print(out['order'],flush=True)
 return res
if __name__=='__main__':
 Path('workspace/agent1_bv_sat.py').write_text(Path(__file__).read_text())
 solve(8,120)
 solve(9,360)
