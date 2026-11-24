import itertools,time
from z3 import *
from agent4_shell_sat import instance
from agent1_shellability import restriction

def check_n8():
 s,fs,t=instance(8,4,stuck=True,seed=True,timeout=180000)
 reps=[27,39,43]
 perms=[]
 for a in itertools.permutations(range(3)):
  for b in [(3,4),(4,3)]:
   for c in itertools.permutations(range(5,8)):
    perms.append(a+b+c)
 def image(F,p):return sum(1<<p[i] for i in range(8) if F>>i&1)
 thirds=[F for F in fs if F not in (15,23) and restriction((15,23),F) is not None]
 for F in thirds:
  assert any(image(F,p) in reps for p in perms),(F,reps)
 print('Verified canonical third-facet orbits for',len(thirds),'possibilities.')
 for F in reps:
  s.push();s.add(t[1]==2,t[fs.index(F)]==3)
  for a in t:s.add(Implies(a>1,Or([b==a-1 for b in t])))
  start=time.time();res=s.check()
  print('third',F,':',res,'in',time.time()-start,flush=True)
  assert res==unsat
  s.pop()
if __name__=='__main__':check_n8()
