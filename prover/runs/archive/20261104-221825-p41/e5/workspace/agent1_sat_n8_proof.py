from itertools import combinations
import z3,time,json
z3.set_param(proof=True)
n=8;q=4
F=[sum(1<<x for x in c) for c in combinations(range(n),q)];m=len(F)
s=z3.Solver();s.set(timeout=240000)
t=[z3.Int('t%d'%i) for i in range(m)];P=[x<=m for x in t]
s.add(*[z3.And(x>=1,x<=m+1) for x in t]);s.add(t[0]==1,t[1]==2)
for i in range(m):
 for j in range(i):s.add(z3.Or(z3.Not(P[i]),z3.Not(P[j]),t[i]!=t[j]))
s.add(z3.Or(*[z3.Not(p) for p in P]))
R={}; B={}
for i,f in enumerate(F):
 vs=[v for v in range(n) if f>>v&1]
 for v in vs:
  r=R[i,v]=z3.Bool('r%d_%d'%(i,v));b=B[i,v]=z3.Bool('b%d_%d'%(i,v))
  ridge=f^(1<<v)
  nn=[j for j,g in enumerate(F) if j!=i and g&ridge==ridge]
  s.add(b==z3.Or(*[P[j] for j in nn]))
  if i:s.add(z3.Implies(z3.And(P[i],r),z3.Or(*[t[j]<t[i] for j in nn])))
 if i:s.add(z3.Implies(P[i],z3.Or(*[R[i,v] for v in vs])))
 for j,g in enumerate(F):
  if i==j:continue
  if i:s.add(z3.Implies(z3.And(P[i],t[j]<t[i]),z3.Or(*[R[i,v] for v in vs if not(g>>v&1)])))
 s.add(z3.Implies(z3.Not(P[i]),z3.Or(*[
  z3.And(P[j],*[z3.Not(B[i,v]) for v in vs if not(g>>v&1)])
  for j,g in enumerate(F) if i!=j])))
for v in range(n):s.add(z3.Or(*[P[i] for i,f in enumerate(F) if f>>v&1]))
print('encoded',n,m,len(s.assertions()),flush=True)
start=time.time();result=s.check();print(result,time.time()-start,flush=True)
if result==z3.sat:
 model=s.model();ranks=[model.eval(x).as_long() for x in t];prefix=sorted([i for i in range(m) if ranks[i]<=m],key=lambda i:ranks[i])
 def legal(old,i):
  ints=[F[i]&F[j] for j in old];rr=[x for x in ints if x.bit_count()==q-1]
  return not old or bool(rr) and all(any(x&r==x for r in rr) for x in ints)
 old=[]
 for i in prefix:assert legal(old,i);old.append(i)
 assert all(not legal(prefix,i) for i in range(m) if i not in prefix)
 out={'n':n,'d':q-1,'prefix':[[v for v in range(n) if F[i]>>v&1] for i in prefix]};print(out)
 with open('workspace/agent1_obstruction.json','w') as ff:json.dump(out,ff)
else:
 print(s.reason_unknown())
 if result==z3.unsat:
  proof=str(s.proof());print('proof chars',len(proof),flush=True)
  with open('workspace/agent1_n8_unsat_proof.txt','w') as ff:ff.write(proof)
with open('workspace/agent1_n8_trap.smt2','w') as ff:ff.write(s.to_smt2())
with open('workspace/agent1_sat_n8_proof.py','w') as ff:ff.write(open(__file__).read())
